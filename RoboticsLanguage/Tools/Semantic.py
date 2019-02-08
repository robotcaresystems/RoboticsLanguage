#
#   This is the Robotics Language compiler
#
#   Semantic.py: checking
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
import sys
from RoboticsLanguage.Base import Utilities, Types
from RoboticsLanguage.Tools import Exceptions


def Checker(code, parameters):
  '''Generic semantic checking function'''

  # check types
  code, parameters = TypeChecker(code, parameters)

  # check that all variables are initialised
  code, parameters = DefiniteAssignment(code, parameters)

  return code, parameters


def TypeChecker(code, parameters):
  '''Generic type checking function'''

  # check atomic types
  code, parameters = AtomsTypeChecker(code, parameters)

  # check defined types
  code, parameters = TypesTypeChecker(code, parameters)

  # check variable types
  code, parameters = VariablesTypeChecker(code, parameters)

  # check function types
  code, parameters = FunctionsTypeChecker(code, parameters)

  # recursively check the rest of the abstract syntax tree
  code, parameters = RecursiveTypeChecker(code, parameters)

  return code, parameters


def AtomsTypeChecker(code, parameters):

  # traverse xml and set all types for all atomic tags
  [x.set('type', type) for type in Types.type_atomic
   for x in code.xpath('//' + type)]

  return code, parameters


def TypesTypeChecker(code, parameters):

  return code, parameters


def VariablesTypeChecker(code, parameters):

  # fill in global scope variable types
  for variable in code.xpath('/node/option[@name="definitions"]//element'):

    # get the name of the variable
    variable_name = variable.getchildren()[0].attrib['name']

    # get its definition
    variable_definition = variable.getchildren()[1]

    # apply type checker to definition of variable
    variable_definition, parameters = RecursiveTypeChecker(variable_definition, parameters)

    # now look for all the places where this variable used in the code and set its type
    for variable_used in code.xpath('//variable[@name="' + variable_name + '"]'):
      variable_used.attrib['type'] = variable_definition.attrib['type']

  # Now repeat the process for local scope. Now the search for the usage of the variable
  # is limited to the local scope where the variable was defined.
  for variable in code.xpath('/node/option[@name!="definitions"]//element'):

    # get the name of the variable
    variable_name = variable.getchildren()[0].attrib['name']

    # get its definition
    variable_definition = variable.getchildren()[1]

    # apply type checker to definition of variable
    variable_definition, parameters = RecursiveTypeChecker(variable_definition, parameters)

    # now look for the places whithin the scope where this variable used and set its type
    for variable_used in variable.getparent().xpath('//variable[@name="' + variable_name + '"]'):
      variable_used.attrib['type'] = variable_definition.attrib['type']

  return code, parameters


def FunctionsTypeChecker(code, parameters):

  functions = {}

  # check function types
  for function in code.xpath('//function_definition'):
    function_name = function.attrib['name']

    functions[function_name] = {'mandatory': [], 'optional': {}, 'returns': []}

    print '----------------------' + function_name + '-------------------'
    Utilities.printCode(function)

    # 1. check the inputs/outputs of function
    print 'Function arguments ============'
    arguments = function.xpath('function_arguments')

    # for each function argument
    if len(arguments) > 0:
      for argument in arguments[0].getchildren():
        argument, parameters = RecursiveTypeChecker(argument, parameters)

        # mandatory argument
        if argument.tag == 'element':
          functions[function_name]['mandatory'].append(argument.xpath('variable')[0].attrib['type'])

        # optional argument
        if argument.tag == 'assign':
          functions[function_name]['optional'][argument.xpath('element/variable')[0].attrib['name']] = argument.xpath('element/variable')[0].attrib['type']

    Utilities.printParameters(functions)


  #
  #
  #
  #   # 2. check usage of function
  #
  #   # 3. check return statement in function definition
  #
  #   # 4. check contents in function definition
  #
  #
  #
  #
  #   # if the function returns, then ckeck that the type(s) returned in the content
  #   # matches the definition
  #   if len(function.xpath('function_returns')) > 0:
  #
  #     with Exceptions.exception('FunctionDefinition', function, parameters):
  #       function_return_type = function.xpath('function_returns')[0].getchildren()[0].attrib['type']
  #
  #     # find the return tag inside the definitions
  #     return_clauses = function.xpath('function_content//return')
  #     if len(return_clauses) > 0:
  #       for return_clause in return_clauses:
  #         # give error if return type is incorrect in definition
  #         if return_clause.attrib['type'] != function_return_type:
  #           Exceptions.raiseException('FunctionDefinition', 'ReturnDoesNotMatch', return_clause, parameters)
  #     else:
  #       Exceptions.raiseException('FunctionDefinition', 'FunctionDoesNotReturn', return_clause, parameters)
  #
  #
  #   # check the function definition
  #   # check the arguments
  #
  #   # check contents of the function definition
  #   function, parameters = RecursiveTypeChecker(function, parameters)
  #
  #
  #
  #   # check the types of the return part of the function
  #   try:
  #     function_returns = function.xpath('function_returns')[0].getchildren()[0]
  #     function_returns, parameters = RecursiveTypeChecker(function_returns, parameters)
  #   except:
  #     pass
  #
  #   # check that the function returns the correct types
  #
  #   # # check the usage of the function
  #   # for function_use in code.xpath('//function[@name="' + function_name + '"]'):
  #   #   print '======================--' + function_name + '===========---------'
  #   #   Utilities.printCode(function_use, 'lovelace')
  #
  #     # check the arguments
  #
  #     # fill in the return types
  #
  # # after the previous steps it is ready to check all the remaining types recursively
  # # code, parameters = RecursiveTypeChecker(code, parameters)

  return code, parameters


def RecursiveTypeChecker(code, parameters):

  # if element already has a type return
  if 'type' in code.attrib.keys():
    return code, parameters

  # if the element is part of the language
  if code.tag in parameters['language']:

    # first recursively traverse all children elements
    for element in code.getchildren():
      element, parameters = RecursiveTypeChecker(element, parameters)

    if code.tag == 'option':
      if len(code.getchildren()) > 0:
        # copy type of the option content to the option tag
        code.attrib['type'] = code.getchildren()[0].attrib['type']
      else:
        # if empty option because none was selected as default, then make type none.
        code.attrib['type'] = 'none'

      return code, parameters

    # # first recursively traverse all children elements that are not option
    # for element in code.xpath('*[not(self::option)]'):
    # # then traverse the optional arguments.
    # for element in code.xpath('option/*[not(self::name)]'):
    #   element, parameters = semanticTypeChecker(element, parameters)
    #

    # for this element find the parameters and arguments
    optional_names = code.xpath('option/@name')
    optional_types = code.xpath('option/@type')
    argument_types = code.xpath('*[not(self::option)]/@type')
    keys = parameters['language']

    # check optional arguments
    try:
      if 'optional' in keys[code.tag]['definition']:

        # check if optional arguments are defined
        if all([x in keys[code.tag]['definition']['optional'].keys() for x in optional_names]):

          # check types for optional arguments
          if not all(map(lambda x, y: keys[code.tag]['definition']['optional']
                         [x]['test']([y]), optional_names, optional_types)):
            # Error: incorrect types for optional arguments!
            # Error.handler('OptionalArgumentTypes', code, parameters, optional_names, optional_types)
            Utilities.errorOptionalArgumentTypes(
                code, parameters, optional_names, optional_types)
        else:
          # Error: optional argument not defined
          # Error.handler('OptionalArgumentNotDefined', code, parameters, optional_names)
          Utilities.errorOptionalArgumentNotDefined(code, parameters, optional_names)

      # check mandatory argument types
      if keys[code.tag]['definition']['arguments']['test'](argument_types):

        # compute resulting type
        code.attrib['type'] = keys[code.tag]['definition']['returns'](argument_types)

      else:
        # Error: mandatory argument missing or incorrect
        # Error.handler('ArgumentTypes',code, parameters, argument_types)
        Utilities.errorArgumentTypes(code, parameters, argument_types)
    except:
      # with Error.exception(parameters,code, stop=True, message='LanguageDefinition')
      Utilities.errorLanguageDefinition(code, parameters)
      sys.exit(1)

    return code, parameters
  else:
    # @TODO type check variables and functions
    return code, parameters


def DefiniteAssignment(code, parameters):
  return code, parameters
