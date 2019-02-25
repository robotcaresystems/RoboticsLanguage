#
#   This is the Robotics Language compiler
#
#   Language.py: Definition of the language for this package
#
#   Created on: 25 February, 2019
#       Author: Gabriel Lopes
#      Licence: license
#    Copyright: Robot Care Systems BV
#

from RoboticsLanguage.Base.Types import arguments, optional, returns


language = {
    '{di}root': {
        'definition': {
            arguments: arguments('anything'),
            returns: returns('nothing')
        },
        'output': {
            'RosCpp': '',
            'RosPy': '# this is the root'
        }
    },
    '{di}name': {},
    '{di}network_input_channels': {},
    '{di}output_type': {},
    '{di}input_type': {},
    '{di}network_input_size': {},
    '{di}network_model': {},
    '{di}item': {},

}
