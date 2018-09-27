# -*- coding: utf-8 -*-
#
#   This is the Robotics Language compiler
#
#   Language.py: Definitions of the base language
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

    #######################################################################
    # Atomic types

    'string': {
        'localisation':
        {
            'pt': 'texto'
        },
        'documentation':
        {
        }
    },

    'integer': {
        'localisation':
        {
            'pt': 'inteiro'
        },
        'documentation':
        {
        }
    },

    'natural': {
        'localisation':
        {
            'pt': 'natural'
        },
        'documentation':
        {
        }
    },

    'boolean': {
        'localisation':
        {
        },
        'documentation':
        {
        }
    },

    'real': {
        'localisation':
        {
            'pt': 'real'
        },
        'documentation':
        {
        }
    },

    #######################################################################
    # Sets


    'Reals': {
        'definition': {
            'arguments': arguments('none'),
            'optional': {
                'bits': optional('natural', 32),
            },
            'returns': returns('real')
        },
        'localisation':
        {
            'pt': 'real'
        },
        'documentation':
        {
            'title': 'Real numbers type',
            'description': 'A type representing real numbers. Assumptions on the number of bits used by the compiler to represent a real number is given as information in the editor.',
            'usage': 'x in Reals'
        }
    },

    'Integers': {
        'definition': {
            'arguments': arguments('none'),
            'optional': {
                'bits': optional('natural', 32),
            },
            'returns': returns('integer')
        },
        'localisation':
        {
            'pt': 'inteiro'
        },
        'documentation':
        {
            'title': 'Integer numbers type',
            'description': 'A type representing integer numbers. Assumptions on the number of bits used by the compiler to represent an integer number is given as information in the editor.',
            'usage': 'x in Integers'
        }
    },

    'Naturals': {
        'definition': {
            'arguments': arguments('none'),
            'optional': {
                'bits': optional('natural', 32),
            },
            'returns': returns('natural')
        },
        'localisation':
        {
            'pt': 'natural'
        },
        'documentation':
        {
            'title': 'Natural numbers type',
            'description': 'A type representing natural numbers. Assumptions on the number of bits used by the compiler to represent an natural number is given as information in the editor.',
            'usage': 'x in Naturals'
        }
    },

    'Strings': {
        'definition': {
            'arguments': arguments('none'),
            'returns': returns('string')
        },
        'localisation':
        {
            'pt': 'texto'
        },
        'documentation':
        {
        }
    },

    'Booleans': {
        'definition': {
            'arguments': arguments('none'),
            'returns': returns('boolean')
        },
        'localisation':
        {
            'pt': 'boleano'
        },
        'documentation':
        {
        }
    },

    'Signals': {
        'definition': {
            'arguments': arguments('real | integer | natural | string | boolean'),
            'optional': {
                'onChange': optional('anything', ''),
                'onNew': optional('anything', '')
            },
            'returns': returns('same')
        },
        'localisation':
        {
            'pt': 'sinal'
        },
        'documentation':
        {
            'title': 'A time or event based signal',
            'description': 'Defines a signal type.',
            'usage': 'x in Signals(Reals,onNew:print(x))'
        }
    },



    #######################################################################
    # Language structural elements

    'option': {
        'definition': {
            'arguments': arguments('anything'),
            'returns': returns('same')
        },
        'localisation':
        {
            'pt': 'parâmetro'
        },
        'documentation':
        {
        }
    },

    'anything': {
        'definition': {
            'arguments': arguments('anything'),
            'returns': returns('none')
        },
    },


    'block': {
        'definition': {
            'arguments': arguments('anything'),
            'returns': returns('block')
        },
    },

    #######################################################################
    # Base functions


    'node': {
        'definition': {
            'arguments': arguments('anything'),
            'optional': {
                'rate': optional('real', 25),
                'name': optional('string', 'unnamed'),
                'initialise': optional('anything', None),
                'finalise': optional('anything', None),
                'definitions': optional('anything', None),
            },
            'returns': returns('node')
        },
        'localisation':
        {
            'pt': 'nó',
            'el': 'κόμβος'
        },
        'documentation':
        {
            'title': 'The main software node',
            'description': 'This is the main RoL node. Definitions, initialisation, events, etc., are defined here.',
            'usage': 'node(\n  name:"hello world",\n  initialise(print("hello world"))\n)'
        }
    },
    'print': {
        'definition': {
            'arguments': arguments('(string | real)+'),
            'optional': {'level': optional('string', 'info')},
            'returns': returns('none')
        },
        'localisation':
        {
            'pt': 'imprimir',
            'el': 'εκτύπωσε',
            'nl': 'afdrukken'
        },
        'documentation':
        {
        }
    },


    'assign': {
        'definition': {
            'arguments': arguments('(real real | string string | element real | element string)'),
            'returns': returns('none')
        },
        'input': {
            'RoL': {
                'infix': {'key': '=',
                          'order': 100}
            }
        },
        'localisation':
        {
            'pt': 'atribuir'
        },

    },

    'element': {
        'definition': {
            'arguments': arguments('anything'),
            'returns': returns('element')
        },
        'localisation':
        {
            'pt': 'elemento'
        },
        'documentation':
        {
            'title': 'Element of a set of type',
            'description': 'Defines a variable to be an element of a set or a type. If a set is provided, then the variable takes the type of the elements of the set',
            'usage': 'x in Reals'
        }
    },

    'variable': {
        'test': 'sdfsdf',
        'definition': {
            'arguments': arguments('none'),
            'returns': returns('none')
        },
        'localisation':
        {
            'pt': 'variável'
        },
        'documentation':
        {
        }
    },

    'function': {
        'definition': {
            'arguments': arguments('anything'),
            'returns': returns('none')
        },
        'documentation':
        {
        }
    },


    'function_pointer': {
        'definition': {
            'arguments': arguments('anything'),
            'returns': returns('function')
        },
        'documentation':
        {
        }
    },


    'return': {
        'definition': {
            'arguments': arguments('anything'),
            'returns': returns('same')
        },
        'localisation':
        {
        },
        'documentation':
        {
        }
    },

    'function_definition': {
        'definition': {
            'arguments': arguments("arguments{0,1} returns{0,1} content"),
            'returns': returns('none')
        },
        'documentation':
        {
        }
    },

    'function_arguments': {
        'definition': {
            'arguments': arguments('anything'),
            'returns': returns('arguments')
        },
        'documentation':
        {
        }
    },

    'function_content': {
        'definition': {
            'arguments': arguments('anything'),
            'returns': returns('content')
        },
        'documentation':
        {
        }
    },

    'function_returns': {
        'definition': {
            'arguments': arguments('anything'),
            'returns': returns('returns')
        },
        'documentation':
        {
        }
    },
    'set': {
        'definition': {
            'arguments': arguments('anything'),
            'returns': returns('set')
        },
        'localisation':
        {
            'pt': 'conjunto'
        },
        'documentation':
        {
        }
    },

    'if': {
        'definition': {
            'arguments': arguments('boolean anything anything'),
            'returns': returns('none')
        },

    },

    'part': {
        'definition': {
            'arguments': arguments('anything'),
            'returns': returns('none')
        },
        'documentation':
        {
        }
    },

    'index': {
        'definition': {
            'arguments': arguments('anything'),
            'returns': returns('none')
        },
        'documentation':
        {
        }
    },

    'domain': {
        'definition': {
            'arguments': arguments('anything'),
            'returns': returns('none')
        },
        'documentation':
        {
        }
    },


}

#
# 'vector': {
#     'localisation':
#     {
#         'pt': 'vector'
#     },
#     'documentation':
#     {
#     }
# },
#
#
# 'associativeArray': {
#     'localisation':
#     {
#     },
#     'documentation':
#     {
#         'title': 'Set',
#         'description': 'A set of values',
#         'usage': 'a = { b, c ,d }'
#     }
# },
#
#
#
#
#
# 'defineFunction': {
#     'definition': {
#         'argumentTypes': anything,
#         'returnType': returnNothing
#     },
#     'localisation':
#     {
#     },
#     'documentation':
#     {
#     }
# },
#
# 'block': {
#     'definition': {
#         'argumentTypes': anything,
#         'returnType': returnCodeBlock
#     },
#     'localisation':
#     {
#     },
#     'documentation':
#     {
#     }
# },
#
# 'anything': {
#     'definition': {
#         'argumentTypes': anything,
#         'returnType': returnNothing
#     },
#     'localisation':
#     {
#     },
#     'documentation':
#     {
#     }
# },

#
# 'cycle': {
#     'output':
#     {
#         'HTMLDocumentation': '{{children|first}}',
#         'HTMLGUI': '{{children|first}}',
#         'RoL': '{{children|first}}',
#     },
#     'localisation':
#     {
#         'pt': 'repetir'
#     },
#     'documentation':
#     {
#     }
# },
#
# 'events': {
#     'localisation':
#     {
#         'pt': 'eventos'
#     },
#     'documentation':
#     {
#     }
# },
#
# 'Event': {
#     'localisation':
#     {
#         'pt': 'eventos'
#     },
#     'documentation':
#     {
#     }
# },
#
# 'Time': {
#     'localisation':
#     {
#         'pt': 'eventos'
#     },
#     'documentation':
#     {
#     }
# },

# 'if': {
#     'localisation':
#     {
#         'pt': 'se',
#     },
#     'documentation':
#     {
#     }
# },
