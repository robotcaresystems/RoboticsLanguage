import os
from shutil import copy
from RoboticsLanguage.Base import Utilities
from jinja2 import Environment, FileSystemLoader, TemplateError

default_templates_path = 'Templates'

default_ignore_files = {'.DS_Store'}

default_file_patterns = {}

default_template_engine_filters = {'todaysDate': Utilities.todaysDate,
                                   'dpath': Utilities.path,
                                   'xpath': Utilities.xpath,
                                   'dpaths': Utilities.paths,
                                   'xpaths': Utilities.xpaths,
                                   'children': Utilities.children,
                                   'parent': Utilities.parent,
                                   'isDefined': Utilities.isDefined,
                                   'ensureList': Utilities.ensureList,
                                   'text': Utilities.text,
                                   'tag': Utilities.tag,
                                   'unique': Utilities.unique,
                                   'attributes': Utilities.attributes,
                                   'attribute': Utilities.attribute,
                                   'option': Utilities.option,
                                   'optionalArguments': Utilities.optionalArguments,
                                   'initials': Utilities.initials,
                                   'underscore': Utilities.underscore,
                                   'fullCaps': Utilities.fullCaps,
                                   'camelCase': Utilities.camelCase,
                                   'underscoreFullCaps': Utilities.underscoreFullCaps}

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
                   templates_path=default_templates_path,
                   deploy_path=None):
  '''The template engine combines multiple template files from different modules to generate code.'''

  if output is None:
    output = parameters['developer']['stepName']

  if deploy_path is None:
    deploy_path = parameters['globals']['deploy']

  if not os.path.isdir(templates_path):
    templates_path = parameters['manifesto'][parameters['developer']['stepGroup']][parameters['developer']['stepName']]['path'] + '/' + templates_path

    # templates_path = '/'.join([parameters['globals']['RoboticsLanguagePath'],
    #                            parameters['developer']['stepGroup'],
    #                            parameters['developer']['stepName'],
    #                            templates_path])
    # @TODO give warning
    # if not os.path.isdir(templates_path):
    #   Tools.Exceptions(...)

  transformers = [x.split('.')[-1] for x in filter(lambda x: 'Transformers' in x, parameters['globals']['loadOrder'])]

  files_to_process = {}
  files_to_copy = []
  new_files_to_copy = []

  # find all the files in the output template folder
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
            'includes': [], 'header': '', 'elements': []}
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

      transformer_path = path + '/' + '/'.join(element.split('.')[1:]) + '/Templates/Outputs/' + output

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
  for file in files_to_process.keys():
    for module in transformers:
      if os.path.isfile(path + 'Transformers/' + module + '/Templates/Outputs/' + output + '/' + file):
        # save the include name
        files_to_process[file]['includes'].append(module)

        # fill in the include header for Jinja2
        files_to_process[file]['header'] += "{{% import '{}' as Include{} with context %}}\n".format(
            path + 'Transformers/' + module + '/Templates/Outputs/' + output + file, module)

        # prepare the text to fill in the spots where includes happen
        files_to_process[file]['elements'].append("{{{{Include" + module + ".{}}}}}")

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
        render = template.render(header=files_to_process[file]['header'])

        # debug
        if parameters['developer']['intermediateTemplates']:
          print '====== File: ' + file + ' -> ' + files_to_process[file]['deploy_path'] + ' ==========================='
          print render
          print '============================================================'

        # create a new environment that includes all the plugin template code
        preprocessed_environment = Environment(loader=FileSystemLoader('/'), trim_blocks=True, lstrip_blocks=True)

        # add filters to environment
        preprocessed_environment.filters.update(filters)

        # create a new template that includes all the plugin template code
        preprocessed_template = preprocessed_environment.from_string(render)

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
