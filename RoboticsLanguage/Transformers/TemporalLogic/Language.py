# -*- coding: utf-8 -*-
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

from RoboticsLanguage.Base.Types import arguments, optional, returns

language = {

    'eventually': {
        'definition': {
            'arguments': arguments('(real real boolean | boolean)'),
            'returns': returns('boolean')
        },
        'input':
        {
            'RoL':
            {
                'alternatives': ['◇'],
                'generic': ['◇[', '](', ')']
            }
        },

        'output':
        {
            'RoL': '{% if children|length == 1 %}◇({{children[0]}}){% else %}◇[{{children[0]}},{{children[1]}}]({{children[2]}}){% endif %}',
            'RosCpp': '{{attributes["temporalLogicName"]}}'
        },
        'localisation':
        {
            'pt': 'eventualmente',
        }
    },

    'always': {
        'definition': {
            'arguments': arguments('(real real boolean | boolean)'),
            'returns': returns('boolean')
        },
        'input':
        {
            'RoL':
            {
                'alternatives': ['□'],
                'generic': ['□[', '](', ')']
            }
        },
        'output':
        {
            'RoL': '{% if children|length == 1 %}□({{children[0]}}){% else %}□[{{children[0]}},{{children[1]}}]({{children[2]}}){% endif %}',
            'RosCpp':  '{{attributes["temporalLogicName"]}}'
        },
        'localisation':
        {
            'pt': 'sempre',
        },
    }
}
