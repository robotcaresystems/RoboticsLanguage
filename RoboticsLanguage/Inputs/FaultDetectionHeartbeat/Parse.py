#
#   This is the Robotics Language compiler
#
#   Parse.py: Parses the  language
#
#   Created on: 19 February, 2019
#       Author: Gabriel Lopes
#      Licence: license
#    Copyright: copyright
#
import yaml
from jinja2 import Template
from RoboticsLanguage.Base import Utilities
from RoboticsLanguage.Inputs.RoL import Parse


def parse(text, parameters):
  Utilities.logging.info("Parsing Fault Detection Heartbeat language...")

  # parse JSON into dictionary
  text_dictionary = yaml.safe_load(text)

  # save the data in the parameters to be used by the GUI
  parameters['Inputs']['FaultDetectionHeartbeat']['data'] = text_dictionary

  # open template file
  with open(Utilities.myPluginPath(parameters) + '/Support/fault_detection_heartbeat.rol.template', 'r') as file:
    template = Template(file.read())

  # render the template with the data
  rol_code = template.render(**text_dictionary)

  # print intermediate rol code is requested
  if parameters['Inputs']['FaultDetectionHeartbeat']['showRol']:
    Utilities.printSource(rol_code, 'coffeescript', parameters)

  # parse generated rol code
  code, parameters = Parse.parse(rol_code, parameters)

  # add fault detection gui to the outputs
  outputs = Utilities.ensureList(parameters['globals']['output'])
  outputs.append('FaultDetectionHeartbeat')
  parameters['globals']['output'] = outputs



  return code, parameters
