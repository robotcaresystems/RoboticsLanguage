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
import re
import sys
from contextlib import contextmanager


class ReturnException(Exception):
  pass


@contextmanager
def tryToProceed():
  '''
  Attempts to proceed when there is an exception. This function is coupled
  with the action 'return' of the exception function. For example:

  from RoboticsLanguage.Tools import Exceptions

  def run_function():
    with Exceptions.exception('test'):
      a = 'a' + 1

    print 'reaches this point'

    with Exceptions.exception('test', action='return'):
      raise Exception('test')

    print 'does not reach this point'

  with Exceptions.tryToProceed():
    run_function()
    print 'does not reach this point'
  print 'reaches this point'

  '''
  try:
    yield
  except Exception as e:
    if type(e).__name__ == 'ReturnException':
      pass
    else:
      raise e


@contextmanager
def exception(key='default', code=None, parameters={}, **options):
  '''
  Generic exception function used in a 'with' context. Can be used fos system/libraries exceptions,
  or to generate own exceptions. Usage:

  # system error
  with Exceptions.exception('test'):
    a = 'a' + 1

  # forced error
  with Exceptions.exception('forced', action='stop'):
    raise Exception('name')
  '''
  try:
    yield
  except Exception as e:

    # get the logger level and action if defined.
    level = options['level'] if 'level' in options.keys() else 'error'
    action = options['action'] if 'action' in options.keys() else None

    try:
      # try to identify who sent the exception
      emitter = re.search("<.*'([^']*)'>", str(type(e))).group(1)
    except:
      emitter = 'unknown'

    # show the message
    showExceptionMessage(emitter, key, e, level, action)

    # apply actions
    if action == 'stop':
      # stop the RoL script
      sys.exit(1)
    elif action == 'return':
      # this will return the parent function
      raise ReturnException


def showExceptionMessage(emitter, key, exception, level, action):
  print 'emitter: ' + emitter
  print 'key: ' + key
  print 'exception: ' + str(exception)
  print 'level: ' + level
  print 'action: ' + str(action)


def raiseException(group, key, code=None, parameters={}):
  with exception(group, code, parameters):
    raise Exception(key)
