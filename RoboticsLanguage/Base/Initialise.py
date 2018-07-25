# -*- coding: utf-8 -*-
#
#   This is the Robotics Language compiler
#
#   Default Parameters.py: These are the default parameters that are passed to the compiler
#
#   Created on: February 8, 2018
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
from . import Utilities
from . import Parameters

@Utilities.cache
def prepareParameters():
  '''Collects parameters, language, messages, and error handling functions from all list_of_modules.
  This function is cached in `rol`. To refresh the cache run `rol --remove-cache`.'''

  # read the path
  language_path = os.path.abspath(os.path.dirname(__file__) + '/../../') + '/'

  # define initial classes of parameters
  manifesto = {'Inputs': {}, 'Outputs': {}, 'Transformers': {}}
  parameters = {'Inputs': {}, 'Outputs': {}, 'Transformers': {}}
  command_line_flags = {}

  # load the parameters form all the modules dynamically
  for element in Utilities.findFileName('Manifesto.py', language_path):

    name_split = element.split('/')[-4:-1]
    module_name = '.'.join(name_split)

    if len(name_split) == 3 and name_split[1] in ['Inputs', 'Outputs', 'Transformers']:

      # The manifesto
      try:
        manifesto_module = __import__(module_name + '.Manifesto', globals(), locals(), ['Manifesto'])

        # read manifesto
        manifesto[name_split[1]][name_split[2]] = manifesto_module.manifesto
      except Exception as e:
        Utilities.logger.debug(e.__repr__())
        pass

      # The parameters
      try:
        parameters_module = __import__(module_name + '.Parameters', globals(), locals(), ['Parameters'])

        # read parameters
        parameters[name_split[1]][name_split[2]] = parameters_module.parameters

        # read command_line_flags
        command_line = parameters_module.command_line_flags
        for key, value in command_line.iteritems():
          command_line_flags[name_split[1] + ':' + name_split[2] + ':' + key] = value
      except Exception as e:
        Utilities.logger.debug(e.__repr__())
        pass

  # merge parameters collected from modules with the default system base parameters
  # At this point the default parameters and the module parameters should be jointly non-identical
  parameters = Utilities.mergeDictionaries(parameters, Parameters.parameters)

  # add some globals information
  parameters['globals']['RoboticsLanguagePath'] = language_path + 'RoboticsLanguage/'

  # add package manifestos
  parameters['manifesto'] = manifesto

  # add command line options
  parameters['command_line_flags'] = Utilities.mergeDictionaries(
      command_line_flags, Parameters.command_line_flags)

  return parameters

@Utilities.time_all_calls
def Initialise(remove_cache):
  '''The main initialisation file of `rol`. Grabs information from all modules to assemble a `parameters` dictionary.'''
  # remove cache if requested
  if remove_cache:
    Utilities.removeCache()

  # load cached parameters or create if necessary
  parameters = prepareParameters()

  return parameters
