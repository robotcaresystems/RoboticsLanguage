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
import stat
import autopep8
from RoboticsLanguage.Base import Utilities
from RoboticsLanguage.Tools import Templates


def output(code, parameters):

  deploy_path = parameters['globals']['deploy']

  # ############ code generation #####################################################

  # save the node name for the templates
  parameters['node']['name'] = code.xpath('/node/option[@name="name"]/string')[0].text

  # find a file system safe name
  node_name_underscore = Utilities.underscore(parameters['node']['name'])

  # run template engine to generate code
  if not Templates.templateEngine(code, parameters, file_patterns={'nodename': node_name_underscore}):
    sys.exit(1)

  # ############ Indentation #####################################################
  # Make sure indentation is respected
  python_file = deploy_path + '/' + node_name_underscore + '/scripts/' + node_name_underscore + '.py'

  # show indentation marks
  if parameters['Outputs']['RosPy']['showPythonIndentationMarks']:
    with open(python_file, 'r') as file:
      Utilities.printSource(file.read(), 'python', parameters)

  # precess indentation marks
  indent = 0
  indent_step = 4
  python_text = ''
  with open(python_file, 'r') as file:
    for line in file:
      clean_line = line.strip()
      if clean_line == '#>>':
        indent = indent + indent_step
        continue
      if clean_line == '#<<':
        indent = indent - indent_step
        continue
      python_text += ' '*indent + clean_line + '\n'

  # beautify
  if parameters['globals']['beautify']:
    python_text = autopep8.fix_code(python_text)

  # save the main script
  with open(python_file, 'w') as file:
    file.write(python_text)

  # make sure the python script is executable
  st = os.stat(python_file)
  os.chmod(python_file, st.st_mode | stat.S_IEXEC)

  return 0
