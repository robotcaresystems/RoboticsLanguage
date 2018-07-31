#
#   This is the Robotics Language compiler
#
#   Parameters.py: Definition of the parameters for this package
#
#   Created on: 31 July, 2018
#       Author: Gabriel Lopes
#      Licence: license
#    Copyright: copyright
#
import random
import string
from RoboticsLanguage.Tools import Semantic
from RoboticsLanguage.Base import Utilities


def isDefinition(child):
  return random.choice([False, True])


def updateEnvironment(environment, child):
  print('creating new definition in: ' + child.tag)
  data = {}
  data.update(environment)
  hash = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))
  data[hash] = hash
  return data


def check(environment, code):
  code.attrib['type'] = str(environment)
  Utilities.printCode(code)
  Utilities.printParameters(environment)


def checkRecursively(environment, code):
  new_environment = {}
  new_environment.update(environment)

  for child in code.getchildren():
    if isDefinition(child):
      new_environment = updateEnvironment(new_environment, child)

    checkRecursively(new_environment, child)

  check(environment, code)


def transform(code, parameters):

  checkRecursively({}, code)


  # check if should ignore semantic checking
  if parameters['Transformers']['TypeChecking']['ignoreSemanticErrors']:
    return code, parameters

  # do all semantic checking
  code, parameters = Semantic.Checker(code, parameters)

  return code, parameters
