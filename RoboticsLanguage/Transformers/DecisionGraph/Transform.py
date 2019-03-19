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

from lxml import etree
from RoboticsLanguage.Base import Utilities
from RoboticsLanguage.Inputs.RoL import Parse as RoL


def transform(code, parameters):
  namespace = {'namespaces': {'dg': 'dg'}}

  for graph in code.xpath('//dg:DecisionGraph', **namespace):
    name = graph.xpath('//dg:name/text()', **namespace)[0]

    node_name = Utilities.underscore(code.xpath(
        '/node/option[@name="name"]/string')[0].text)

    definitions = code.xpath('/node/option[@name="definitions"]/block')[0]

    rol_code, rol_parameters = RoL.parse(
        'expression(dg_' + name + '_publisher in Signals(Integers,rosTopic:"/' + node_name + '/' + name + '"))', parameters)

    definitions.insert(0, rol_code.getchildren()[0])

  return code, parameters
