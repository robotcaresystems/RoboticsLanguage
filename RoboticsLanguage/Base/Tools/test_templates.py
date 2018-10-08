import os
from jinja2 import Environment, FileSystemLoader

default_template_engine_filters = {}
default_file_patterns = {}

filepatterns = {}

path = '/Users/glopes/Projects/Tests/test_templates/templates/'






def templateEngine(code, parameters, output_name, file_patterns=default_file_patterns, filters=default_template_engine_filters):

  delimeters = {'block_start_string': '<%%',
                'block_end_string': '%%>',
                'variable_start_string': '<<<',
                'variable_end_string': '>>>',
                'comment_start_string': '<##',
                'comment_end_string': '##>'
                }

  transformers = ['FSM', 'test']
  output = 'RosCpp'

  deploy_path = parameters['globals']['deploy']

  templates_path = path + 'Outputs/' + output
  files_to_process = {}
  files_to_copy = []

  # find all the template files in the output template folder
  for root, dirs, files in os.walk(templates_path):
    for file in files:
      if file.endswith(".template"):

        # extracts full and relative paths
        file_full_path = os.path.join(root, file)
        file_relative_path = file_full_path.replace(templates_path, '').replace('Templates/', '')

        # save it
        files_to_process[file_relative_path] = {'full_path': file_full_path, 'includes': [], 'header': '', 'elements': []}
      else:
        files_to_copy.append(os.path.join(root, file))


  def CreateGroupFunction(text):
    return lambda x: '\n'.join([z.format(x) for z in text])


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
    files_to_process[file]['group_function'] = CreateGroupFunction(files_to_process[file]['elements'])

  # all the data is now ready, time to apply templates
  for file in files_to_process.keys():

    # start the jinja environment with special delimiters
    env = Environment(loader=FileSystemLoader('/'), **delimeters)

    # load the group function that places includes on demand
    env.filters['group'] = files_to_process[file]['group_function']

    # load the main template file for the output
    template = env.get_template(files_to_process[file]['full_path'])

    # render it
    render = template.render(header=files_to_process[file]['header'])

    print('=================================')
    print(render)
    print('=================================')

    # create a new template that includes all the plugin template code
    preprocessed_template = Environment(loader=FileSystemLoader('/')).from_string(render)

    # render the combined template
    print('-----------------------------------')
    print(preprocessed_template.render(message="hello", number="3"))
    print('-----------------------------------')
