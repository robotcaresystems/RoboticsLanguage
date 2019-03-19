#
#   This is the Robotics Language compiler
#
#   Parse.py: Parses the Decision Graph language
#
#   Created on: 11 March, 2019
#       Author: Gabriel Lopes
#      Licence: license
#    Copyright: Robot Care Systems BV
#
import sys
from lxml import etree
from parsley import makeGrammar
from RoboticsLanguage.Tools import Parsing
from RoboticsLanguage.Base import Utilities
from RoboticsLanguage.Inputs.RoL import Parse as RoL

grammar_definition = """
name = <letter ( letter | '_' | '.' | digit )*>

end = ';' wws

graph_name = 'name' ws ':' ws name:w ws end-> xml('name', text=w , attributes={'p':str(self.input.position + P)})

initial = 'initial' ws ':' ws name:w ws end-> xml('initial', text=w , attributes={'p':str(self.input.position + P)})

# comments
wws = (ws longComment)* (ws shortComment)* ws

longComment = ('##'  <(~('##') anything)+>:c  '##' -> xml('comment',text=str(c), attributes={'p':str(self.input.position + P)}))

shortComment = ('#'  <(~('\n') anything)+>:c  '\n' -> xml('comment',text=str(c), attributes={'p':str(self.input.position + P)}))

trueArrow = ( '-T->' | '-t->' | '-True->' | '-true->' )

falseArrow = ( '-F->' | '-f->' | '-False->' | '-false->' )

decision = name:n wws trueArrow wws name:t wws falseArrow wws name:f wws end -> xml('decision', [xml('true', attributes={'name':t, 'p':str(self.input.position + P)}), xml('false', attributes={'name':f, 'p':str(self.input.position + P)})], attributes={'name':n, 'p':str(self.input.position + P)})

expression = ('|'  <(~('|') anything)+>:c  '|' -> xml('expression',text=str(c), attributes={'text':str(c), 'p':str(self.input.position + P)}))

decisionInLine = name:n wws expression:e wws trueArrow wws name:t wws falseArrow wws name:f wws end -> xml('decision', [e,xml('true', attributes={'name':t, 'p':str(self.input.position + P)}), xml('false', attributes={'name':f, 'p':str(self.input.position + P)})], attributes={'name':n, 'p':str(self.input.position + P)})


case = '-' expression:e '->' wws name:n -> xml('case',[e, xml('node', attributes={'name':n})], attributes={'p':str(self.input.position + P)})

switch = name:s wws  expression:e   ( wws case )*:c end -> xml('switch', [e] + c, attributes={'name':s, 'p':str(self.input.position + P)})

sequence = name:f wws '->' wws name:t wws end -> xml('sequence', xml('to', attributes={'name':t, 'p':str(self.input.position + P)}),  attributes={'name':f, 'p':str(self.input.position + P)})

main = wws graph_name:n wws initial:i wws ( decision | decisionInLine | switch | sequence )*:e wws -> xml('DecisionGraph', [n, i] + e )

"""


def parse(text, parameters):
  namespace = {'namespaces': {'dg': 'dg'}}

  # make the grammar
  grammar = makeGrammar(grammar_definition, {'xml': Parsing.xmlNamespace(
      'dg'), 'P': parameters['parsing']['position']})

  # parse the text
  code = grammar(text).main()

  nodes = {node: {'type': 'function'}
           for node in code.xpath('//*/@name', **namespace)}

  name = code.xpath('//dg:DecisionGraph/dg:name/text()', **namespace)[0]

  prefix = 'dg_' + name + '_'

  functions = etree.SubElement(code, '{dg}functions')

  arcs = []

  arcs_counter = 1

  # # add extra topic for publishing arcs
  rol_code, rol_parameters = RoL.parse('expression(dg_' + name + '_publisher in Signals(Integers,rosTopic:"/temporary"))', parameters)

  functions.insert(0, rol_code.getchildren()[0])

  # decisions
  for node in code.xpath('//dg:decision', **namespace):

    arc_true = None
    arc_false = None

    # parameter definitions
    nodes[node.attrib['name']]['type'] = 'decision'

    expression = node.xpath('.//dg:expression', **namespace)
    if len(expression) > 0:
      nodes[node.attrib['name']]['label'] = expression[0].text

    true_node = node.xpath('.//dg:true', **namespace)
    if len(true_node) > 0:
      arcs.append(
          {'begin': node.attrib['name'], 'end': true_node[0].attrib['name'], 'label': 'true', 'id':arcs_counter})
      arc_true = arcs_counter
      arcs_counter = arcs_counter + 1


    false_node = node.xpath('.//dg:false', **namespace)
    if len(false_node) > 0:
      arcs.append(
          {'begin': node.attrib['name'], 'end': false_node[0].attrib['name'], 'label': 'false', 'id':arcs_counter})
      arc_false = arcs_counter
      arcs_counter = arcs_counter + 1

    # function definitions
    function_definition = etree.SubElement(functions, 'function_definition', attrib={'name': prefix + node.attrib['name']})
    function_content = etree.SubElement(function_definition, 'function_content')
    if_statement = etree.SubElement(function_content, 'if')

    if len(expression) > 0:
      rol_code, rol_parameters = RoL.parse('expression(' + expression[0].text + ')', parameters)
      if_statement.insert(0, rol_code.getchildren()[0])
    else:
      etree.SubElement(if_statement, 'function', attrib={'name': node.attrib['name']})

    block_true = etree.SubElement(if_statement, 'block')
    rol_code, rol_parameters = RoL.parse('expression(' + prefix + 'publisher = ' + str(arc_true) + ')', parameters)
    block_true.insert(0, rol_code.getchildren()[0])
    etree.SubElement(block_true, 'function', attrib={'name': prefix + true_node[0].attrib['name']})

    block_false = etree.SubElement(if_statement, 'block')
    rol_code, rol_parameters = RoL.parse('expression(' + prefix + 'publisher = ' + str(arc_false) + ')', parameters)
    block_false.insert(0, rol_code.getchildren()[0])
    etree.SubElement(block_false, 'function', attrib={'name': prefix + false_node[0].attrib['name']})

    nodes[node.attrib['name']]['definition'] = function_definition


  # switches
  for node in code.xpath('//dg:switch', **namespace):

    # parameters
    nodes[node.attrib['name']]['type'] = 'switch'
    expression = node.xpath('.//dg:expression', **namespace)
    nodes[node.attrib['name']]['expression'] = expression[0].text

    # code
    function_definition = etree.SubElement(functions, 'function_definition', attrib={'name': prefix + node.attrib['name']})
    function_content = etree.SubElement(function_definition, 'function_content')
    switch_statement = etree.SubElement(function_content, 'switch')

    rol_code, rol_parameters = RoL.parse('expression(' + expression[0].text + ')', parameters)
    switch_statement.insert(0, rol_code.getchildren()[0])

    for case in node.xpath('.//dg:case', **namespace):

      function_to = case.xpath('.//dg:node/@name', namespaces={'dg': 'dg'})[0]

      arcs.append({'begin': node.attrib['name'], 'end': function_to, 'label': case.xpath('.//dg:expression/@text', **namespace)[0], 'id':arcs_counter})
      arcs_counter = arcs_counter + 1

      case_expression = case.xpath('.//dg:expression', **namespace)
      case_statement = etree.SubElement(switch_statement, 'case')
      rol_code, rol_parameters = RoL.parse('expression(' + case_expression[0].text + ')', parameters)

      case_statement.insert(0, rol_code.getchildren()[0])

      block_case = etree.SubElement(case_statement, 'block')
      rol_code, rol_parameters = RoL.parse('expression(' + prefix + 'publisher = ' + str(arcs_counter - 1) + ')', parameters)
      block_case.insert(0, rol_code.getchildren()[0])
      etree.SubElement(block_case, 'function', attrib={'name': prefix + function_to})

    nodes[node.attrib['name']]['definition'] = function_definition



  # sequences
  for node in code.xpath('//dg:sequence', **namespace):

    # name of the next function in the sequence
    sequence_to = node.xpath('.//dg:to/@name', **namespace)[0]

    # parameters definitions
    arcs.append({'begin': node.attrib['name'], 'end': sequence_to, 'id':arcs_counter})
    arcs_counter = arcs_counter + 1

    # function definitions
    function_definition = etree.SubElement(functions, 'function_definition', attrib={'name': prefix + node.attrib['name']})
    function_content = etree.SubElement(function_definition, 'function_content')
    rol_code, rol_parameters = RoL.parse('expression(' + prefix + 'publisher = ' + str(arcs_counter - 1) + ')', parameters)
    function_content.insert(0, rol_code.getchildren()[0])
    etree.SubElement(function_content, 'function', attrib={'name': node.attrib['name']})
    etree.SubElement(function_content, 'function', attrib={'name': prefix + sequence_to})

    nodes[node.attrib['name']]['definition'] = function_definition


  # add functions for terminal branches
  for element in nodes:
    if 'definition' not in nodes[element].keys():
      function_definition = etree.SubElement(functions, 'function_definition', attrib={'name': prefix + element})
      function_content = etree.SubElement(function_definition, 'function_content')
      etree.SubElement(function_content, 'function', attrib={'name': element})

      nodes[element]['definition'] = function_definition


  # add unique id's to nodes and arcs
  # map(lambda (x, y): x.update({'id': y}), zip(arcs, range(len(arcs))))
  map(lambda (x, y): x.update({'id': y}), zip(
      nodes.itervalues(), range(len(nodes))))

  # add from and to id's to arcs
  map(lambda x: x.update({'from': nodes[x['begin']]['id']}), arcs)
  map(lambda x: x.update({'to': nodes[x['end']]['id']}), arcs)

  parameters['Transformers']['DecisionGraph']['graphs'][name] = {}
  parameters['Transformers']['DecisionGraph']['graphs'][name]['nodes'] = nodes
  parameters['Transformers']['DecisionGraph']['graphs'][name]['arcs'] = arcs


  return code, parameters
