#
#   This is the Robotics Language compiler
#
#   Parameters.py: Definition of the parameters for this package
#
#   Created on: 31 July, 2018
#       Author: Gabriel Lopes
#      Licence: license
#    Copyright: copyright
#

parameters = {
    'ignoreSemanticErrors': True
}

command_line_flags = {
    'ignoreSemanticErrors': {
        'longFlag': 'ignore-semantic-errors',
        'noArgument': True,
        'description': 'Ignores the semantic errors and attempts to generate code. Result may not compile.'
    },
}
