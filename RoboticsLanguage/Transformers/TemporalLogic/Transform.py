#
#   This is the Robotics Language compiler
#
#   Language.py: Parses the Robotics Language
#
#   Created on: June 22, 2017
#       Author: Gabriel A. D. Lopes
#      Licence: Apache 2.0
#    Copyright: 2014-2017 Robot Care Systems BV, The Hague, The Netherlands. All rights reserved.
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

import copy
import dpath.util
from lxml import etree
from RoboticsLanguage.Base import Utilities
from RoboticsLanguage.Tools import Serialise


def processTemporalOperators(code, parameters, logic_id_counter):
  # find all the relevant tags
  logics = code.xpath('.//always|.//eventually')

  # reverse the list. This ensures all the dependencies of cascated
  # operators are correct
  logics.reverse()

  for logic in logics:

    # find all the variables inside the temporal logic operator that affect
    # its behaviour
    all_variables = logic.xpath('.//variable[not(ancestor::domain)]/@name|.//domain/variable[count(preceding-sibling::*)=0]/@name')

    # also find all signal dependencies of cascated temporal logic
    # operators
    all_previous_variables = ','.join(logic.xpath(
        './/always/@temporalLogicVariables|.//eventually/@temporalLogicVariables'))

    # add all variables
    all_variables = all_variables + all_previous_variables.split(',')

    # remove duplicates and preserve order (just in case)
    all_variables = list(set(all_variables))

    # remove empty elements
    all_variables = filter(lambda x: x != '', all_variables)

    # fill information about logic operator
    logic_id_counter += 1
    logic_type = logic.tag

    # interval operator
    if len(logic.getchildren()) > 1:
      logic_type += 'Interval'

    # fill information about logic operator
    logic_name = logic_type + '_' + str(logic_id_counter) + '_'
    logic.attrib['temporalLogicId'] = str(logic_id_counter)
    logic.attrib['temporalLogicName'] = logic_name
    logic.attrib['temporalLogicVariables'] = ','.join(all_variables)

    # add logic update function to all variable involved in this operator
    for variable in all_variables:
      new_parameters = {}
      dpath.util.new(new_parameters, '/Transformers/Base/variables/' + variable + '/operators/assign/post/Cpp',
                     ['logic' + logic_type[0].title() + logic_type[1:] + str(logic_id_counter) + '()'])
      dpath.util.merge(parameters, new_parameters)

    # create text element for the GUI
    if 'HTMLGUI' in parameters['globals']['output']:

      # make a copy of the code to not polute it with extra attributes
      xml_copy = copy.deepcopy(logic)
      root = etree.Element("root")
      root.append(xml_copy)

      # use the RoL serialiser to create the text tag
      Serialise.serialise(root.getchildren()[0], parameters, parameters['language'], 'RoL')

      # annotate tag
      logic.attrib['temporalLogicText'] = root.getchildren()[0].attrib['RoL']

  return logic_id_counter


def transform(code, parameters):

  processTemporalOperators(code, parameters, 0)

  return code, parameters
