#
#   This is the Robotics Language compiler
#
#   Parameters.py: Definition of the parameters for this package
#
#   Created on: 11 July, 2018
#       Author: Gabriel Lopes
#      Licence: license
#    Copyright: copyright
#
from RoboticsLanguage.Base.Types import arguments, optional, returns

language = {
    'FiniteStateMachine': {
        'definition': {
            'arguments': arguments('initial transitions'),
            'returns': returns('none')
        },
    },
    'initial': {
        'definition': {
            'arguments': arguments('none'),
            'returns': returns('initial')
        },
    },
    'transitions': {
        'definition': {
            'arguments': arguments('transition+'),
            'returns': returns('transitions')
        },
    },
    'transition': {
        'definition': {
            'arguments': arguments('label begin end'),
            'returns': returns('transition')
        },
    },
    'label': {
        'definition': {
            'arguments': arguments('none'),
            'returns': returns('label')
        },

    },
    'begin': {
        'definition': {
            'arguments': arguments('none'),
            'returns': returns('begin')
        },
    },
    'end': {
        'definition': {
            'arguments': arguments('none'),
            'returns': returns('end')
        },
    }




}
