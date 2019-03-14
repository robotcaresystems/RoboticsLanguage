#
#   This is the Robotics Language compiler
#
#   Language.py: Definition of the language for this package
#
#   Created on: 11 March, 2019
#       Author: Gabriel Lopes
#      Licence: license
#    Copyright: Robot Care Systems BV
#

from RoboticsLanguage.Base.Types import arguments, returns

default = {
    'definition': {
        arguments: arguments('anything'),
        returns: returns('nothing')
    },
    'output': {
        'RosCpp': ''
    }
}

language = {
    '{dg}DecisionGraph': default,
    '{dg}initial': default,
    '{dg}decision': default,
    '{dg}decisionInLine': default,
    '{dg}switch': default,
    '{dg}case': default,
    '{dg}expression': default,
    '{dg}function': default,
    '{dg}sequence': default,
    '{dg}name': default,
    '{dg}true': default,
    '{dg}false': default,
    '{dg}to': default,
    '{dg}node': default,
}
