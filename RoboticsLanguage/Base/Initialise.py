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
import sys
import time
import signal
from . import Utilities
from . import Parameters

sys.setrecursionlimit(99999)


def exit_gracefully(*arguments):
  sys.exit(1)


signal.signal(signal.SIGINT, exit_gracefully)
signal.signal(signal.SIGTERM, exit_gracefully)


@Utilities.cache_in_disk
def prepareParameters():
  '''Collects parameters, language, messages, and error handling functions from all list_of_modules.
  This function is cached in `rol`. To refresh the cache run `rol --remove-cache`.'''

  # start by loading default parameters
  parameters = Parameters.parameters

  # add plugins folder to python path
  sys.path.append(parameters['globals']['plugins']+'/../')

  # define initial classes of parameters
  manifesto = {'Inputs': {}, 'Outputs': {}, 'Transformers': {}}
  parameters['Inputs'] = {}
  parameters['Outputs'] = {}
  parameters['Transformers'] = {}

  command_line_flags = {}

  package_order = {}

  # load the manifesto from all the modules
  for element in Utilities.findFileName('Manifesto.py', [parameters['globals']['RoboticsLanguagePath']+'/../', parameters['globals']['plugins']]):

    name_split = element.split('/')[-4:-1]
    module_name = '.'.join(name_split)

    if len(name_split) == 3 and name_split[1] in ['Inputs', 'Outputs', 'Transformers']:

      # The manifesto
      try:
        manifesto_module = __import__(module_name + '.Manifesto', globals(), locals(), ['Manifesto'])

        # read manifesto
        manifesto[name_split[1]][name_split[2]] = manifesto_module.manifesto

        # add path
        manifesto[name_split[1]][name_split[2]]['path'] = os.path.realpath(os.path.dirname(element))

        # add type: built-in or plugin
        manifesto[name_split[1]][name_split[2]]['type'] = name_split[0]

        # get the load order for the packages
        if 'order' in manifesto_module.manifesto.keys():
            package_order[module_name] = manifesto_module.manifesto['order']
        else:
          # Inputs are loaded first
          if name_split[1] == 'Inputs':
            package_order[module_name] = -1
          # outputs are loaded last
          elif name_split[1] == 'Outputs':
            package_order[module_name] = 100000000

      except Exception as e:
        Utilities.logger.debug(e.__repr__())
        pass

  # add package manifestos
  parameters['manifesto'] = manifesto

  # add the package load order
  parameters['globals']['loadOrder'] = sorted(package_order, key=package_order.get, reverse=False)

  # load the parameters form all the modules dynamically
  for module_name in parameters['globals']['loadOrder']:

    name_split = module_name.split('.')

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

  # add command line options
  parameters['command_line_flags'] = Utilities.mergeDictionaries(
      command_line_flags, Parameters.command_line_flags)

  return parameters


# @Utilities.time_all_calls
def Initialise(remove_cache):
  '''The main initialisation file of `rol`. Grabs information from all modules to assemble a `parameters` dictionary.'''

  # remove cache if requested
  if remove_cache:
    Utilities.removeCache()

  # load cached parameters or create if necessary
  parameters = prepareParameters()

  # add plugins folder to python path
  sys.path.append(parameters['globals']['plugins']+'/../')

  # remember approximate starting time
  parameters['developer']['progressStartTime'] = time.time()

  return parameters
