#
#   This is the Robotics Language compiler
#
#   CommandLine.py: Process command line arguments
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

import argcomplete
import argparse
import os
import yaml
import sys

from . import Parameters
from . import Utilities

# paths to be searched automatically for parameters
parameters_home_file = '.rol/parameters.yaml'
parameters_local_file = ['.rol.parameters.yaml', 'rol.parameters.yaml']


def generateArgparseArguments(parameters, flags):
  flat = Utilities.flatDictionary(parameters)
  arguments = {}
  command_line_flags = {}

  for key, value in flat.iteritems():
    special_key = key.replace('-', ':')[1:]
    arguments[special_key] = {}
    arguments[special_key]['dest'] = key

    command_line_flags[special_key] = ['-' + str(key)]

    arguments[special_key]['default'] = None  # value

    if special_key in flags.keys():

      if Utilities.isKeyDefined('longFlag', flags[special_key]):
        command_line_flags[special_key] = ['--' + flags[special_key]['longFlag']]

      if Utilities.isKeyDefined('flag', flags[special_key]):
        command_line_flags[special_key].insert(0, '-' + flags[special_key]['flag'])

      if Utilities.isKeyDefined('numberArguments', flags[special_key]):
        arguments[special_key]['nargs'] = flags[special_key]['numberArguments']

      if Utilities.isKeyDefined('noArgument', flags[special_key]):
        if flags[special_key]['noArgument']:
          if value is False:
            arguments[special_key]['action'] = 'store_true'
          else:
            arguments[special_key]['action'] = 'store_false'
      else:
        arguments[special_key]['type'] = type(value)
        arguments[special_key]['metavar'] = str(type(value).__name__.upper())

      if Utilities.isKeyDefined('description', flags[special_key]):
        arguments[special_key]['help'] = flags[special_key]['description']

      if Utilities.isKeyDefined('choices', flags[special_key]):
        arguments[special_key]['choices'] = flags[special_key]['choices']

      if Utilities.isKeyDefined('suppress', flags[special_key]):
        if flags[special_key]['suppress']:
          arguments.pop(special_key)
          command_line_flags.pop(special_key)

    else:
      arguments[special_key]['type'] = type(value)
      arguments[special_key]['metavar'] = str(type(value).__name__.upper())

  return command_line_flags, arguments


def prepareCommandLineArguments(parameters):

  # remember the available choices for outputs
  Parameters.command_line_flags['globals:output']['choices'] = parameters['manifesto']['Outputs'].keys()
  # create a subset of all the parameters
  subset = dict((x, parameters[x]) for x in ['Information', 'Transformers', 'Inputs', 'Outputs', 'globals', 'debug'])

  # create argparse list parameters
  flags, arguments = generateArgparseArguments(subset, parameters['command_line_flags'])

  # get all file formats
  file_formats = []
  file_package_name = []
  for key, value in parameters['manifesto']['Inputs'].iteritems():

    # @TODO Add support to multiple file extensions per format

    # the file extension
    file_formats.append(value['fileFormat'])

    # the description of the file type
    file_package_name.append(value['fileFormat'] + ': ' + value['packageName'] + ' file format')

  # parameter files are always YAML
  file_package_name.append('yaml: optional parameter files; \n')

  return flags, arguments, file_package_name, file_formats


def runCommandLineParser(parameters, arguments, flags, file_formats, file_package_name, command_line_arguments):
    # instantiate the command line parser
  parser = argparse.ArgumentParser(prog='rol', description='Robotics Language compiler',
                                   formatter_class=argparse.RawTextHelpFormatter)

  # divide parameters by groups
  groups = {}
  for key in sorted(parameters):
    groups[key] = parser.add_argument_group(key.lower())

  # add arguments to argparse
  for key in sorted(arguments):
    groups[key.split(':')[0]].add_argument(*flags[key], **arguments[key])

  # the files to process
  parser.add_argument('filename',
                      metavar='[ ' + ' | '.join(map(lambda x: 'file.' + x, file_formats)) + ' ] [ profile.yaml ... ]',
                      type=argparse.FileType('r'),
                      nargs='+',
                      # default=sys.stdin,
                      help=';\n'.join(file_package_name))

  # run the command line parser with autocomplete
  argcomplete.autocomplete(parser)
  args = parser.parse_args(command_line_arguments[1:])
  return parser, args


def processFileParameters(args, file_formats):
  # Check file types
  rol_files = []
  parameter_files = []
  unknown_files = []
  for element in args.filename:
    name, extension = os.path.splitext(os.path.abspath(element.name))
    if extension.lower() in map(lambda x: '.' + x.lower(), file_formats):
      # it is a RoL file
      rol_files.append({'file': element, 'name': name + extension, 'type': extension[1:]})
    elif extension.lower() in ['.yaml', '.yml']:
      # it is a parameter file
      parameter_files.append({'file': element, 'name': name + extension})
    else:
      # it is unknown
      unknown_files.append(name + extension)

  # return an error if files are unknown
  if len(unknown_files) > 0:
    Utilities.logger.error('the following files have unknown formal: ' + str(unknown_files))
    sys.exit(1)

  if len(rol_files) == 0:
    Utilities.logger.error('no Robotics Language files detected!')
    sys.exit(1)
    # @TODO: implement multiple file support
  elif len(rol_files) > 1:
    # @BUG if two files are repeated the message is displayed
    Utilities.logger.warn('the following files are disregarded:\n' + '\n'.join([x['name'] for x in rol_files[1:]]))

  # @NOTE: this is loading all YAML files for all the ROL files supplied in the command line. This is meant for
  # a later implementation that supports for processing multiple rol files simultaneously. Must separate local
  # parameters for each RoL file.

  # look for global parameter files in the local path
  for rol_file in rol_files:
    path, name = os.path.split(rol_file['name'])
    for local in parameters_local_file:
      local_file = path + '/' + local
      if os.path.isfile(local_file):
        parameter_files.insert(0, {'file': open(local_file, 'r'), 'name': local_file})

  # look for the global parameter file in the home path
  home_file = os.path.expanduser('~') + '/' + parameters_home_file
  if os.path.isfile(home_file):
    parameter_files.insert(0, {'file': open(home_file, 'r'), 'name': home_file})

  return rol_files, parameter_files


def processCommandLineParameters(args, file_formats, parameters):
  # select only the parameters that are referenced in the command line
  command_line_parameters_flat = {}
  for key, value in vars(args).iteritems():
    if value is not None:
      command_line_parameters_flat[key] = value

  # unflatten list of parameters into a dictionary
  command_line_parameters = Utilities.unflatDictionary(command_line_parameters_flat)

  # set debug level
  if Utilities.isDefined(command_line_parameters, '/globals/verbose'):
    Utilities.setLoggerLevel(command_line_parameters['globals']['verbose'])

  # check for files parameters
  rol_files, parameter_files = processFileParameters(args, file_formats)

  # now concatenate all parameters starting with
  # 1. defaults from RoL and from modules (can be cached)
  # 2. ~/.rol/parameters.yaml
  # 3. local rol.parameters.yaml
  # 4. list of yaml files passed as arguments
  # 5. command line parameters
  for parameter_file in parameter_files:
    parameters = Utilities.mergeDictionaries(yaml.load(parameter_file['file']), parameters)

  # merge the command line flags
  parameters = Utilities.mergeDictionaries(command_line_parameters, parameters)

  # close files opened by argparse
  for openfile in parameters['filename']:
    openfile.close()

  # remove filename key
  parameters.pop('filename', None)

  return rol_files[0]['name'], rol_files[0]['type'], Utilities.ensureList(parameters['globals']['output']), parameters


def ProcessArguments(command_line_parameters, parameters):

  # load cached command line flags or create if necessary
  flags, arguments, file_package_name, file_formats = Utilities.cache(
      'command_line_parameters', lambda: prepareCommandLineArguments(parameters))

  # @NOTE: 'file_package_name' and 'file_formats' should be one thing right?
  #         Also why : 'yaml: optional parameter files; \n'? What 's with the '; \n'

  # run the command line parser
  parser, args = runCommandLineParser(parameters, arguments, flags, file_formats,
                                      file_package_name, command_line_parameters)

  # process the parameters
  file_name, file_type, outputs, parameters = processCommandLineParameters(args, file_formats, parameters)

  return file_name, file_type, outputs, parameters
