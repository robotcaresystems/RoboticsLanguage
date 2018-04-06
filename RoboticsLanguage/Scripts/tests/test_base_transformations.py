#!/usr/bin/python
#
#   This is the Robotics Language compiler
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

import unittest
from lxml import etree
from RoboticsLanguage.Base import Transformations
from RoboticsLanguage.Base.Types import singleString, manyStrings, anything


# =================================================================================================
#  Base Transformations
# =================================================================================================

class TestBaseTransformations(unittest.TestCase):

  def test_Apply(self):

    xml = etree.fromstring('<node><print><string>hello</string></print></node>')

    parameters = {
        'text': 'node(print("hello"))',
        'errors': [],
        'debug': {'parameters': False,
                  'stepCounter': 0,
                  'step': 0,
                  'ignoreSemanticErrors': False
                  },
        'manifesto': {
                'Transformers': {
                    'Base': {
                        'order': 0,
                        'packageName': 'Base',
                        'packageShortName': 'base'
                    }
                }
        },
        'globals': {
            'output': ['RoL', 'RosCpp']
        },
        'language': {
            'string': {
                'output': {
                    'RosCpp': '"{{text}}"',
                    'RoL': '"{{text}}"',
                }
            },
            'node': {
                'definition': {
                    'optionalArguments': {'name': singleString},
                    'optionalDefaults': {'name': 'unnamed'},
                    'argumentTypes': anything,
                    'returnType': lambda x: 'Nothing'
                },
            },
            'print': {
                'definition': {
                    'optionalArguments': {'level': singleString},
                    'optionalDefaults': {'level': 'info'},
                    'argumentTypes': manyStrings,
                    'returnType': lambda x: 'block'
                },
                'output':  {
                    'RosCpp': 'ROS_INFO({{children|first}})',
                    'RoL': 'print({{children|first}})',
                }
            },
            'option': {
                'output': {
                    'RosCpp': '"{{text}}"',
                    'RoL': '"{{text}}"',
                },
                'documentation':
                {
                }
            },
            'name': {
                'output': {
                    'RosCpp': '"{{text}}"',
                    'RoL': '"{{text}}"',
                },
                'documentation':
                {
                }
            }
        }
    }

    xml_code, parameters = Transformations.Apply(xml, parameters)

    self.assertEqual(etree.tostring(xml_code),
                     '<node type="Nothing"><print type="block" RoL="print(&quot;hello&quot;)" RosCpp="ROS_INFO(&quot;hello&quot;)"><string type="Strings" RoL="&quot;hello&quot;" RosCpp="&quot;hello&quot;">hello</string><option name="level" RoL="&quot;&quot;" RosCpp="&quot;&quot;"><string type="Strings" RoL="&quot;info&quot;" RosCpp="&quot;info&quot;">info</string></option></print><option name="name" RoL="&quot;&quot;" RosCpp="&quot;&quot;"><string type="Strings" RoL="&quot;unnamed&quot;" RosCpp="&quot;unnamed&quot;">unnamed</string></option></node>')


if __name__ == '__main__':
  unittest.main()
