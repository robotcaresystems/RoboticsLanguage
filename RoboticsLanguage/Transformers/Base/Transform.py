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

from RoboticsLanguage.Base import Utilities


def CreateTypeList(code, parameters):
  parameters['Transformers']['Base']['types'] = {}

  return code, parameters


def CreateVariableList(code, parameters):
  parameters['Transformers']['Base']['variables'] = {}

  for variable in code.xpath('/node/option[@name="definitions"]/*//element/variable'):
    parameters['Transformers']['Base']['variables'][variable.attrib['name']] = {'definition': variable.getparent().getchildren()[1]}

  return code, parameters


def CreateFunctionList(code, parameters):
  parameters['Transformers']['Base']['functions'] = {}

  for function in code.xpath('/node/option[@name="definitions"]/*//function_definition'):
    parameters['Transformers']['Base']['functions'][function.attrib['name']] = {'definition': function }

  return code, parameters




def transform(code, parameters):

  # fill in defaults in optional arguments
  code, parameters = Utilities.fillDefaultsInOptionalArguments(code, parameters)

  code, parameters = CreateTypeList(code, parameters)

  code, parameters = CreateVariableList(code, parameters)

  code, parameters = CreateFunctionList(code, parameters)


  return code, parameters
