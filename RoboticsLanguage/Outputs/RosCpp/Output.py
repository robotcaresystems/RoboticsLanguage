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


def runPreparations(code, parameters):

  # save the node name for the templates
  parameters['node']['name'] = code.xpath('/node/option[@name="name"]/string')[0].text

  # find a file system safe name
  node_name_underscore = Utilities.underscore(parameters['node']['name'])

  # list of c++ libraries to include based on the existance of specific tags in the code
  include_libraries = {'Integers': 'cstdint',
                       'Strings': 'string'}

  # add only the required libraries
  for tag, library in include_libraries.iteritems():
    if len(code.xpath('//' + tag)) > 0:
      parameters['Outputs']['RosCpp']['globalIncludes'].add(library)

  return code, parameters, node_name_underscore


def output(code, parameters):

  # check if node tag is present
  if len(code.xpath('/node')) < 1:
    Utilities.logging.warning('No `node` element found. ROS C++ will not generate code!')
    return

  # preprocess the code to provide information for templares
  code, parameters, node_name_underscore = runPreparations(code, parameters)

  # run template engine to generate node code
  if not Utilities.templateEngine(code, parameters, {'nodename': node_name_underscore}, os.path.dirname(
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
