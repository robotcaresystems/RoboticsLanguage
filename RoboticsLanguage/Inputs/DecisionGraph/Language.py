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
    '{dg}to': default,
    '{dg}name': default,
    '{dg}node': default,
    '{dg}case': default,
    '{dg}true': default,
    '{dg}false': default,
    '{dg}switch': default,
    '{dg}initial': default,
    '{dg}decision': default,
    '{dg}function': default,
    '{dg}sequence': default,
    '{dg}functions': default,
    '{dg}expression': default,
    '{dg}DecisionGraph': default,
    '{dg}decisionInLine': default,
}
