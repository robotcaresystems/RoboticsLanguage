#
#   This is the Robotics Language compiler
#
#   Template.py: Jinja2 template tools
#
#   Created on: June 22, 2017
#       Author: Gabriel A. D. Lopes
#      Licence: Apache 2.0
#    Copyright: 2014-2018 Robot Care Systems BV, The Hague, The Netherlands. All rights reserved.
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
from shutil import copy
from pygments import highlight
from RoboticsLanguage.Base import Utilities
from pygments.lexers import get_lexer_for_filename
from pygments.formatters import Terminal256Formatter
from jinja2 import Environment, FileSystemLoader, TemplateError

default_file_patterns = {}

default_ignore_files = {'.DS_Store'}

default_template_engine_filters = {'tag': Utilities.tag,
                                   'text': Utilities.text,
                                   'dpath': Utilities.path,
                                   'xpath': Utilities.xpath,
                                   'dpaths': Utilities.paths,
                                   'xpaths': Utilities.xpaths,
                                   'parent': Utilities.parent,
                                   'unique': Utilities.unique,
                                   'option': Utilities.option,
                                   'children': Utilities.children,
                                   'initials': Utilities.initials,
                                   'fullCaps': Utilities.fullCaps,
                                   'isDefined': Utilities.isDefined,
                                   'attribute': Utilities.attribute,
                                   'camelCase': Utilities.camelCase,
                                   'todaysDate': Utilities.todaysDate,
                                   'ensureList': Utilities.ensureList,
                                   'attributes': Utilities.attributes,
                                   'underscore': Utilities.underscore,
                                   'mergeManyOrdered': Utilities.mergeManyOrdered,
                                   'optionalArguments': Utilities.optionalArguments,
                                   'underscoreFullCaps': Utilities.underscoreFullCaps,
                                   'sortListCodeByAttribute': Utilities.sortListCodeByAttribute,
                                   'split': lambda x, y: x.split(y)
                                   }

delimeters = {'block_start_string': '<%%',
              'block_end_string': '%%>',
              'variable_start_string': '<<<',
              'variable_end_string': '>>>',
              'comment_start_string': '<##',
              'comment_end_string': '##>'
              }


def createGroupFunction(text):
  '''Internal function to the template engine.
  Returns a function that will apply a string to a list of text templates'''
  return lambda x: '\n'.join([z.format(x) for z in text])


def templateEngine(code, parameters, output=None,
                   ignore_files=default_ignore_files,
                   file_patterns=default_file_patterns,
                   filters=default_template_engine_filters,
                   templates_path=None,
                   deploy_path=None):
  '''The template engine combines multiple template files from different modules to generate code.'''

  # check if the output is specified or use parameters
  if output is None:
    output = parameters['developer']['stepName']

  # check the deploy folder for the code generated
  if deploy_path is None:
    if parameters['developer']['stepName'] in parameters['globals']['deployOutputs'].keys():
      deploy_path = parameters['globals']['deployOutputs'][parameters['developer']['stepName']]
    else:
      deploy_path = parameters['globals']['deploy']

  # check for package dependencies
  package_parents = Utilities.getPackageOutputParents(parameters, output)

  # look for all the templates
  if templates_path is None:
    templates_paths = [parameters['manifesto'][parameters['developer']['stepGroup']][x]['path'] + '/Templates' for x in reversed(package_parents)]

  else:
    templates_paths = [templates_path]


  transformers = [x.split('.')[-1] for x in filter(lambda x: 'Transformers' in x, parameters['globals']['loadOrder'])]

  files_to_process = {}
  files_to_copy = []
  new_files_to_copy = []

  # find all the files in the output template folder, including templates from dependencies
  for templates_path in templates_paths:
    for root, dirs, files in os.walk(templates_path):
      for file in files:
        if file.endswith(".template"):

          # extracts full and relative paths
          file_full_path = os.path.join(root, file)
          file_relative_path = Utilities.replaceFirst(file_full_path, templates_path, '')
          file_deploy_path = Utilities.replaceLast(Utilities.replaceFirst(file_full_path, templates_path, deploy_path), '.template', '')

          # apply file template names
          for key, value in file_patterns.iteritems():
            file_deploy_path = file_deploy_path.replace('_' + key + '_', value)

          # save it
          files_to_process[file_relative_path] = {
              'full_path': file_full_path,
              'deploy_path': file_deploy_path,
              'includes': [], 'header': [], 'elements': []}
        else:
          # just copy the files
          if file not in default_ignore_files:
            copy_file_name = os.path.join(root, file)
            files_to_copy.append(copy_file_name)
            new_files_to_copy.append(Utilities.replaceFirst(copy_file_name, templates_path, deploy_path))


  # find all the non template files in the transformers template folder
  for element in parameters['globals']['loadOrder']:
    if '.Transformers.' in element:
      if 'RoboticsLanguage.' in element:
        path = parameters['globals']['RoboticsLanguagePath']
      else:
        path = parameters['globals']['plugins']



      for output_parent in reversed(package_parents):

        transformer_path = path + '/' + '/'.join(element.split('.')[1:]) + '/Templates/Outputs/' + output_parent

        for root, dirs, files in os.walk(transformer_path):
          for file in files:
            if not file.endswith(".template") and file not in default_ignore_files:
              copy_file_name = os.path.join(root, file)
              files_to_copy.append(copy_file_name)
              new_files_to_copy.append(Utilities.replaceFirst(copy_file_name, transformer_path, deploy_path))

  # rename files acording to file pattern names
  for key, value in file_patterns.iteritems():
    for i in range(len(new_files_to_copy)):
      new_files_to_copy[i] = new_files_to_copy[i].replace('_' + key + '_', value)

  # search for the same file in transformers plugins to include as plugins
  for parent_output in reversed(package_parents):
    for file in files_to_process.keys():
      for module in transformers:
        if os.path.isfile(path + 'Transformers/' + module + '/Templates/Outputs/' + parent_output + '/' + file):

          # remove templates for parent outputs if a child template exists
          if package_parents.index(parent_output) < len(package_parents)-1:
            parent = package_parents[1+package_parents.index(parent_output)]

            header_parent = "{{% import '{}' as Include{} with context %}}\n".format(
                path + 'Transformers/' + module + '/Templates/Outputs/' + parent + file, module)

            if header_parent in files_to_process[file]['header']:
              files_to_process[file]['header'].remove(header_parent)

          # save the include name
          if module not in files_to_process[file]['includes']:
            files_to_process[file]['includes'].append(module)

          # fill in the include header for Jinja2
          files_to_process[file]['header'].append( "{{% import '{}' as Include{} with context %}}\n".format(
              path + 'Transformers/' + module + '/Templates/Outputs/' + parent_output + file, module))

          # prepare the text to fill in the spots where includes happen
          elements_text = "{{{{Include" + module + ".{}}}}}"
          if elements_text not in files_to_process[file]['elements']:
            files_to_process[file]['elements'].append(elements_text)

      # after all modules create a grouping function for fill in includes
      files_to_process[file]['group_function'] = createGroupFunction(files_to_process[file]['elements'])


  # all the data is now ready, time to apply templates
  for file in files_to_process.keys():

    if os.path.realpath(files_to_process[file]['full_path']) not in parameters['globals']['skipTemplateFiles']:

      try:
        # start the jinja environment with special delimiters
        environment = Environment(loader=FileSystemLoader('/'), trim_blocks=True, lstrip_blocks=True, **delimeters)

        # load the group function that places includes on demand
        environment.filters['group'] = files_to_process[file]['group_function']

        # load the main template file for the output
        template = environment.get_template(files_to_process[file]['full_path'])

        # render it
        render = template.render(header=''.join(files_to_process[file]['header']))

        # debug
        if parameters['developer']['intermediateTemplates']:
          if not parameters['globals']['noColours']:
            print Utilities.color.BOLD
            print Utilities.color.YELLOW
          print '=============================================================================='
          print 'File: ' + file
          print 'Full path:' + files_to_process[file]['full_path']
          print 'Deploy path:' + files_to_process[file]['deploy_path']
          print '------------------------------------------------------------------------------'
          if not parameters['globals']['noColours']:
            print Utilities.color.END
            try:
              print(highlight(render, get_lexer_for_filename(files_to_process[file]['deploy_path']),Terminal256Formatter(style=Terminal256Formatter().style)))
            except:
              print(render)
          else:
            print(render)

        # create a new environment that includes all the plugin template code
        preprocessed_environment = Environment(loader=FileSystemLoader('/'), trim_blocks=True, lstrip_blocks=True, finalize=lambda x: x if x is not None else '')

        # add filter that collects serialized code for this output
        filters['serializedCode'] = lambda x: Utilities.allAttribute(x, output)

        # add filters to environment
        preprocessed_environment.filters.update(filters)

        # create a new template that includes all the plugin template code
        preprocessed_template = preprocessed_environment.from_string(render)

        # add some simpler information about the current output package and its parents
        parameters['this'] = parameters['developer']['stepName']
        parameters['this_parents'] = package_parents

        # render the combined template
        result = preprocessed_template.render(code=code, parameters=parameters)
      except TemplateError as e:
        Utilities.logger.error(e.__repr__())
        #   # with Error.exception(parameters, filename=files_to_process[i])
        # Utilities.logErrors(Utilities.formatJinjaErrorMessage(
        #     e, filename=files_to_process[file]['full_path']), parameters)
        return False

      try:
        # create paths for the new files if needed
        Utilities.createFolderForFile(files_to_process[file]['deploy_path'])

        # write files
        new_package_file = open(files_to_process[file]['deploy_path'], 'w')
        new_package_file.write(result)
        new_package_file.close()
        Utilities.logging.debug('Wrote file ' + files_to_process[file]['deploy_path'] + ' ...')

      except OSError as e:
        # with Error.exception(parameters, stop=True)
        Utilities.logErrors(Utilities.formatOSErrorMessage(e), parameters)
        return False

    # copy support files
  for i in range(0, len(new_files_to_copy)):

    if os.path.realpath(files_to_copy[i]) not in parameters['globals']['skipCopyFiles']:

      try:

        # create paths for the new files if needed
        Utilities.createFolderForFile(new_files_to_copy[i])

        # copy files
        copy(files_to_copy[i], new_files_to_copy[i])
        Utilities.logging.debug('Copied file ' + new_files_to_copy[i] + '...')

      except OSError as e:
        # with Error.exception(parameters, stop=True)
        Utilities.logErrors(Utilities.formatOSErrorMessage(e), parameters)
        return False

  return True
