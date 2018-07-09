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

# @Utilities.cache
def prepareParameters():
  '''Collects parameters, language, messages, and error handling functions from all list_of_modules. This function is cached in `rol`. To refresh the cache run `rol --remove-cache`.'''

  # read the path
  language_path = os.path.dirname(__file__) + '/../../'

  # define initial classes of parameters
  manifesto = {'Inputs': {}, 'Outputs': {}, 'Transformers': {}}
  parameters = {'Inputs': {}, 'Outputs': {}, 'Transformers': {}}
  language = {}
  messages = {}
  command_line_flags = {}
  error_handling = {}
  error_exceptions = {}
  default_output = {}

  # load the parameters form all the modules dynamically
  for element in Utilities.findFileName('Manifesto.py', language_path):
    module_name = element.replace(language_path, '').replace('/Manifesto.py', '').replace('/', '.')

    # break the module name into pieces
    name_split = module_name.split('.')

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

      # The language
      try:
        language_module = __import__(module_name + '.Language', globals(), locals(), ['Language'])

        # append to each keyword in the language information from which package it comes from
        for keyword in language_module.language.keys():
          language_module.language[keyword]['package'] = name_split[1] + ':' + name_split[2]

        # append language definitions
        language = Utilities.mergeDictionaries(language, language_module.language)

        # read the default output for each language keyword per package
        if name_split[1] == 'Outputs':
          default_output[name_split[2]] = language_module.default_output
      except Exception as e:
        Utilities.logger.debug(e.__repr__())
        pass

      # The messages
      try:
        messages_module = __import__(module_name + '.Messages', globals(), locals(), ['Messages'])

        # append messages definitions
        messages = Utilities.mergeDictionaries(messages, messages_module.messages)
      except Exception as e:
        Utilities.logger.debug(e.__repr__())
        pass

      # The error handling functions
      try:
        error_module = __import__(module_name + '.ErrorHandling', globals(), locals(), ['ErrorHandling'])

        # append error handling definitions
        error_handling = Utilities.mergeDictionaries(error_handling, error_module.error_handling_functions)

        # append error exceptions definitions
        error_exceptions = Utilities.mergeDictionaries(error_exceptions, error_module.error_exception_functions)
      except Exception as e:
        Utilities.logger.debug(e.__repr__())
        pass

  # merge parameters collected from modules with the default system base parameters
  # At this point the default parameters and the module parameters should be jointly non-identical
  parameters = Utilities.mergeDictionaries(parameters, Parameters.parameters)

  # add package manifestos
  parameters['manifesto'] = manifesto

  # add package language definitions
  parameters['language'] = language

  # add package messages definitions
  parameters['messages'] = messages

  # add package error exceptions definitions
  parameters['errorExceptions'] = error_exceptions

  # add package error handling definitions
  parameters['errorHandling'] = error_handling

  # add command line options
  parameters['command_line_flags'] = Utilities.mergeDictionaries(
      command_line_flags, Parameters.command_line_flags)

  # fill in the languages using each outputs default language structure
  for keyword, value in parameters['language'].iteritems():
    # make sure the `output` tag is defined
    if 'output' in value.keys():
      # find missing outputs
      missing = list(set(parameters['Outputs'].keys()) - set(value['output'].keys()))
    else:
      # all outputs are missing
      missing = parameters['Outputs'].keys()
      parameters['language'][keyword]['output'] = {}

    parameters['language'][keyword]['defaultOutput'] = []
    for item in missing:
      # fill in the missing output
      parameters['language'][keyword]['output'][item] = default_output[item]
      # log that the default output is being used
      parameters['language'][keyword]['defaultOutput'].append(item)

  return parameters


def Initialise(remove_cache):
  '''The main initialisation file of `rol`. Grabs information from all modules to assemble a `parameters` dictionary.'''
  # remove cache if requested
  if remove_cache:
    Utilities.removeCache()

  # load cached parameters or create if necessary
  parameters = prepareParameters()

  return parameters
