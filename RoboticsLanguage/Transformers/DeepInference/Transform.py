#
#   This is the Robotics Language compiler
#
#   Transform.py: Deep Inference code transformer
#
#   Created on: 25 February, 2019
#       Author: Gabriel Lopes
#      Licence: license
#    Copyright: Robot Care Systems BV
#


from RoboticsLanguage.Base import Utilities

def transform(code, parameters):
  namespaces = {'namespaces':{'di': 'di'}}

  for network in code.xpath('//di:root', **namespaces):

    name = network.xpath('//di:name', **namespaces)[0].text
    




  return code, parameters
