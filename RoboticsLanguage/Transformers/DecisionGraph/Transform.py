#
#   This is the Robotics Language compiler
#
#   Transform.py: Decision Graph code transformer
#
#   Created on: 14 March, 2019
#       Author: Gabriel Lopes
#      Licence: license
#    Copyright: Robot Care Systems BV
#
import copy
from lxml import etree
from RoboticsLanguage.Base import Utilities
from RoboticsLanguage.Inputs.RoL import Parse as RoL


def transform(code, parameters):
  try:
    namespace = {'namespaces': {'dg': 'dg'}}

    definitions = code.xpath('/node/option[@name="definitions"]/block')[0]

    node_name = Utilities.underscore(code.xpath('/node/option[@name="name"]/string')[0].text)

    # add a topic to publish progress
    for graph in code.xpath('//dg:DecisionGraph/dg:functions', **namespace):

      name = graph.xpath('//dg:name/text()', **namespace)[0]

      ros_topic = graph.xpath('.//Signals/option[@name="rosTopic"]/string')[0]

      ros_topic.text = '/decision_graphs/' + node_name + '/' + name

      map(lambda x: definitions.insert(0, x), copy.deepcopy(graph.getchildren()))

      graph.getparent().remove(graph)
  except Exception as e:
    pass

  return code, parameters
