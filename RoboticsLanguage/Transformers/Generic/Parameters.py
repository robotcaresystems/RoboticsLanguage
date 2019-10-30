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

parameters = {
  'yamlInput':'',
  'jsonInput':'',
  'templateFolder':''
}

command_line_flags = {
    'yamlInput':
        {
            'longFlag': 'generic-yaml-input',
            'description': 'Use the data of a generic yaml file to populate a template',
            'fileNotNeeded': True
        },
    'jsonInput':
        {
            'longFlag': 'generic-json-input',
            'description': 'Use the data of a generic json file to populate a template',
            'fileNotNeeded': True
        },
    'templateFolder':
        {
            'longFlag': 'generic-template-folder',
            'description': 'Template forder used by generic yaml or json inputs',
            'fileNotNeeded': True
        }
}
