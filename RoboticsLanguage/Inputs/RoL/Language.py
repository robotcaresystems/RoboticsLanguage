# -*- coding: utf-8 -*-
#
#   This is the Robotics Language compiler
#
#   Language.py: Definition of the language for this package
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

language = {
    # base types
    'Reals': {
        'input':
        {
            'RoL':
            {
                'alternatives': ['ℝ']
            }
        },
    },

    'Integers': {
        'input':
        {
            'RoL':
            {
                'alternatives': ['ℤ']
            }
        },
    },

    'Naturals': {
        'input':
        {
            'RoL':
            {
                'alternatives': ['ℕ']
            }
        },
    },

    'Booleans': {
        'input':
        {
            'RoL':
            {
                'alternatives': ['𝔹']
            }
        },
    },

    'vector': {
        'input': {
            'RoL': {
                'bracket': {'open': '[',
                            'close': ']',
                            'arguments': 'values'}
            }
        },
    },

    'set': {
        'input': {
            'RoL': {
                'bracket': {'open': '{',
                            'close': '}',
                            'arguments': 'values'}
            }
        },
    },

    'associativeArray': {
        'input': {
            'RoL': {
                'bracket': {'open': '{',
                            'close': '}',
                            'arguments': 'keyValues'}
            }
        },
    },

    'element': {
        'input': {
            'RoL': {
                'infix': {'key': ['in', '∈'],
                          'order': 150}
            }
        },
    },
    'domain': {
        'input': {
            'RoL': {
                'infix': {'key': '.',
                          'order': 1400,
                          'flat': True}
            }
        },
    },
}
