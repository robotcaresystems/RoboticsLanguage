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


parameters = {
    'addingNewMessages': False,
    'topicDefinitions': [],
    'buildDependencies': set(),
    'runDependencies': set(),
    'messageDependencies': set(),
    'distribution': '',
    'useSimulationTime': False
}

command_line_flags = {
    'addingNewMessages': {'suppress': True},
    'topicDefinitions': {'suppress': True},
    'buildDependencies': {'suppress': True},
    'runDependencies': {'suppress': True},
    'messageDependencies': {'suppress': True},
    'distribution': {'suppress': True},
    'useSimulationTime': {
        'longFlag': 'ros-use-simulation-time',
        'noArgument': True,
        'description': 'Uses simulation clock in ROS'
    },

}
