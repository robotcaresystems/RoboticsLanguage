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
from jinja2 import TemplateSyntaxError, TemplateAssertionError, TemplateError
from RoboticsLanguage.Base import Messages
from RoboticsLanguage.Base import Utilities


class ReturnException(Exception):
  pass


def createErrorMessage(parameters, error_type, reason, line='', filename='', line_number=0, column_number=0):
  # the optional snipped of code
  line_text = '\n' + line.strip('\n') + '\n' + (' ' * column_number + '^') + '\n' if line is not '' else ''

  # the optional finename
  file_text = (tryMessageInLanguage('error-in-file', parameters).format(filename)) if filename is not '' else ''

  # the opitional line number
  line_number_text = (tryMessageInLanguage('error-at-line', parameters).format(line_number)) if line_number > 0 else ''

  # the optional column number
  column_number_text = (tryMessageInLanguage(
      'error-at-column', parameters).format(column_number)) if column_number > 0 else ''

  return tryMessageInLanguage('error-sentence', parameters).format(
      line_text, error_type, file_text, line_number_text, column_number_text, reason)


def tryMessageInLanguage(key, parameters):
  try:
    return tryInLanguage(parameters['messages'][key], parameters['globals']['compilerLanguage'])
  except:
    return default_message(parameters)


def tryExceptionMessageInLanguage(exception, key, parameters):
  try:
    return tryInLanguage(parameters['exeptionMessages'][exception][key], parameters['globals']['compilerLanguage'])
  except:
    return default_message(parameters)


def tryInLanguage(text, language):
  if language in text.keys():
    return text[language]
  else:
    # revert to english
    return text['en']


def default_message(parameters):
  '''Default error message for all languages'''

  return tryInLanguage(Messages.default_error_message, parameters['globals']['compilerLanguage'])


def exceptionMessage(exception_type, key, parameters, code, **options):

  try:
    # Jinja exceptions
    if exception_type == 'TemplateError':
      pass

    elif exception_type == 'UndefinedError':
      pass

    elif exception_type == 'TemplateNotFound':
      pass

    elif exception_type == 'TemplatesNotFound':
      pass

    elif exception_type == 'TemplateRuntimeError':
      pass

    elif exception_type == 'TemplateSyntaxError':
      pass

    elif exception_type == 'TemplateAssertionError':
      pass




  except:
    return Messages.default_message(parameters)


def handlerMessage(key, parameters, code, **options):

  try:
    # get the message from parameters
    message = parameters['messages'][key]

    # get the compiler language
    language = parameters['globals']['compilerLanguage']

    # try to get the message in the desired compiler language
    if language in message.keys():
      translated_message = message[language]
    else:
      # revert to english
      translated_message = message['en']

    return translated_message.format(*(options['format']))

  except:
    return Messages.default_message(parameters)


@contextmanager
def tryToProceed():
  try:
    yield
  except Exception as e:
    if type(e).__name__ == 'ReturnException':
      pass
    else:
      raise Exception


def handler(parameters, code=None, key='', **options):
  # get the logger level if defined. If not, default to error
  level = options['level'] if 'level' in options.keys() else 'error'

  # create a message
  message = handlerMessage(key, parameters, code, **options)

  # show the message
  Utilities.logger.log(level, message['text'])

  # log the messages
  Utilities.logErrors(message, parameters)

  # apply actions
  if 'action' in options.keys() and not parameters['debug']['ignoreErrors']:
    if options['action'] == 'stop':
      # stop the RoL script
      sys.exit(1)
    elif options['action'] == 'return':
      # this will return the parent function
      raise ReturnException


@contextmanager
def exception(parameters, code=None, key='', **options):
  try:
    yield
  except Exception as e:
    # get exception
    exception_type = type(e).__name__

    # get the logger level if defined. If not, default to error
    level = options['level'] if 'level' in options.keys() else 'error'

    # create a message
    message = exceptionMessage(exception_type, key, parameters, code, **options)

    # show the message
    Utilities.logger.log(level, message['text'])

    # log the messages
    Utilities.logErrors(message, parameters)

    # apply actions
    if 'action' in options.keys() and not parameters['debug']['ignoreErrors']:
      if options['action'] == 'stop':
        # stop the RoL script
        sys.exit(1)
      elif options['action'] == 'return':
        # this will return the parent function
        raise ReturnException
