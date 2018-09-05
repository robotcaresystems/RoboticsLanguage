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


def printGraphviz(parameters, string):
  if parameters['Transformers']['Events']['printGraphviz']:
    print(string())


def buildEventsGraph(parameters, code, list, id=0, leafs=[]):

  for expression, index in zip(list, range(len(list))):
    id = id + 1

    if expression.tag != 'if':
      if expression.tag == 'block':
        id, leafs = buildEventsGraph(parameters, code, expression.getchildren(), id - 1, leafs)

      else:
        expression.attrib['eventId'] = str(id)
        expression.attrib['eventClass'] = "computation"
        printGraphviz(parameters, lambda: str(id) + ' [label="' + str(id) + ': ' + expression.attrib['RoL'] + '"]')

        if index == len(list) - 1:
          leafs.append(id)
        else:
          expression.attrib['eventNext'] = str(id + 1)
          printGraphviz(parameters, lambda: str(id) + '->' + str(id + 1))

    else:
      expression.attrib['eventId'] = str(id)
      expression.attrib['eventClass'] = "if"
      if_id = id

      if_expression = expression.getchildren()

      printGraphviz(parameters, lambda: str(if_id) + ' [shape = "diamond", label="' + str(id) + ': if' + if_expression[0].attrib['RoL'] + '"]')

      expression.attrib['eventTrue'] = str(id + 1)
      printGraphviz(parameters, lambda: str(if_id) + '->' + str(id + 1) + ' [label="Y"]')
      id, leafs = buildEventsGraph(parameters, code, [if_expression[1]], id, leafs)

      leafs_right = leafs
      leafs = []
      leafs_left = []

      if len(if_expression) > 2:
        expression.attrib['eventFalse'] = str(id + 1)
        printGraphviz(parameters, lambda: str(if_id) + '->' + str(id + 1) + ' [label="N"]')
        id, leafs = buildEventsGraph(parameters, code, [if_expression[2]], id, leafs)

        leafs_left = leafs
        leafs = []
      else:
        expression.attrib['eventFalse'] = str(id + 1)
        printGraphviz(parameters, lambda: str(if_id) + '->' + str(id + 1) + ' [label="N"]')

      for x in leafs_right:
        code.xpath('//*[@eventId="' + str(x) + '"]')[0].attrib['eventNext'] = str(id + 1)
        printGraphviz(parameters, lambda: str(x) + '->' + str(id + 1))
      for x in leafs_left:
        code.xpath('//*[@eventId="' + str(x) + '"]')[0].attrib['eventNext'] = str(id + 1)
        printGraphviz(parameters, lambda: str(x) + '->' + str(id + 1))

  return id, leafs


def transform(code, parameters):

  # find code about events
  events = code.xpath('/node/option[@name="events"]')

  # use the RoL serialiser to create the text tag
  if parameters['Transformers']['Events']['printGraphviz']:
    Utilities.serialise(events[0], parameters, parameters['language'], 'RoL')

  printGraphviz(parameters, lambda: """digraph test{
  node [shape="box"];
""")

  # call buildEventsGraph parameters, with a list that has at least one expression
  if len(events) > 0:
    if len(events[0].getchildren()) > 0:
      buildEventsGraph(parameters, code, events[0].getchildren())

  printGraphviz(parameters, lambda: "}")

  return code, parameters
