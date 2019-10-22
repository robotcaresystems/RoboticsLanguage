#
#   This is the Robotics Language compiler
#
#   Transform.py: generic code transformer
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
import yaml
import json

from RoboticsLanguage.Base import Utilities
from RoboticsLanguage.Tools import Templates


def transform(code, parameters):
  Utilities.logging.info("Transforming generic...")

  yamlInput = parameters['Transformers']['Generic']['yamlInput']
  jsonInput = parameters['Transformers']['Generic']['jsonInput']
  templateFolder = parameters['Transformers']['Generic']['templateFolder']


  if yamlInput != '' or jsonInput != '':
      if templateFolder == '':
        print('Please provide a templates folder.\n\nUsage:\nrol --generic-yaml-input file.yaml --generic-template-folder path\n')
      else:
        if isinstance(parameters['globals']['output'], list):
          parameters['globals']['output'].append('Generic')
        else:
          parameters['globals']['output'] = [parameters['globals']['output'], 'Generic']


  if templateFolder != '' and yamlInput=='' and jsonInput=='':
        print('Please provide a generic yaml or json file.\n\nUsage:\nrol --generic-yaml-input file.yaml --generic-template-folder path\n')


  return code, parameters
