#
#   This is the Robotics Language compiler
#
#   Parameters.py: Definition of the parameters for this package
#
#   Created on: 02 November, 2018
#       Author: Gabriel Lopes
#      Licence: license
#    Copyright: copyright
#

parameters = {'strict': False,
              'globalIncludes': set(),
              'localIncludes': set()
              }

command_line_flags = {
    'strict': {'suppress': True},
    'globalIncludes': {'suppress': True},
    'localIncludes': {'suppress': True}
}
