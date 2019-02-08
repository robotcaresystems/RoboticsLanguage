#
#   This is the Robotics Language compiler
#
#   Output.py: Generates HTML documentation
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

import os
import re
import sys
import subprocess
import dpath.util
from RoboticsLanguage.Base import Utilities
from RoboticsLanguage.Tools import Templates

ignored_files = ['.DS_Store']

include_template = """
{{% set {} %}}

{{% endset %}}
"""


@Utilities.cache_in_disk
def prepareGroups(parameters):
  '''group keyword by package'''
  groups = {}

  for keyword, value in parameters['language'].iteritems():
    group, module = tuple(value['package'].split(':'))
    if not Utilities.isDefined(groups, '/' + group + '/' + module):
      dpath.util.new(groups, '/' + group + '/' + module, [])

    groups[group][module].append(keyword)

  return groups


def output(code, parameters):

  if parameters['Outputs']['Developer']['create']['reference']:

    groups = prepareGroups(parameters)

    parameters['documentation'] = {'groups': groups}

    # run template engine to generate code API
    if not Templates.templateEngine(code, parameters,
                                    templates_path=os.path.dirname(__file__) + '/Templates/Documentation'):
      sys.exit(1)

  paths = [parameters['globals']['RoboticsLanguagePath'], parameters['globals']['plugins']]

  outputs = parameters['Outputs'].keys()

  for type in ['Inputs', 'InputsJSON', 'InputsYAML', 'InputsXML', 'Transformers', 'Outputs']:
    if parameters['Outputs']['Developer']['create'][type] is not '':

      module_type = type.replace('JSON', '').replace('XML', '').replace('YAML', '')

      parameters['Outputs']['Developer']['Info'] = {'type': module_type,
                                                    'name': parameters['Outputs']['Developer']['create'][type]}

      filepatterns = {'name': Utilities.camelCase(parameters['Outputs']['Developer']['create'][type])}

      # @UPDATE to use latest template engine
      # run template engine to generate node code
      if not Templates.templateEngine(code, parameters,
                                      file_patterns=filepatterns,
                                      templates_path=os.path.dirname(__file__) + '/Templates/' + type,
                                      deploy_path=parameters['globals']['plugins'] + '/' + module_type):
        sys.exit(1)

      # make sure the path ~/.rol/plugins containts an __init__.py file
      try:
        subprocess.call(['touch', parameters['globals']['plugins'] + '/__init__.py'])
      except:
        pass

      # create template code elements for transformers
      if type == 'Transformers':
        for output in outputs:

          # traverse all the output template folders
          for path in paths:
            for root, dirs, files in os.walk(path + '/Outputs/' + output + '/Templates'):
              for file in files:
                if file not in ignored_files:
                  with open(os.path.join(root, file), 'r') as input_file:
                    text = input_file.read()

                    # look for include tags in the templates, e.g. "<<<'initialise'|group>>>"
                    result = re.findall('<<<\'([^\']*)[^>>>]*>>>', text)
                    if len(result) > 0:

                      # create an copy of the file with includes,
                      # e.g. "{% set initialise %} {% endset %}"
                      file_name = parameters['globals']['plugins'] + '/' + type + '/' + filepatterns['name'] + '/' + os.path.join(
                          root, file).replace(path + '/Outputs/' + output + '/Templates', 'Templates/Outputs/' + output)
                      # create folder if needed for new file
                      Utilities.createFolderForFile(file_name)

                      # save the new template file
                      with open(file_name, 'w') as output_file:
                        for element in result:
                          output_file.write(include_template.format(element))
                        Utilities.logger.debug('Wrote file ' + file_name)

      print('Created ' + module_type + ' plugin "' + filepatterns['name'] + '" in folder ' +
            parameters['globals']['plugins'] + '/' + module_type + '/' + filepatterns['name'])

      # clean cache in disk
      Utilities.removeCache()

  return 0
