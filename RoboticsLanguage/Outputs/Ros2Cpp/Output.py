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


import sys
from RoboticsLanguage.Base import Utilities
from RoboticsLanguage.Tools import Templates

def output(code, parameters):
  Utilities.logging.info("Output Ros 2 cpp...")

  # save the node name for the templates
  parameters['node']['name'] = code.xpath('/node/option[@name="name"]/string')[0].text

  # find a file system safe name
  node_name_underscore = Utilities.underscore(parameters['node']['name'])

  # run template engine to generate code
  if not Templates.templateEngine(code, parameters, file_patterns={'nodename': node_name_underscore}):
    sys.exit(1)

  return 0
