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

import os
import sys
import yaml
import glob
import shutil
import argparse
import dpath.util
import argcomplete
from copy import copy
from . import Utilities
from . import Parameters

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


@Utilities.cache_in_disk
def prepareCommandLineArguments(parameters):

  # remember the available choices for outputs
  Parameters.command_line_flags['globals:output']['choices'] = parameters['manifesto']['Outputs'].keys()
  Parameters.command_line_flags['globals:input']['choices'] = parameters['manifesto']['Inputs'].keys()
  Parameters.command_line_flags['globals:setEnvironment']['choices'] = sum([ x.keys() for x in dpath.util.values(parameters,'manifesto/*/*/environments')],[])

  # create a subset of all the parameters
  subset = dict((x, parameters[x])
                for x in ['Information', 'Transformers', 'Inputs', 'Outputs', 'globals', 'developer'])

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

  try:
    # get a list of flags where a file is not needed
    list_of_no_file_needed_flags = reduce(lambda a, b: a + b, [flags[x] for x in dpath.util.search(
        parameters, 'command_line_flags/*/fileNotNeeded')['command_line_flags'].keys()])
  except:
    list_of_no_file_needed_flags = []

  # if one of the flags that does not require a file is used than change argparse
  if any([x in list_of_no_file_needed_flags for x in sys.argv]):
    nargs = '*'
    parameters['globals']['fileNeeded'] = False
  else:
    nargs = '+'
    parameters['globals']['fileNeeded'] = True

  # the files to process
  parser.add_argument('filename',
                      metavar='[ ' + ' | '.join(map(lambda x: 'file.' + x, file_formats)) + ' ] [ profile.yaml ... ]',
                      type=argparse.FileType('r'),
                      nargs=nargs,
                      # default=sys.stdin,
                      help=';\n'.join(file_package_name))

  # run the command line parser with autocomplete
  argcomplete.autocomplete(parser)
  args = parser.parse_args(command_line_arguments[1:])

  return parser, args


def processFileParameters(args, file_formats, parameters):
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
    Utilities.logging.error('the following files have unknown formal: ' + str(unknown_files))
    sys.exit(1)

  if len(rol_files) == 0 and parameters['globals']['fileNeeded']:
    Utilities.logging.error('no Robotics Language files detected!')
    sys.exit(1)
    # @TODO: implement multiple file support
  elif len(rol_files) > 1:
    # @BUG if two files are repeated the message is displayed
    Utilities.logging.warn('the following files are disregarded:\n' + '\n'.join([x['name'] for x in rol_files[1:]]))

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
    first_time = False
  else:
    first_time = True

  return rol_files, parameter_files, first_time


def runAllWizards(personalized_parameters, parameters):

  for module_name in parameters['globals']['loadOrder']:

    name_split = module_name.split('.')

    # The parameters
    try:
      wizard_module = __import__(module_name + '.Wizard', globals(), locals(), ['Wizard'])

      # run wizard function
      personalized_parameters, parameters = wizard_module.wizard(personalized_parameters, parameters)

    except Exception as e:
      Utilities.logging.debug(e.__repr__())
      pass

  return personalized_parameters, parameters




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
  rol_files, parameter_files, first_time = processFileParameters(args, file_formats, parameters)

  # now concatenate all parameters starting with
  # 1. defaults from RoL and from modules (can be cached)
  # 2. ~/.rol/parameters.yaml
  # 3. local rol.parameters.yaml
  # 4. list of yaml files passed as arguments
  # 5. command line parameters
  for parameter_file in parameter_files:
    parameters = Utilities.mergeDictionaries(yaml.safe_load(parameter_file['file']), parameters)

  # merge the command line flags
  parameters = Utilities.mergeDictionaries(command_line_parameters, parameters)

  # close files opened by argparse
  for openfile in parameters['filename']:
    openfile.close()

  # remove filename key
  parameters.pop('filename', None)

  parameters['globals']['output'] = Utilities.ensureList(parameters['globals']['output'])

  # Set the total number of plugins being processed
  parameters['developer']['progressTotal'] = 1 + \
      len(parameters['manifesto']['Transformers']) + len(parameters['globals']['output'])

  # on the first time
  if first_time:
    personalized_parameters, parameters = runAllWizards({}, parameters)

    # create rol folder and parameters file
    Utilities.createFolder(os.path.expanduser('~/.rol'))
    with open(os.path.expanduser('~/.rol/parameters.yaml'), 'w') as output:
      yaml.dump(personalized_parameters, output, default_flow_style=False)

    # warn the user
    Utilities.logging.warning('Created parameters file "~/.rol/parameters.yaml".')

    # remember if it is the first time the script is executed
    parameters['globals']['firstTime'] = personalized_parameters

  if len(rol_files) == 0:
    return None, None, parameters
  else:
    return rol_files[0]['name'], rol_files[0]['type'], parameters


# @NOTE for speed should we `try/catch` or check first?
def getTemplateTextForOutputPackage(parameters, keyword, package):
  if package in parameters['language'][keyword]['output'].keys():
    return parameters['language'][keyword]['output'][package], package
  elif 'parent' in parameters['manifesto']['Outputs'][package].keys():
    return getTemplateTextForOutputPackage(parameters, keyword, parameters['manifesto']['Outputs'][package]['parent'])
  else:
    raise


def loadRemainingParameters(parameters):

  language = {}
  messages = {}
  error_handling = {}
  error_exceptions = {}
  default_output = {}

  # load the parameters form all the modules dynamically
  # When this function is executed the plugins folder has already
  # been added to the path
  for module_name in parameters['globals']['loadOrder']:

    name_split = module_name.split('.')

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
      Utilities.logging.debug(e.__repr__())
      pass

    # The messages
    try:
      messages_module = __import__(module_name + '.Messages', globals(), locals(), ['Messages'])

      # append messages definitions
      messages = Utilities.mergeDictionaries(messages, messages_module.messages)
    except Exception as e:
      Utilities.logging.debug(e.__repr__())
      pass

    # The error handling functions
    try:
      error_module = __import__(module_name + '.ErrorHandling', globals(), locals(), ['ErrorHandling'])

      # append error handling definitions
      error_handling = Utilities.mergeDictionaries(error_handling, error_module.error_handling_functions)

      # append error exceptions definitions
      error_exceptions = Utilities.mergeDictionaries(error_exceptions, error_module.error_exception_functions)
    except Exception as e:
      Utilities.logging.debug(e.__repr__())
      pass

  # add package language definitions
  parameters['language'] = language

  # add package messages definitions
  parameters['messages'] = messages

  # add package error exceptions definitions
  parameters['errorExceptions'] = error_exceptions

  # add package error handling definitions
  parameters['errorHandling'] = error_handling

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
    parameters['language'][keyword]['inheritedOutput'] = []
    for item in missing:
      # fill in the missing output

      try:
        parameters['language'][keyword]['output'][item], inherited_package = getTemplateTextForOutputPackage(parameters, keyword, item)

        # log that the inherited output is being used
        parameters['language'][keyword]['inheritedOutput'].append({item: inherited_package})
      except:
        parameters['language'][keyword]['output'][item] = default_output[item]

        # log that the default output is being used
        parameters['language'][keyword]['defaultOutput'].append(item)

  return parameters


def postCommandLineParser(parameters):

  # Version
  if parameters['globals']['version']:
    import pkg_resources
    print('The Robotics Language version: ' + pkg_resources.get_distribution('RoboticsLanguage').version)

  # Deploy path
  if parameters['developer']['showDeployPath']:
    print(parameters['globals']['deploy'])

  # environments
  if parameters['globals']['setEnvironment'] != '':
    for environment in dpath.util.values(parameters,'manifesto/*/*/environments'):
      if parameters['globals']['setEnvironment'] in environment.keys():

        parameters_filename = os.path.expanduser('~') + '/.rol/parameters.yaml'

        try:
          if os.path.exists(parameters_filename):
            with open(parameters_filename, 'r') as file:
              # read current environment
              current_environment = yaml.safe_load(file)

            # update environment with new definitions
            new_environment = Utilities.mergeDictionaries(environment[parameters['globals']['setEnvironment']], current_environment)

            # backup old parameters
            old_parameters_filename = Utilities.getNonexistantPath(parameters_filename)
            shutil.move(parameters_filename, old_parameters_filename)
          else:
            # copy environment
            new_environment = environment[parameters['globals']['setEnvironment']]

          # create new parameters file
          with open(parameters_filename, 'w') as file:
            # read current environment
            file.write(yaml.safe_dump(new_environment, default_flow_style=False))

          print("Create new parameters file at '" + parameters_filename + "'.\nOld parameters file saved in '"+ old_parameters_filename + "'")

        except Exception as e:
          Utilities.logging.warning('Unable to set environment to "' + parameters['globals']['setEnvironment'] + '". Please check the permissions of the file "' + parameters_filename + '"')
          print(e)




  # Package information
  if parameters['developer']['info']:
    import pkg_resources
    print('The Robotics Language version: ' + pkg_resources.get_distribution('RoboticsLanguage').version)
    for key, value in parameters['manifesto'].iteritems():
      print(key + ':')
      for item, content in value.iteritems():
        extra = ' *' if parameters['globals']['plugins'] in content['path'] else ''
        print('  ' + item + ' (' + content['version'] + ')' + extra)

  # Detailed Package information
  if parameters['developer']['infoPackage'] != '':
    for type in ['Inputs', 'Transformers', 'Outputs']:
      if parameters['developer']['infoPackage'] in parameters['manifesto'][type].keys():
        package = parameters['manifesto'][type][parameters['developer']['infoPackage']]
        print('Package ' + type + '/' + parameters['developer']['infoPackage'])
        print('Version: ' + package['version'])
        print('Path: ' + package['path'])
        print('Information:')
        Utilities.printParameters(package['information'])

  # generate configuration script
  if parameters['developer']['makeConfigurationFile']:
    data = parameters['command_line_flags']
    filtered = filter(lambda x: x[0:11] == 'Information' or 'suppress' not in data[x].keys() or data[x]['suppress'] is not True, data.iterkeys())
    commands = {x: dpath.util.get(parameters, x.replace(':', '/')) for x in filtered}
    commands_dictionary = Utilities.unflatDictionary(commands, ':')
    commands_dictionary['developer']['makeConfigurationFile'] = False

    try:
      Utilities.createFolder(os.path.expanduser('~/.rol'))
      if os.path.isfile(os.path.expanduser('~/.rol/parameters.yaml')):
        with open(os.path.expanduser('~/.rol/parameters.yaml.template'), 'w') as output:
          yaml.dump(commands_dictionary, output, default_flow_style=False)
        print 'Created the file "~/.rol/parameters.yaml.template".'
        print 'Please modify this file and rename it to "~/.rol/parameters.yaml"'
      else:
        with open(os.path.expanduser('~/.rol/parameters.yaml'), 'w') as output:
          yaml.dump(commands_dictionary, output, default_flow_style=False)
        print 'Created the file "~/.rol/parameters.yaml".'
    except Exception as e:
      print 'Error creating configuration file!'
      print e

  # Outputs dependency
  if parameters['developer']['showOutputDependency']:
    for package in parameters['manifesto']['Outputs']:
      if 'parent' in parameters['manifesto']['Outputs'][package].keys():
        print parameters['manifesto']['Outputs'][package]['parent'] + ' <- ' + package

  # Copy examples here
  if parameters['developer']['copyExamplesHere']:
    from_path = parameters['globals']['RoboticsLanguagePath'] + 'Examples'
    here_path = os.getcwd()

    # copytree workaround to ignore existing folders and maintain folder structure. slightly adjusted from here:
    # https://stackoverflow.com/questions/1868714/how-do-i-copy-an-entire-directory-of-files-into-an-existing-directory-using-pyth
    for item in os.listdir(from_path):
      s = os.path.join(from_path, item)
      d = os.path.join(here_path, item)
      if os.path.isdir(s):
        shutil.copytree(s, d)
      else:
        shutil.copy2(s, d)

  # Unit testing
  if parameters['developer']['runTests']:
    from unittest import defaultTestLoader, TextTestRunner
    import coverage

    # save the parameters into a file to pass to the unit tests
    import cloudpickle
    with open('/tmp/parameters.pickle', 'wb') as file:
      cloudpickle.dump(parameters, file)

    # coverage
    if parameters['developer']['coverage']:
      cov = coverage.Coverage(omit=['*/lib/python*', '*Tests/test_*', '*__init__.py'])
      cov.start()

    # look for all the tests and run them
    suite = defaultTestLoader.discover(parameters['globals']['RoboticsLanguagePath'], 'test_*.py')
    TextTestRunner(verbosity=2).run(suite)

    # coverage
    if parameters['developer']['coverage']:
      cov.stop()
      cov.save()
      cov.html_report(directory=parameters['developer']['coverageFolder'], ignore_errors=True)
      print('Coverage report is: ' + parameters['developer']['coverageFolder'] + '/index.html')

    # remove the parameters file
    os.remove('/tmp/parameters.pickle')

    # done
    sys.exit(1)

  # make examples
  if parameters['developer']['makeExamples']:
    import subprocess

    command_line_arguments = copy(parameters['commandLineParameters'])

    command_line_arguments.remove('--make-examples')

    list_commands = []

    for name in glob.glob(parameters['globals']['RoboticsLanguagePath'] + '/*/*/Examples/*.*'):
      list_commands.append([command_line_arguments[0], name] + command_line_arguments[1:])

    for command, index in zip(list_commands, range(len(list_commands))):
      print '[' + str(index + 1) + '/' + str(len(list_commands)) + '] ' + command[1]
      process = subprocess.Popen(command)
      process.wait()

    sys.exit(1)

  return parameters


def ProcessArguments(command_line_parameters, parameters):

  parameters['commandLineParameters'] = command_line_parameters

  # load cached command line flags or create if necessary
  flags, arguments, file_package_name, file_formats = prepareCommandLineArguments(parameters)

  # run the command line parser
  parser, args = runCommandLineParser(parameters, arguments, flags, file_formats,
                                      file_package_name, command_line_parameters)

  # loads definitions for language, messages, etc
  parameters = loadRemainingParameters(parameters)

  # process the parameters
  file_name, file_type, parameters = processCommandLineParameters(args, file_formats, parameters)

  # processes special generic flags
  parameters = postCommandLineParser(parameters)

  return file_name, file_type, parameters
