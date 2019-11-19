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

import os
import sys
import subprocess
from RoboticsLanguage.Base import Utilities
from RoboticsLanguage.Tools import Templates

def output(code, parameters):

  # save the node name for the templates
  parameters['node']['name'] = code.xpath('/node/option[@name="name"]/string')[0].text

  # find a file system safe name
  node_name_underscore = Utilities.underscore(parameters['node']['name'])

  deploy_path = parameters['globals']['deploy']

  # ############ generate code #####################################################

  # run template engine to generate node code
  if not Templates.templateEngine(code, parameters, file_patterns={'nodename': node_name_underscore}):
    sys.exit(1)

  # ############ compile #####################################################

  # if the flag compile is set then run catkin
  if parameters['globals']['compile']:
    command = ['make']
    folder = deploy_path + '/' + node_name_underscore

    Utilities.logging.debug("Compiling with: `" + ' '.join(command) + "` in folder " + folder)
    process = subprocess.Popen(command, cwd=folder)
    process.wait()

    if process.returncode > 0:
      Utilities.logging.error("Compilation failed!!!")

  # ############ run code #####################################################
  # if the flag launch is set then launch the node
  if parameters['globals']['launch']:

    command = ['./' + node_name_underscore]
    folder = os.path.join(deploy_path , node_name_underscore , 'build')

    Utilities.logging.debug("Running command `" + ' '.join(command) + "` in folder " + folder)
    try:
      process = subprocess.Popen(command, cwd=folder)
      process.wait()
    except Exception as e:
      print(e)



  return 0
