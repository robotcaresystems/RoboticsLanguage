#
#   This is the Robotics Language compiler
#
#   Wizard.py: Setting up the parameters for this package automatically or with help
#
#   Created on: 29 October, 2019
#       Author: Gabriel A. D. Lopes
#      Licence: Apache 2.0
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
from RoboticsLanguage.Base import Utilities

def wizard(personalized_parameters, parameters):

  Utilities.logging.info('Running Base wizard...')

  personalized_parameters['Outputs'] = {}
  personalized_parameters['Inputs'] = {}
  personalized_parameters['Transformers'] = {}
  personalized_parameters['developer'] = {}
  personalized_parameters['globals'] = {}
  personalized_parameters['globals']['deploy'] = os.path.expanduser('~') + '/deploy/'

  return personalized_parameters, parameters
