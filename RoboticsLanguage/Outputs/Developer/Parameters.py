#
#   This is the Robotics Language compiler
#
#   Parameters.py: Defines the parameters for this package
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


parameters = {
    'create': {
        'Inputs': '',
        'InputsYAML': '',
        'InputsJSON': '',
        'InputsXML': '',
        'Transformers': '',
        'Outputs': '',
        'reference': False
    }
}

command_line_flags = {
    'create:Inputs':
        {
            'longFlag': 'create-input-template',
            'description': 'Create a template for an Input module',
            'fileNotNeeded': True
        },
    'create:InputsJSON':
        {
            'longFlag': 'create-input-json-template',
            'description': 'Create a template for a JSON Input module',
            'fileNotNeeded': True
        },
    'create:InputsYAML':
        {
            'longFlag': 'create-input-yaml-template',
            'description': 'Create a template for a YAML Input module',
            'fileNotNeeded': True
        },
    'create:InputsXML':
        {
            'longFlag': 'create-input-xml-template',
            'description': 'Create a template for a XML Input module',
            'fileNotNeeded': True
        },
    'create:Transformers':
        {
            'longFlag': 'create-transformer-template',
            'description': 'Create a template for a Transformer module',
            'fileNotNeeded': True
        },
    'create:Outputs':
        {
            'longFlag': 'create-output-template',
            'description': 'Create a template for an Output module',
            'fileNotNeeded': True
        },
    'create:reference':
        {
            'longFlag': 'create-reference-documentation',
            'description': 'Creates the Reference Documentation for the Robotics Language',
            'fileNotNeeded': True,
            'noArgument': True
        }


}
