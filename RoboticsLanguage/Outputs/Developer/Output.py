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
import sys
from RoboticsLanguage.Base import Utilities
import dpath.util

@Utilities.cache
def prepareGroups(parameters):
    '''group keyword by package'''
    groups = {}

    for keyword, value in parameters['language'].iteritems():
      group, module = tuple(value['package'].split(':'))
      if not Utilities.isDefined(groups, '/'+group+'/'+module):
        dpath.util.new(groups,'/'+group+'/'+module,[])

      groups[group][module].append(keyword)

    return groups

def output(code, parameters):

  if parameters['Outputs']['Developer']['create']['reference']:

    groups = prepareGroups(parameters)

    parameters['memory']['documentation']={'groups': groups }

    # run template engine to generate code API
    if not Utilities.templateEngine(code,parameters,{},
                             os.path.dirname(__file__)+'/templates/Documentation/Reference',
                             parameters['globals']['deploy']):
      sys.exit(1)

  for type in ['input','output','transformer']:
    if parameters['Outputs']['Developer']['create'][type] is not '':
      filepatterns = {'name':Utilities.camelCase(parameters['Outputs']['Developer']['create'][type])}

      # run template engine to generate node code
      if not Utilities.templateEngine(code,parameters,
                               filepatterns,os.path.dirname(__file__)+'/templates/'+type.title(),
                               parameters['globals']['deploy']):
        sys.exit(1)

  return 0
