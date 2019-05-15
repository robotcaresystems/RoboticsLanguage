# -*- coding: utf-8 -*-
#
#   This is the Robotics Language compiler
#
#   Parameters.py: Definition of the parameters for this package
#
#   Created on: 05 September, 2018
#       Author: Gabriel Lopes
#      Licence: license
#    Copyright: copyright
#


from RoboticsLanguage.Base import Utilities
from RoboticsLanguage.Tools import Serialise

# @BUG When using too many 'block' statements this function will fail. Example:
# cachedComputation:
#   block(
#     if(state == "idle",block(block(block(z=x)),block(block(x=z,y=x))),
#       z = x),
#     if(state == "idle",block(z=x,x=z,y=x),
#       z = x)
#     )


def buildCachedComputationGraph(parameters, code, list, id=0, leafs=[]):

  for expression, index in zip(list, range(len(list))):
    id = id + 1

    if expression.tag != 'if':
      # process generic computations
      if expression.tag == 'block':
        # make sure to expand blocks
        id, leafs = buildCachedComputationGraph(parameters, code, expression.getchildren(), id - 1, leafs)

      else:
        # add computation cache element
        expression.attrib['cacheId'] = str(id)
        expression.attrib['cacheClass'] = "computation"

        # check for assign clauses to add output
        if expression.tag == 'assign':
          expression.attrib['cacheOutput'] = expression.getchildren()[0].attrib['name']
          inputs_to_check = expression.getchildren()[1]
        else:
          inputs_to_check = expression

        # add inputs to function
        if inputs_to_check.tag == 'variable':
          expression.attrib['cacheInputs'] = inputs_to_check.attrib['name']
        else:
          expression.attrib['cacheInputs'] = ','.join(Utilities.unique(inputs_to_check.xpath('.//variable/@name')))

        # connect the cache to the next block being executed
        if index == len(list) - 1:
          # if unknow save it to a list
          leafs.append(id)
        else:
          # if it is known save the next id
          expression.attrib['cacheNext'] = str(id + 1)

    else:
      # process if statements
      expression.attrib['cacheId'] = str(id)
      expression.attrib['cacheClass'] = "if"

      if_expression = expression.getchildren()

      # add inputs to function
      if if_expression[0].tag == 'variable':
        expression.attrib['cacheInputs'] = if_expression[0].attrib['name']
      else:
        expression.attrib['cacheInputs'] = ','.join(Utilities.unique(if_expression[0].xpath('.//variable/@name')))

      # process the true side
      expression.attrib['cacheTrue'] = str(id + 1)
      id, leafs = buildCachedComputationGraph(parameters, code, [if_expression[1]], id, leafs)

      leafs_right = leafs
      leafs = []
      leafs_left = []

      # process the false side
      if len(if_expression) > 2:
        expression.attrib['cacheFalse'] = str(id + 1)

        id, leafs = buildCachedComputationGraph(parameters, code, [if_expression[2]], id, leafs)

        leafs_left = leafs
        leafs = []
      else:
        # point to the next expression being executed
        expression.attrib['cacheFalse'] = str(id + 1)

      # for all expressions with unknown next state, add the next state here
      for x in leafs_right:
        code.xpath('//*[@cacheId="' + str(x) + '"]')[0].attrib['cacheNext'] = str(id + 1)
      for x in leafs_left:
        code.xpath('//*[@cacheId="' + str(x) + '"]')[0].attrib['cacheNext'] = str(id + 1)

  return id, leafs


def printGraphvizDot(code, parameters):

  # find cachedComputation
  cachedComputation = code.xpath('/node/option[@name="cachedComputation"]')

  if len(cachedComputation) > 0:
    # use the RoL serialiser to create the text tag
    Serialise.serialise(cachedComputation[0], parameters, parameters['language'], 'RoL')

    # get all cachedComputation
    elements = code.xpath('/node/option[@name="cachedComputation"]//*[@cacheId]')

    # header of the graphviz plot
    print 'digraph test{'
    print '0 [shape="point"]'
    print '0->1'

    max_cache_next = -1

    for element in elements:
      # look for if clauses
      if element.attrib['cacheClass'] == 'if':
        print element.attrib['cacheId'] + ' [shape = "diamond", color="blue", fontcolor="blue", label="' + \
            element.attrib['cacheId'] + ': if' + element.getchildren()[0].attrib['RoL'] + \
            '" xlabel="{' + element.attrib['cacheInputs'] + '}"]'
        print element.attrib['cacheId'] + '->' + element.attrib['cacheTrue'] + ' [label="yes"]'
        if 'cacheFalse' in element.attrib:
          print element.attrib['cacheId'] + '->' + element.attrib['cacheFalse'] + ' [label="no"]'

      # look for computations
      if element.attrib['cacheClass'] == 'computation':

        if 'cacheOutput' in element.attrib:
          output = '→' + element.attrib['cacheOutput']
        else:
          output = ''

        print element.attrib['cacheId'] + ' [shape = "box", label="' + \
            element.attrib['cacheId'] + ': ' + element.attrib['RoL'] + \
            '" xlabel="{' + element.attrib['cacheInputs'] + output + '}"]'
        if 'cacheNext' in element.attrib:
          print element.attrib['cacheId'] + '->' + element.attrib['cacheNext']
          max_cache_next = max(max_cache_next, int(element.attrib['cacheNext']))

    # make the end node
    if max_cache_next > len(elements):
      print str(max_cache_next) + ' [shape="point"]'
    else:
      print str(max_cache_next + 1) + ' [shape="point"]'
      print str(max_cache_next) + '->' + str(max_cache_next + 1)

    # done
    print '}'


def transform(code, parameters):

  # find code about cachedComputation
  cachedComputation = code.xpath('/node/option[@name="cachedComputation"]/*')

  # traverses the code in cachedComputation and builds graph
  buildCachedComputationGraph(parameters, code, cachedComputation)

  # show graphviz graph if needed
  if parameters['Transformers']['CachedComputation']['printGraphviz']:
    printGraphvizDot(code, parameters)

  return code, parameters
