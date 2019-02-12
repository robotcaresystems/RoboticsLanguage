#
#   This is the Robotics Language compiler
#
#   Parse.py: Parses the  language
#
#   Created on: 11 February, 2019
#       Author: Gabriel Lopes
#      Licence: license
#    Copyright: copyright
#
import yaml
import copy
from jinja2 import Template
from RoboticsLanguage.Base import Utilities
from RoboticsLanguage.Inputs.RoL import Parse


def getType(value):
  return u'Reals'


def convertParameters(input):
  output = copy.copy(input)

  # extract parameters
  output['parameters'] = []
  for key, value in input['parameters'].iteritems():
    output['parameters'].append({u'name': key, u'type': getType(value), u'value': value})

  # extract topics
  output['topics'] = []
  for key, value in input['topics'].iteritems():
    [name, type] = value.split(' ')
    output['topics'].append({u'variable': key, u'type': type, u'name': name})

  return output


def parse(text, parameters):

  # parse JSON into dictionary
  text_dictionary = yaml.safe_load(text)

  # convert into more descriptive dictionary
  discriptive_dictionary = convertParameters(text_dictionary)

  # open template file
  with open(Utilities.myPluginPath(parameters) + '/Support/fault_detection_topic.rol.template', 'r') as file:
    template = Template(file.read())

  # render the template with the data
  rol_code = template.render(**discriptive_dictionary)

  # parse generated rol file
  code, parameters = Parse.parse(rol_code, parameters)

  return code, parameters
