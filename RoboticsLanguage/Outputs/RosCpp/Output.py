#
#   This is the Robotics Language compiler
#
#   Output.py: Generates ROS c++ code
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

from RoboticsLanguage.Base import Utilities
import os
import sys
import subprocess
# import dpath.util

def output(code, parameters):

  if len(code.xpath('/node')) < 1:
    Utilities.logging.warning('No `node` element found. ROS C++ will not generate code!')
    return

  # get the node name
  node_name = Utilities.option(code.xpath('/node')[0],'name').text

  # save the name for the templates
  parameters['node']['name'] = node_name
  # @NOTE why is dpath not working?
  # dpath.util.set(parameters,'/node/name',node_name)

  # use the node name on the file patterns
  node_name_underscore = Utilities.underscore(node_name)
  filepatterns = {'nodename': node_name_underscore}

  # run template engine to generate node code
  if not Utilities.templateEngine(code, parameters, filepatterns, os.path.dirname(
      __file__) + '/templates', parameters['globals']['deploy']):
    sys.exit(1)

  # if the flag compile is set then run catkin
  if parameters['globals']['compile']:
    Utilities.logger.debug("Compiling with: `catkin build " + node_name_underscore +
                           "` in folder " + parameters['globals']['deploy'])
    process = subprocess.Popen(['catkin', 'build', node_name_underscore], cwd=parameters['globals']['deploy'])
    process.wait()
    if process.returncode > 0:
      Utilities.logger.error("Compilation failed!!!")

  # if the flag launch is set then launch the node
  if parameters['globals']['launch']:
    Utilities.logger.debug("launching: `roslaunch " + node_name_underscore + " " + node_name_underscore + '.launch`')
    process = subprocess.Popen(['roslaunch', node_name_underscore, node_name_underscore + '.launch'])

  return 0
