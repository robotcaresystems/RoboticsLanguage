#
#   This is the Robotics Language compiler
#
#   Parameters.py: Definition of the parameters for this package
#
#   Created on: 08 October, 2018
#       Author: Gabriel Lopes
#      Licence: license
#    Copyright: copyright
#
import os

parameters = {
    'globalIncludes': set(),
    'localIncludes': set(),
    'deploy': os.path.expanduser('~') + '/ros2_ws/src/'
}

command_line_flags = {
    'globalIncludes': {'suppress': True},
    'localIncludes': {'suppress': True},
    'deploy': {
        'longFlag': 'deploy-ros-2-cpp-path',
        'description': 'The path where the generated ROS 2 code is saved'
    }
}
