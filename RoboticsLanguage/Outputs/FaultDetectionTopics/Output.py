#
#   This is the Robotics Language compiler
#
#   Parameters.py: Definition of the parameters for this package
#
#   Created on: 12 February, 2019
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

  # ############ launching code #####################################################
  # if the flag launch is set then launch the node
  if parameters['globals']['launch']:
    # open HTML in different platforms
    if 'darwin' in sys.platform:
      launch_command = 'open'

    if 'linux' in sys.platform:
      launch_command = 'xdg-open'

    subprocess.Popen([launch_command, parameters['globals']['deploy'] + node_name_underscore + '/html/' + node_name_underscore + '_fault_detection_topics_gui.html'])

  return 0
