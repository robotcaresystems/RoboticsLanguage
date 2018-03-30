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

from RoboticsLanguage.Base.Types import manySameNumbersOrStrings
from RoboticsLanguage.Base.Types import returnSameArgumentType

language = {

    # math
    'times': {
        'input': {
            'RoL': {
                'infix': {'key':'*',
                          'order': 1000,
                          'flat':True}
            }
        },
        'output': {
            'RosCpp': '({{children|join(" * ")}})',
            'HTMLDocumentation': '({{children|join(" * ")}})',
            'RoL': '({{children|join(" * ")}})',
        },
        'localisation':
        {
            'pt': 'multiplicar'
        },
        'documentation':
        {
            'title': 'Number multiplication',
            'description': 'Normal number, vector, or matrix multiplication. ',
            'usage': 'a = 2*3'
        }
    },
    'divide': {
        'input': {
            'RoL': {
                'infix': {'key':'/',
                'order': 1000,
                'flat':True}
            }
        },
        'output': {
            'RosCpp': '({{children|join(" / ")}})',
            'HTMLDocumentation': '({{children|join(" / ")}})',
            'RoL': '({{children|join(" / ")}})',
        },
        'localisation':
        {
            'pt': 'dividir'
        },
    },

    'plus': {
        'definition': {
            'argumentTypes': manySameNumbersOrStrings,
            'returnType': returnSameArgumentType
        },
        'input': {
            'RoL': {
                'infix': {'key':'+',
                'order': 900,
                'flat':True}
            }
        },
        'output': {
            'RosCpp': '({{children|join(" + ")}})',
            'HTMLDocumentation': 'print({{children|join(" + ")}})',
            'HTMLGUI': '',
            'RoL': 'print({{children|join(" + ")}})',
        },
        'localisation':
        {
            'pt': 'adicionar'
        },
    },
    'minus': {
        'input': {
            'RoL': {
                'infix': {'key':'-',
                'order': 900,
                'flat':True}
            }
        },
        'output': {
            'RosCpp': '({{children|join(" - ")}})',
            'HTMLDocumentation': 'print({{children|join(" - ")}})',
            'HTMLGUI': '',
            'RoL': 'print({{children|join(" - ")}})',
        },
        'localisation':
        {
            'pt': 'subtrair'
        },
    },

    'larger': {
        'input': {
            'RoL': {
                'infix': {'key':'>',
                'order': 800}
            }
        },
        'output': {
            'RosCpp': '({{children|join(" > ")}})',
            'HTMLDocumentation': 'print({{children|join(" > ")}})',
            'HTMLGUI': '',
            'RoL': 'print({{children|join(" > ")}})',
        },
        'localisation':
        {
            'pt': 'maior'
        },
    },
    'smaller': {
        'input': {
            'RoL': {
                'infix': {'key':'<',
                'order': 800}
            }
        },
        'output': {
            'RosCpp': '({{children|join(" < ")}})',
            'HTMLDocumentation': 'print({{children|join(" < ")}})',
            'HTMLGUI': '',
            'RoL': 'print({{children|join(" < ")}})',
        },
        'localisation':
        {
            'pt': 'menor'
        },
    },
    'largerEqual': {
        'input': {
            'RoL': {
                'infix': {'key':['>=', '≥'],
                'order': 800}
            }
        },
        'output': {
            'RosCpp': '({{children|join(" >= ")}})',
            'HTMLDocumentation': 'print({{children|join(" ≥ ")}})',
            'HTMLGUI': '',
            'RoL': 'print({{children|join(" ≥ ")}})',
        },
        'localisation':
        {
            'pt': 'maiorIgual'
        },
    },
    'smallerEqual': {
        'input': {
            'RoL': {
                'infix': {'key':['<=', '≤'],
                'order': 800}
            }
        },
        'output': {
            'RosCpp': '({{children|join(" <= ")}})',
            'HTMLDocumentation': 'print({{children|join(" ≤ ")}})',
            'HTMLGUI': '',
            'RoL': 'print({{children|join(" ≤ ")}})',
        },
        'localisation':
        {
            'pt': 'menorIgual'
        },
    },

    'equal': {
        'input': {
            'RoL': {
                'infix': {'key':['==', '≡'],
                'order': 700}
            }
        },
        'output': {
            'RosCpp': '({{children|join(" == ")}})',
            'HTMLDocumentation': 'print({{children|join(" ≡ ")}})',
            'HTMLGUI': '',
            'RoL': 'print({{children|join(" ≡ ")}})',
        },
        'localisation':
        {
            'pt': 'igual'
        },
    },
    'notEqual': {
        'input': {
            'RoL': {
                'infix': {'key':['!=', '≠'],
                'order': 700}
            }
        },
        'output': {
            'RosCpp': '({{children|join(" != ")}})',
            'HTMLDocumentation': 'print({{children|join(" ≠ ")}})',
            'HTMLGUI': '',
            'RoL': 'print({{children|join(" ≠ ")}})',
        },
        'localisation':
        {
            'pt': 'diferente'
        },
    },


    'and': {
        'input': {
            'RoL': {
                'infix': {'key':['and', '∧'],
                'order': 600,
                'flat':True}
            }
        },
        'output': {
            'RosCpp': '({{children|join(" && ")}})',
            'HTMLDocumentation': 'print({{children|join(" ∧ ")}})',
            'HTMLGUI': '',
            'RoL': 'print({{children|join(" ∧ ")}})',
        },
        'localisation':
        {
            'pt': 'e'
        },
        'documentation':
        {
            'title': 'Logical `and` operator',
            'description': 'Is the logical AND function. It evaluates its arguments in order, giving False immediately if any of them are False, and True if they are all True. ',
            'usage': 'a = b and c'
        }
    },
    'or': {
        'RoL': {
            'input': {
                'infix': {'key':['or', '∨'],
                'order': 600,
                'flat':True}
            }
        },
        'output': {
            'RosCpp': '({{children|join(" || ")}})',
            'HTMLDocumentation': 'print({{children|join(" ∨ ")}})',
            'HTMLGUI': '',
            'RoL': 'print({{children|join(" ∨ ")}})',
        },
        'localisation':
        {
            'pt': {'prefix': 'ou', 'infix': ['ou', '∧']}
        },
    },
    'assign': {
        'input': {
            'RoL': {
                'infix': {'key':'=',
                'order': 500}
            }
        },
        'output': {
            'RosCpp': '{{children|join(" = ")}}',
            'HTMLDocumentation': 'print({{children|join(" = ")}})',
            'HTMLGUI': '',
            'RoL': 'print({{children|join(" = ")}})',
        },
        'localisation':
        {
            'pt': 'atribuir'
        },

    }
}
