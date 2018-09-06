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

# @BUG When using too many 'block' statements this function will fail. Example:
# events:
#   block(
#     if(state == "idle",block(block(block(z=x)),block(block(x=z,y=x))),
#       z = x),
#     if(state == "idle",block(z=x,x=z,y=x),
#       z = x)
#     )
def buildEventsGraph(parameters, code, list, id=0, leafs=[]):

  for expression, index in zip(list, range(len(list))):
    id = id + 1

    if expression.tag != 'if':
      # process generic computations
      if expression.tag == 'block':
        # make sure to expand blocks
        id, leafs = buildEventsGraph(parameters, code, expression.getchildren(), id - 1, leafs)

      else:
        # add computation event element
        expression.attrib['eventId'] = str(id)
        expression.attrib['eventClass'] = "computation"

        # connect the event to the next block being executed
        if index == len(list) - 1:
          # if unknow save it to a list
          leafs.append(id)
        else:
          # if it is known save the next id
          expression.attrib['eventNext'] = str(id + 1)

    else:
      # process if statements
      expression.attrib['eventId'] = str(id)
      expression.attrib['eventClass'] = "if"

      if_expression = expression.getchildren()

      expression.attrib['eventTrue'] = str(id + 1)

      # process the true side
      id, leafs = buildEventsGraph(parameters, code, [if_expression[1]], id, leafs)

      leafs_right = leafs
      leafs = []
      leafs_left = []

      # process the false side
      if len(if_expression) > 2:
        expression.attrib['eventFalse'] = str(id + 1)

        id, leafs = buildEventsGraph(parameters, code, [if_expression[2]], id, leafs)

        leafs_left = leafs
        leafs = []
      else:
        # point to the next expression being executed
        expression.attrib['eventFalse'] = str(id + 1)

      # for all expressions with unknown next state, add the next state here
      for x in leafs_right:
        code.xpath('//*[@eventId="' + str(x) + '"]')[0].attrib['eventNext'] = str(id + 1)
      for x in leafs_left:
        code.xpath('//*[@eventId="' + str(x) + '"]')[0].attrib['eventNext'] = str(id + 1)

  return id, leafs


def printGraphvizDot(code, parameters):

  # find events
  events = code.xpath('/node/option[@name="events"]')

  if len(events) > 0:
    # use the RoL serialiser to create the text tag
    Utilities.serialise(events[0], parameters, parameters['language'], 'RoL')

    # get all events
    elements = code.xpath('/node/option[@name="events"]//*[@eventId]')

    # header of the graphviz plot
    print 'digraph test{'
    print '0 [shape="point"]'
    print '0->1'

    max_event_next = -1

    for element in elements:
      # look for if clauses
      if element.attrib['eventClass'] == 'if':
        print element.attrib['eventId'] + ' [shape = "diamond", label="' + \
            element.attrib['eventId'] + ': if' + element.getchildren()[0].attrib['RoL'] + '"]'
        print element.attrib['eventId'] + '->' + element.attrib['eventTrue'] + ' [label="yes"]'
        if 'eventFalse' in element.attrib:
          print element.attrib['eventId'] + '->' + element.attrib['eventFalse'] + ' [label="no"]'

      # look for computations
      if element.attrib['eventClass'] == 'computation':
        print element.attrib['eventId'] + ' [shape = "box", label="' + \
            element.attrib['eventId'] + ': ' + element.attrib['RoL'] + '"]'
        if 'eventNext' in element.attrib:
          print element.attrib['eventId'] + '->' + element.attrib['eventNext']
          max_event_next = max(max_event_next, int(element.attrib['eventNext']))

    # make the end node
    if max_event_next > len(elements):
      print str(max_event_next) + ' [shape="point"]'
    else:
      print str(max_event_next + 1) + ' [shape="point"]'
      print str(max_event_next) + '->' + str(max_event_next + 1)

    # done
    print '}'


def transform(code, parameters):

  # find code about events
  events = code.xpath('/node/option[@name="events"]/*')

  # traverses the code in events and builds graph
  buildEventsGraph(parameters, code, events)

  # show graphviz graph if needed
  if parameters['Transformers']['Events']['printGraphviz']:
    printGraphvizDot(code, parameters)

  return code, parameters
