import os
from shutil import copy
from RoboticsLanguage.Base import Utilities
from jinja2 import Environment, FileSystemLoader, TemplateError

default_ignore_files = {'.DS_Store'}

default_file_patterns = {}

default_template_engine_filters = {'todaysDate': Utilities.todaysDate,
                                   'dpath': Utilities.path,
                                   'xpath': Utilities.xpath,
                                   'dpaths': Utilities.paths,
                                   'xpaths': Utilities.xpaths,
                                   'isDefined': Utilities.isDefined,
                                   'ensureList': Utilities.ensureList,
                                   'text': Utilities.text,
                                   'tag': Utilities.tag,
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


def templateEngine(code, parameters, output,
                   ignore_files=default_ignore_files,
                   file_patterns=default_file_patterns,
                   filters=default_template_engine_filters):
  '''The template engine combines multiple template files from different modules to generate code.'''

  transformers = parameters['Transformers'].keys()

  deploy_path = parameters['globals']['deploy']

  path = parameters['globals']['RoboticsLanguagePath']

  templates_path = path + 'Outputs/' + output + '/Templates'
  files_to_process = {}
  files_to_copy = []
  new_files_to_copy = []

  # find all the files in the output template folder
  for root, dirs, files in os.walk(templates_path):
    for file in files:
      if file.endswith(".template"):

        # extracts full and relative paths
        file_full_path = os.path.join(root, file)
        file_relative_path = file_full_path.replace(templates_path, '').replace('Templates/', '')
        file_deploy_path = file_full_path.replace(templates_path, deploy_path).replace('.template', '')

        # apply file template names
        for key, value in file_patterns.iteritems():
          print file_deploy_path
          print key
          print value

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
          new_files_to_copy.append(copy_file_name.replace(templates_path, deploy_path))

  # find all the non template files in the transformers template folder
  for transformer in transformers:
    for root, dirs, files in os.walk(path + 'Transformers/' + transformer + '/Templates'):
      for file in files:
        if not file.endswith(".template") and file not in default_ignore_files:
          copy_file_name = os.path.join(root, file)
          files_to_copy.append(copy_file_name)
          new_files_to_copy.append(copy_file_name.replace(path + 'Transformers/' +
                                                          transformer + '/Templates/Outputs/' + output, deploy_path))

  # rename files acording to file pattern names
  for key, value in file_patterns.iteritems():
    for i in range(len(new_files_to_copy)):
      new_files_to_copy[i] = new_files_to_copy[i].replace('_' + key + '_', value)

  # search for the same file in transformers plugins to include as plugins
  for file in files_to_process.keys():
    for module in transformers:
      if os.path.isfile(path + 'Transformers/' + module + '/Templates/Outputs/' + output + file):
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

    try:
      # start the jinja environment with special delimiters
      env = Environment(loader=FileSystemLoader('/'), **delimeters)

      # load the group function that places includes on demand
      env.filters['group'] = files_to_process[file]['group_function']

      # load the main template file for the output
      template = env.get_template(files_to_process[file]['full_path'])

      # render it
      render = template.render(header=files_to_process[file]['header'])

      # debug
      if parameters['debug']['intermediateTemplates']:
        print '====== File: ' + file + '==========================='
        print render
        print '============================================================'

      # create a new template that includes all the plugin template code
      preprocessed_template = Environment(loader=FileSystemLoader('/')).from_string(render)

      # render the combined template
      result = preprocessed_template.render(message="hello", number="3")
    except TemplateError as e:
        # with Error.exception(parameters, filename=files_to_process[i])
      Utilities.logErrors(Utilities.formatJinjaErrorMessage(
          e, filename=files_to_process[file]['full_path']), parameters)
      return False

    try:
      # create paths for the new files if needed
      Utilities.createFolderForFile(deploy_path + file)

      # write files
      new_package_file = open(files_to_process[file]['deploy_path'], 'w')
      new_package_file.write(result)
      new_package_file.close()
      Utilities.logging.debug('Wrote file ' + files_to_process[file]['deploy_path'] + ' ...')

      # copy support files
      for i in range(0, len(new_files_to_copy)):
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
