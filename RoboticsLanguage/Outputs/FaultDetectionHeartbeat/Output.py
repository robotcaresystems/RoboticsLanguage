#
#   This is the Robotics Language compiler
#
#   Parameters.py: Definition of the parameters for this package
#
#   Created on: 19 February, 2019
#       Author: Gabriel Lopes
#      Licence: license
#    Copyright: copyright
#


import sys
import subprocess
from RoboticsLanguage.Base import Utilities
from RoboticsLanguage.Tools import Templates


def output(code, parameters):
  # save the node name for the templates
  parameters['node']['name'] = code.xpath('/node/option[@name="name"]/string')[0].text

  # find a file system safe name
  node_name_underscore = Utilities.underscore(parameters['node']['name'])

  # run template engine to generate node code
  if not Templates.templateEngine(code, parameters, file_patterns={'nodename': node_name_underscore}):
    sys.exit(1)


  print parameters['globals']['deploy'] + node_name_underscore + '/html/' + node_name_underscore + '_fault_detection_heartbeat_gui.html'

  # ############ launching code #####################################################
  # if the flag launch is set then launch the node
  if parameters['globals']['launch']:
    # open HTML in different platforms
    if 'darwin' in sys.platform:
      launch_command = 'open'

    if 'linux' in sys.platform:
      launch_command = 'xdg-open'

    subprocess.Popen([launch_command, parameters['globals']['deploy'] + node_name_underscore + '/html/' + node_name_underscore + '_fault_detection_heartbeat_gui.html'])

  return 0
