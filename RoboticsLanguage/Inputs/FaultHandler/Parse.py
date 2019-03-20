#
#   This is the Robotics Language compiler
#
#   Parse.py: Parses the  language
#
#   Created on: 11 February, 2019
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
import os
import yaml
from jinja2 import Template
from RoboticsLanguage.Base import Utilities
from RoboticsLanguage.Inputs.RoL import Parse as RoL


def parse(text, parameters):

  # parse JSON into dictionary
  text_dictionary = yaml.safe_load(text)

  # save the data in the parameters to be used by the GUI
  parameters['Inputs']['FaultHandler']['data'] = text_dictionary

  # print
  if parameters['Inputs']['FaultHandler']['showYAML']:
    Utilities.printParameters(text_dictionary, parameters)

  try:
    # open template file
    with open(os.path.dirname(os.path.realpath(__file__)) + '/Support/fault_handler.rol.template', 'r') as file:
      template = Template(file.read())

    # render the template with the data
    rol_code = template.render(text=text_dictionary)

    # print
    if parameters['Inputs']['FaultHandler']['showRol']:
      Utilities.printSource(rol_code, 'coffeescript', parameters)

    # parse generated rol code
    code, parameters = RoL.parse('block(' + rol_code + ')', parameters)
  except Exception as e:
    print e

  if parameters['Inputs']['FaultHandler']['showXML']:
    Utilities.printCode(code, parameters)

  return code, parameters
