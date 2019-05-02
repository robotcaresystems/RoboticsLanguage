#
#   This is the Robotics Language compiler
#
#   Parameters.py: Definition of the parameters for this package
#
#   Created on: 08 March, 2019
#       Author: Gabriel Lopes
#      Licence: license
#    Copyright: copyright
#

import os
import sys
import shlex
import subprocess
from RoboticsLanguage.Base import Utilities
from RoboticsLanguage.Tools import Templates


def output(code, parameters):

  # save the node name for the templates
  parameters['node'] = {}
  parameters['node']['name'] = code.xpath('//fts:name/text()', namespaces={'fts': 'fts'})[0]

  # find a file system safe name
  node_name_underscore = Utilities.underscore(parameters['node']['name'])

  # get the path to deploy the code
  if 'FaultToleranceSystem' in parameters['globals']['deployOutputs'].keys():
    deploy_path = parameters['globals']['deployOutputs']['FaultToleranceSystem']
  else:
    deploy_path = parameters['globals']['deploy']

  # run template engine to generate node code
  if not Templates.templateEngine(code, parameters, file_patterns={'nodename': node_name_underscore}):
    sys.exit(1)

  # ############ compile code #####################################################
  # if the flag compile is set then run catkin
  if parameters['globals']['compile']:
    if parameters['Outputs']['RosCpp']['useColcon']:
      command = ['colcon', 'build', '--packages-select', node_name_underscore]
    else:
      command = ['catkin', 'build', node_name_underscore]

    Utilities.logging.debug("Compiling with: `" + ' '.join(command) + "` in folder " + deploy_path + '/..')
    process = subprocess.Popen(command, cwd=deploy_path +'/..')
    process.wait()

    if process.returncode > 0:
      Utilities.logging.error("Compilation failed!!!")

  # ############ run code #####################################################
  # if the flag launch is set then launch the node
  if parameters['globals']['launch']:

    # open HTML in different platforms
    if 'darwin' in sys.platform:
      launch_command = 'open'

    if 'linux' in sys.platform:
      launch_command = 'xdg-open'

    subprocess.Popen([launch_command, parameters['globals']['deploy'] + node_name_underscore + '/html/' + node_name_underscore + '_gui.html'])

    # # check if package is in the ros path
    package_location = (deploy_path + '/' + node_name_underscore).replace('//', '/')
    if package_location not in os.environ['ROS_PACKAGE_PATH']:
      os.environ['ROS_PACKAGE_PATH'] += ':' + package_location

    command = 'roslaunch ' + node_name_underscore + ' ' + node_name_underscore + '.launch'

    Utilities.logging.debug("launching: `" + command + '`')
    process = subprocess.Popen(shlex.split(command))
    process.wait()


  return 0
