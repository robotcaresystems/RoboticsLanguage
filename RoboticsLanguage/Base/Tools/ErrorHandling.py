#
#   This is the Robotics Language compiler
#
#   ErrorHandling.py: Implements Error Handling functions
#
#   Created on: June 22, 2017
#       Author: Gabriel A. D. Lopes
#      Licence: Apache 2.0
#    Copyright: 2014-2017 Robot Care Systems BV, The Hague, The Netherlands. All rights reserved.
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
from contextlib import contextmanager
import sys
import re
from RoboticsLanguage.Base import Utilities


class ReturnException(Exception):
  pass

def createErrorMessage(parameters, error_type, reason, line='', filename='', line_number=0, column_number=0):
  # the optional snipped of code
  line_text = '\n' + line.strip('\n') + '\n' + (' ' * column_number + '^') + '\n' if line is not '' else ''

  # the optional finename
  file_text = (tryMessageInLanguage(parameters,'error-in-file').format(filename)) if filename is not '' else ''

  # the opitional line number
  line_number_text = (tryMessageInLanguage(parameters,'error-at-line').format(line_number)) if line_number > 0 else ''

  # the optional column number
  column_number_text = (tryMessageInLanguage(parameters,
      'error-at-column').format(column_number)) if column_number > 0 else ''

  return tryMessageInLanguage(parameters,'error-sentence').format(
      line_text, error_type, file_text, line_number_text, column_number_text, reason)


def tryMessageInLanguage(parameters, key):
  try:
    return tryInLanguage(parameters['messages'][key], parameters['globals']['compilerLanguage'])
  except:
    return default_error_message(parameters)


def tryInLanguage(text, language):
  if language in text.keys():
    return text[language]
  else:
    # revert to english
    return text['en']


def default_error_message(parameters):
  '''Default error message for all languages'''

  return tryInLanguage('default_error_message', parameters['globals']['compilerLanguage'])

def fileLineNumberToLine(filename, line_number):
  '''given a file name and a line number, returns the text line'''
  with open(filename) as file:
    line = [next(file) for x in xrange(line_number)][-1]
  return line


def textLineNumberToLine(text, line_number):
  '''given a text string and a line number, returns the text line'''
  return text.split('\n')[line_number - 1]



def positionToLineColumn(position, text):
  '''given a position (byte counter) and text, returns the line, line number and column number'''
  lines = str(text).split('\n')
  counter = 0
  line_number = 1
  column_number = 0
  for line in lines:
    new_counter = counter + len(line)
    if new_counter > position:
      column_number = position - counter
      break
    else:
      counter += len(line) + 1
      line_number += 1
  return line_number, column_number, line


@contextmanager
def tryToProceed():
  try:
    yield
  except Exception as e:
    if type(e).__name__ == 'ReturnException':
      pass
    else:
      raise Exception


def handler(parameters, key='default', **options):
  # get the logger level if defined. If not, default to error
  level = options['level'] if 'level' in options.keys() else 'error'

  try:
    # create a message
    message = parameters['errorHandlingFunctions'][key](parameters, **options)
  except:
    message = default_error_message(parameters)

  # show the message
  Utilities.logger.log(level, message)

  # log the messages
  Utilities.logErrors(message, key, parameters)

  # apply actions
  if 'action' in options.keys() and not parameters['developer']['ignoreErrors']:
    if options['action'] == 'stop':
      # stop the RoL script
      sys.exit(1)
    elif options['action'] == 'return':
      # this will return the parent function
      raise ReturnException


@contextmanager
def exception(e, parameters, key='default', **options):
  try:
    yield
  except Exception as e:

    # get the logger level if defined. If not, default to error
    level = options['level'] if 'level' in options.keys() else 'error'

    try:
      # try the desired exception
      exception_emmiter = re.search("<.*'([^']*)'>", str(type(e))).group(1)
      # create a message
      message = parameters['errorExceptionFunctions'][exception_emmiter][key](e,parameters, **options)
    except:
      try:
        # try the default exception for the emmiter class
        exception_emmiter = '.'.join(exception_emmiter.split('.')[:-1])
        message = parameters['errorExceptionFunctions'][exception_emmiter]['default'](e,parameters, **options)
      except:
        # return the default error message
        message = default_error_message(parameters)

    # show the message
    Utilities.logger.log(level, message)

    # log the messages
    Utilities.logErrors(message, key, parameters, exception=e)

    # apply actions
    if 'action' in options.keys() and not parameters['developer']['ignoreErrors']:
      if options['action'] == 'stop':
        # stop the RoL script
        sys.exit(1)
      elif options['action'] == 'return':
        # this will return the parent function
        raise ReturnException
