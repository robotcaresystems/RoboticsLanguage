#
#   This is the Robotics Language compiler
#
#   Transform.py: Developer code transformer
#
#   Created on: 06 February, 2019
#       Author: Gabriel Lopes
#      Licence: license
#    Copyright: copyright
#


from RoboticsLanguage.Base import Utilities

def transform(code, parameters):

  if len(filter(lambda x: isinstance(x, basestring) and x != '', parameters['Outputs']['Developer']['create'].itervalues())) > 0:
    if isinstance(parameters['globals']['output'], list):
      parameters['globals']['output'].append('Developer')
    else:
      parameters['globals']['output'] = [parameters['globals']['output'], 'Developer']

  return code, parameters
