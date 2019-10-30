#
#   This is the Robotics Language compiler
#
#   Wizard.py: Setting up the parameters for this package automatically or with help
#
#   Created on: 29 October, 2019
#       Author: Gabriel A. D. Lopes
#      Licence: Apache 2.0
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
from RoboticsLanguage.Base import Utilities

def wizard(personalized_parameters, parameters):

  Utilities.logging.info('Running RosCpp wizard...')

  # check of colcon or katkin are available
  # python 3.3: shutil.which()
  import distutils.spawn

  # find executables
  catkin_available = distutils.spawn.find_executable("catkin") is not None
  colcon_available = distutils.spawn.find_executable("colcon") is not None
  roscore_available = distutils.spawn.find_executable("roscore") is not None

  personalized_parameters['Outputs']['RosCpp'] = {}

  # only post message if ros is installed
  if roscore_available and not catkin_available and not colcon_available:
    print("Warning: catkin and colcon not found!")

  if catkin_available:
    personalized_parameters['Outputs']['RosCpp']['rosBuildingEngine'] = 'catkin'

  # default to the more modern colcon
  if colcon_available:
    personalized_parameters['Outputs']['RosCpp']['rosBuildingEngine'] = 'colcon'

  return personalized_parameters, parameters
