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

from RoboticsLanguage.Base.Types import manySameNumbersStrings, manySameNumbers, manySameNumbersStringsBooleans, anything, manySameBooleans
from RoboticsLanguage.Base.Types import returnSameArgumentType, returnNothing, returnBoolean

language = {

    # math
    'times': {
        'definition': {
            'argumentTypes': manySameNumbers,
            'returnType': returnSameArgumentType
        },
        'input': {
            'RoL': {
                'infix': {'key': '*',
                          'order': 1200,
                          'flat': True}
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
        'definition': {
            'argumentTypes': manySameNumbers,
            'returnType': returnSameArgumentType
        },
        'input': {
            'RoL': {
                'infix': {'key': '/',
                          'order': 1200,
                          'flat': True}
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
            'argumentTypes': manySameNumbersStrings,
            'returnType': returnSameArgumentType
        },
        'input': {
            'RoL': {
                'infix': {'key': '+',
                          'order': 1100,
                          'flat': True}
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
        'definition': {
            'argumentTypes': manySameNumbers,
            'returnType': returnSameArgumentType
        },
        'input': {
            'RoL': {
                'infix': {'key': '-',
                          'order': 1100,
                          'flat': True}
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
        'definition': {
            'argumentTypes': manySameNumbers,
            'returnType': returnBoolean
        },
        'input': {
            'RoL': {
                'infix': {'key': '>',
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
        'definition': {
            'argumentTypes': manySameNumbers,
            'returnType': returnBoolean
        },
        'input': {
            'RoL': {
                'infix': {'key': '<',
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
        'definition': {
            'argumentTypes': manySameNumbers,
            'returnType': returnBoolean
        },
        'input': {
            'RoL': {
                'infix': {'key': ['>=', '≥'],
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
        'definition': {
            'argumentTypes': manySameNumbers,
            'returnType': returnBoolean
        },
        'input': {
            'RoL': {
                'infix': {'key': ['<=', '≤'],
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
        'definition': {
            'argumentTypes': manySameNumbersStringsBooleans,
            'returnType': returnBoolean
        },
        'input': {
            'RoL': {
                'infix': {'key': ['==', '≡'],
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
        'definition': {
            'argumentTypes': manySameNumbersStringsBooleans,
            'returnType': returnBoolean
        },
        'input': {
            'RoL': {
                'infix': {'key': ['!=', '≠'],
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
        'definition': {
            'argumentTypes': manySameBooleans,
            'returnType': returnBoolean
        },
        'input': {
            'RoL': {
                'infix': {'key': ['and', '∧'],
                          'order': 600,
                          'flat': True}
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
        'definition': {
            'argumentTypes': manySameBooleans,
            'returnType': returnBoolean
        },
        'RoL': {
            'input': {
                'infix': {'key': ['or', '∨'],
                          'order': 400,
                          'flat': True}
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
        'definition': {
            'argumentTypes': anything,
            'returnType': returnNothing
        },
        'input': {
            'RoL': {
                'infix': {'key': '=',
                          'order': 100}
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
