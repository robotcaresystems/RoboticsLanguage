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

import dpath.util
from RoboticsLanguage.Base import Utilities


def transform(code, parameters):

  when_counter = 0

  for when in code.xpath('//when'):

    # give a unique id to each when clause
    when_counter = when_counter + 1
    when.attrib['whenId'] = str(when_counter)

    # look for all variable dependencies on the arguments
    variables = list(set(when.getchildren()[0].xpath('.//variable[not(ancestor::domain)]/@name|.//domain/variable[count(preceding-sibling::*)=0]/@name')))

    # also check for first element
    if when.getchildren()[0].tag == 'variable':
      variables.append(when.getchildren()[0].attrib['name'])

    for variable in variables:
      new_parameters = {}
      dpath.util.new(new_parameters, 'Transformers/Base/variables/' + variable +
                     '/operators/assign/post/Cpp', ['when' + str(when_counter) + '()'])
      dpath.util.merge(parameters, new_parameters)

  return code, parameters
