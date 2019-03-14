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
name = <letter ( letter | '_' | digit )*>

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

  # make the grammar
  grammar = makeGrammar(grammar_definition, {'xml': Parsing.xmlNamespace(
      'dg'), 'P': parameters['parsing']['position']})

  # parse the text
  code = grammar(text).main()

  nodes = {node: {'type': 'function'}
           for node in code.xpath('//*/@name', namespaces={'dg': 'dg'})}

  name = code.xpath('//dg:DecisionGraph/dg:name/text()', namespaces={'dg': 'dg'})[0]

  arcs = []


  # decisions
  for node in code.xpath('//dg:decision', namespaces={'dg': 'dg'}):
    nodes[node.attrib['name']]['type'] = 'decision'

    expression = node.xpath('.//dg:expression', namespaces={'dg': 'dg'})
    if len(expression) > 0:
      nodes[node.attrib['name']]['label'] = expression[0].text

    true_node = node.xpath('.//dg:true', namespaces={'dg': 'dg'})
    if len(true_node) > 0:
      arcs.append(
          {'begin': node.attrib['name'], 'end': true_node[0].attrib['name'], 'label': 'true'})

    false_node = node.xpath('.//dg:false', namespaces={'dg': 'dg'})
    if len(false_node) > 0:
      arcs.append(
          {'begin': node.attrib['name'], 'end': false_node[0].attrib['name'], 'label': 'false'})

  # switches
  for node in code.xpath('//dg:switch', namespaces={'dg': 'dg'}):
    nodes[node.attrib['name']]['type'] = 'switch'
    expression = node.xpath('.//dg:expression', namespaces={'dg': 'dg'})
    nodes[node.attrib['name']]['expression'] = expression[0].text
    for case in node.xpath('.//dg:case', namespaces={'dg': 'dg'}):
      arcs.append({'begin': node.attrib['name'], 'end': case.xpath('.//dg:node/@name', namespaces={
                  'dg': 'dg'})[0], 'label': case.xpath('.//dg:expression/@text', namespaces={'dg': 'dg'})[0]})

  # sequences
  for node in code.xpath('//dg:sequence', namespaces={'dg': 'dg'}):
    arcs.append({'begin': node.attrib['name'], 'end': node.xpath(
        './/dg:to/@name', namespaces={'dg': 'dg'})[0]})

  # add unique to nodes and arcs
  map(lambda (x, y): x.update({'id': y}), zip(arcs, range(len(arcs))))
  map(lambda (x, y): x.update({'id': y}), zip(
      nodes.itervalues(), range(len(nodes))))

  # add from and to id's to arcs
  map(lambda x: x.update({'from': nodes[x['begin']]['id']}), arcs)
  map(lambda x: x.update({'to': nodes[x['end']]['id']}), arcs)

  parameters['Transformers']['DecisionGraph']['graphs'][name] = {}
  parameters['Transformers']['DecisionGraph']['graphs'][name]['nodes'] = nodes
  parameters['Transformers']['DecisionGraph']['graphs'][name]['arcs'] = arcs

  # # replace the inside of the 'expression' tags with RoL code
  # for expression in code.xpath('//dg:expression', namespaces={'dg': 'dg'}):
  #
  #   print expression.text
  #   # RoL.parse(expression.text, parameters)

  return code, parameters
