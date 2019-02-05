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

    # math
    'times': {
        'definition': {
            'arguments': arguments('real real+'),
            'returns': returns('same')
        },
        'input': {
            'RoL': {
                'infix': {'key': '*',
                          'order': 1200,
                          'flat': True}
            }
        },
        'output': {
            'HTMLDocumentation': '({{children|join(" * ")}})',

        },
        'localisation':
        {
            'pt': 'multiplicar'
        },
        'documentation':
        {
            'title': 'Number multiplication',
            'description': 'Normal real, vector, or matrix multiplication. ',
            'usage': 'a = 2*3'
        }
    },
    'divide': {
        'definition': {
            'arguments': arguments('real real+'),
            'returns': returns('same')
        },
        'input': {
            'RoL': {
                'infix': {'key': '/',
                          'order': 1200,
                          'flat': True}
            }
        },
        'output': {
            'HTMLDocumentation': '({{children|join(" / ")}})',

        },
        'localisation':
        {
            'pt': 'dividir'
        },
    },

    'plus': {
        'definition': {
            'arguments': arguments('( real real+ | string string+)'),
            'returns': returns('same')
        },
        'input': {
            'RoL': {
                'infix': {'key': '+',
                          'order': 1100,
                          'flat': True}
            }
        },
        'output': {
            'HTMLDocumentation': '({{children|join(" + ")}})',

        },
        'localisation':
        {
            'pt': 'adicionar'
        },
    },
    'minus': {
        'definition': {
            'arguments': arguments('real real+'),
            'returns': returns('same')
        },
        'input': {
            'RoL': {
                'infix': {'key': '-',
                          'order': 1100,
                          'flat': True}
            }
        },
        'output': {
            'HTMLDocumentation': '({{children|join(" - ")}})',
        },
        'localisation':
        {
            'pt': 'subtrair'
        },
    },

    'larger': {
        'definition': {
            'arguments': arguments('real real'),
            'returns': returns('boolean')
        },
        'input': {
            'RoL': {
                'infix': {'key': '>',
                          'order': 800}
            }
        },
        'output': {
            'HTMLDocumentation': '({{children|join(" > ")}})',


        },
        'localisation':
        {
            'pt': 'maior'
        },
    },
    'smaller': {
        'definition': {
            'arguments': arguments('real real'),
            'returns': returns('boolean')
        },
        'input': {
            'RoL': {
                'infix': {'key': '<',
                          'order': 800}
            }
        },
        'output': {
            'HTMLDocumentation': '({{children|join(" < ")}})',


        },
        'localisation':
        {
            'pt': 'menor'
        },
    },
    'largerEqual': {
        'definition': {
            'arguments': arguments('real real'),
            'returns': returns('boolean')
        },
        'input': {
            'RoL': {
                'infix': {'key': ['>=', '≥'],
                          'order': 800}
            }
        },
        'output': {
            'HTMLDocumentation': '({{children|join(" ≥ ")}})',


        },
        'localisation':
        {
            'pt': 'maiorIgual'
        },
    },
    'smallerEqual': {
        'definition': {
            'arguments': arguments('real real'),
            'returns': returns('boolean')
        },
        'input': {
            'RoL': {
                'infix': {'key': ['<=', '≤'],
                          'order': 800}
            }
        },
        'output': {
            'HTMLDocumentation': '({{children|join(" ≤ ")}})',


        },
        'localisation':
        {
            'pt': 'menorIgual'
        },
    },

    'equal': {
        'definition': {
            'arguments': arguments('( real real | string string | boolean boolean )'),
            'returns': returns('boolean')
        },
        'input': {
            'RoL': {
                'infix': {'key': ['==', '≡'],
                          'order': 700}
            }
        },
        'output': {
            'HTMLDocumentation': '({{children|join(" ≡ ")}})',


        },
        'localisation':
        {
            'pt': 'igual'
        },
    },
    'notEqual': {
        'definition': {
            'arguments': arguments('( real real | string string | boolean boolean )'),
            'returns': returns('boolean')
        },
        'input': {
            'RoL': {
                'infix': {'key': ['!=', '≠'],
                          'order': 700}
            }
        },
        'output': {
            'HTMLDocumentation': '({{children|join(" ≠ ")}})',


        },
        'localisation':
        {
            'pt': 'diferente'
        },
    },


    'and': {
        'definition': {
            'arguments': arguments('boolean boolean+'),
            'returns': returns('boolean')
        },
        'input': {
            'RoL': {
                'infix': {'key': ['and', '∧'],
                          'order': 600,
                          'flat': True}
            }
        },
        'output': {
            'HTMLDocumentation': '({{children|join(" ∧ ")}})',


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
            'arguments': arguments('boolean boolean+'),
            'returns': returns('boolean')
        },
        'input': {
            'RoL': {
                'infix': {'key': ['or', '∨'],
                          'order': 400,
                          'flat': True}
            }
        },
        'output': {
            'HTMLDocumentation': '({{children|join(" ∨ ")}})',
        },
        'localisation':
        {
            'pt': {'prefix': 'ou', 'infix': ['ou', '∧']}
        },
    },
    'not': {
        'definition': {
            'arguments': arguments('boolean'),
            'returns': returns('boolean')
        },
        'input': {
            'RoL': {
                'prefix': {'key': '¬',
                           'order': 1300}
            }
        },
        'output': {
            'HTMLDocumentation': '¬({{children[0]}})',

        },
        'localisation':
        {
        },
    },

    'negative': {
        'definition': {
            'arguments': arguments('real'),
            'returns': returns('same')
        },
        'input': {
            'RoL': {
                'prefix': {'key': '-',
                           'order': 1300}
            }
        },
        'output': {
            'HTMLDocumentation': '-({{children[0]}})',

        },
        'localisation':
        {
            'pt': 'negativo'
        },
        'documentation':
        {
            'title': 'Number negation',
            'description': 'Normal real or variable negation. ',
            'usage': 'a = -b'
        }
    },

    'positive': {
        'definition': {
            'arguments': arguments('real'),
            'returns': returns('same')
        },
        'input': {
            'RoL': {
                'prefix': {'key': '+',
                           'order': 1300}
            }
        },
        'output': {
            'HTMLDocumentation': '({{children[0]}})',

        },
        'localisation':
        {
            'pt': 'positivo'
        },
        'documentation':
        {
            'title': 'Positive sign',
            'description': 'Has no effect on sign.',
            'usage': 'a = +b'
        }
    },

}
