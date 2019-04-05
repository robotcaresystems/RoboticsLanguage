#
#   This is the Robotics Language compiler
#
#   Parameters.py: Definition of the parameters for this package
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
import os
from . import Tools

parameters = {
    'globalIncludes': set(),
    'localIncludes': set(),
    'useColcon': False,
    'deploy':  os.path.expanduser('~') + '/catkin_ws/src/',
}

command_line_flags = {
    'globalIncludes': {'suppress': True},
    'localIncludes': {'suppress': True},
    'useColcon': {
        'longFlag': 'use-colcon-cpp',
        'noArgument': True,
        'description': 'Use the colcon system instead of catkin'
    },
    'deploy': {
        'longFlag': 'deploy-ros-cpp-path',
        'description': 'The path where the generated ROS code is saved'
    }
}

wizard = {
    'deploy': {
        'question': 'What is the folder of your ROS workspace?',
        'showDefault': True,
        'defaultFunction': Tools.findROSWorkspace,
    }
}
