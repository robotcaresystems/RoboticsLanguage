#
#   This is the Robotics Language compiler
#
#   Parameters.py: Definition of the parameters for this package
#
#   Created on: 22 October, 2019
#       Author: Gabriel Lopes
#      Licence: Apache 2.0
#    Copyright: Gabriel Lopes
#
#   Licensed under the Apache License, Version 2.0 (the "License"); you may not use
#   this file except in compliance with the License. You may obtain a copy of the
#   License at http://www.apache.org/licenses/LICENSE-2.0 Unless required by
#   applicable law or agreed to in writing, software distributed under the License
#   is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
#   KIND, either express or implied. See the License for the specific language
#   governing permissions and limitations under the License.
#
import os
import yaml
import json
from RoboticsLanguage.Base import Utilities
from RoboticsLanguage.Tools import Templates
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

def output(code, parameters):
  Utilities.logging.info("Output generic...")

  yamlInput = parameters['Transformers']['Generic']['yamlInput']
  jsonInput = parameters['Transformers']['Generic']['jsonInput']
  templateFolder = parameters['Transformers']['Generic']['templateFolder']

  if templateFolder[0] !='/':
    templateFolder = os.getcwd() + '/' + templateFolder


  if yamlInput != '':
      try:
        with open(yamlInput, 'r') as file:
          parameters['data'] = yaml.load(file.read(), Loader=Loader)

      except Exception as e:
        print('Error reading file: ' + yamlInput)
        print(e)


      if 'file_patterns' in parameters['data'].keys():
        file_patterns = parameters['data']['file_patterns']
      else:
        file_patterns = {}

      # run template engine to generate code API
      if not Templates.templateEngine(code, parameters,
                                      file_patterns=file_patterns,
                                      templates_path=templateFolder):
        print('Error creating object from templates folder: '+ templateFolder)

  if jsonInput != '':
      try:
        with open(jsonInput, 'r') as file:
          parameters['data'] = json.load(file.read())

      except Exception as e:
        print('Error reading file: ' + jsonInput)
        print(e)


      if 'file_patterns' in parameters['data'].keys():
        file_patterns = parameters['data']['file_patters']
      else:
        file_patterns = {}


      # run template engine to generate code API
      if not Templates.templateEngine(code, parameters,
                                      file_patterns=file_patterns,
                                      templates_path=templateFolder):
        print('Error creating object from templates folder: '+ templateFolder)


  return 0
