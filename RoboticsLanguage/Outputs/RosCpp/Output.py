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
from RoboticsLanguage.Tools import Templates

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

  # get the path to deploy the code
  if 'RosCpp' in parameters['globals']['deployOutputs'].keys():
    deploy_path = parameters['globals']['deployOutputs']['RosCpp']
  else:
    deploy_path = parameters['globals']['deploy']

  return code, parameters, node_name_underscore, deploy_path


def output(code, parameters):

  # ############ generate code #####################################################
  # check if node tag is present
  if len(code.xpath('/node')) < 1:
    Utilities.logging.warning('No `node` element found. ROS C++ will not generate code!')
    return

  # preprocess the code to provide information for templares
  code, parameters, node_name_underscore, deploy_path = runPreparations(code, parameters)

  # run template engine to generate node code
  if not Templates.templateEngine(code, parameters, file_patterns={'nodename': node_name_underscore}):
    sys.exit(1)

  # ############ create ros message if needed file if needed ############################################
  namespace = {'namespaces': {'rosm': 'rosm'}}

  messages = code.xpath('//rosm:message', **namespace)

  if len(messages) > 0:
    folder =  Utilities.myOutputPath(parameters) + '/' + node_name_underscore + '/msg'
    Utilities.createFolder(folder)

    for message in messages:
      name = message.xpath('.//rosm:name', **namespace)[0].text
      definition =  message.xpath('.//rosm:definition', **namespace)[0].text

      with open(folder + '/' + name + '.msg', 'w') as file:
        file.write(definition)

        Utilities.logging.debug('Wrote file ' + folder + '/' + name + '.msg ...')


  # ############ beautify code #####################################################
  # if the flag beautify is set then run uncrustify
  if parameters['globals']['beautify']:
    try:
      with open(os.devnull, 'w') as output_file:
        list_of_cpp_files = ['src/' + node_name_underscore + '.cpp',
                             'include/' + node_name_underscore + '/' + node_name_underscore + '.h']
        for file in list_of_cpp_files:
          process = subprocess.Popen(['uncrustify', '-c',  unicode(Utilities.myPluginPath(parameters) + '/Resources/uncrustify.cfg'),
                                      file,  '--replace', '--no-backup'],
                                     cwd=deploy_path + '/' + node_name_underscore,
                                     stdout=output_file,
                                     stderr=subprocess.STDOUT)
          process.wait()
          if process.returncode > 0:
            Utilities.logger.error("Error beautifying code. Uncrustify has returned an error.")
    except:
      # open HTML in different platforms
      if 'darwin' in sys.platform:
        Utilities.logger.error(
            "Error beautifying code. You may need to install uncrustify:\n\n  brew install uncrustify")

      if 'linux' in sys.platform:
        Utilities.logger.error(
            "Error beautifying code. You may need to install uncrustify:\n\n  sudo apt install uncrustify")

  # ############ compile code #####################################################
  # if the flag compile is set then run catkin
  if parameters['globals']['compile']:
    if parameters['Outputs']['RosCpp']['useColcon']:
      command = ['colcon', 'build', '--packages-select', node_name_underscore]
    else:
      command = ['catkin', 'build', node_name_underscore]

    Utilities.logger.debug("Compiling with: `" + ' '.join(command) + "` in folder " + deploy_path + '/..')
    process = subprocess.Popen(command, cwd=deploy_path +'/..')
    process.wait()

    if process.returncode > 0:
      Utilities.logger.error("Compilation failed!!!")

  # ############ run code #####################################################
  # if the flag launch is set then launch the node
  if parameters['globals']['launch']:
    Utilities.logger.debug("launching: `roslaunch " + node_name_underscore + " " + node_name_underscore + '.launch`')
    process = subprocess.Popen(['roslaunch', node_name_underscore, node_name_underscore + '.launch'])
    process.wait()

  return 0
