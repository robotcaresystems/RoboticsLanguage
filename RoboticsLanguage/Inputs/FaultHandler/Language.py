#
#   This is the Robotics Language compiler
#
#   Language.py: Definition of the language for this package
#
#   Created on: 05 March, 2019
#       Author: Gabriel Lopes
#      Licence: license
#    Copyright: copyright
#

from RoboticsLanguage.Base.Types import arguments, returns

language = {
    '{fh}root': {
        'output': {
            'Cpp': '{{children|join("\n")}}'
        }
    },
    '{fh}item': {
        'output': {
            'Cpp': '{{children|join("\n")}}'
        }
    },
    '{fh}node': {
        'output': {
            'Cpp': 'void node_{{text}}_callback(){ {{children|join("\n")}} }'
        }
    },
    '{fh}action': {'output': {'Cpp': ''}},
    '{fh}if': {'output': {'Cpp': ''}},
    '{fh}faults': {'output': {'Cpp': ''}},
    '{fh}on_fault': {'output': {'Cpp': ''}},
    '{fh}conditions': {'output': {'Cpp': ''}},
    '{fh}condition': {'output': {'Cpp': ''}},
    '{fh}on_fail': {'output': {'Cpp': ''}},
    '{fh}retry': {'output': {'Cpp': ''}},
    '{fh}script': {'output': {'Cpp': ''}},
    '{fh}then': {'output': {'Cpp': ''}},
    '{fh}timeout': {'output': {'Cpp': ''}},
    '{fh}command': {'output': {'Cpp': ''}},
    '{fh}else': {'output': {'Cpp': ''}},
    '{fh}failure': {'output': {'Cpp': ''}},
    '{fh}name': {'output': {'Cpp': ''}},
    '{fh}fault': {'output': {'Cpp': ''}},




}
