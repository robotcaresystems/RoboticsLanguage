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
# from jinja2 import TemplateSyntaxError, TemplateAssertionError, TemplateError

from RoboticsLanguage.Base import Messages
from RoboticsLanguage.Base import Utilities



formatJinjaErrorMessage

# with Error.exception(parameters)
# with Error.exception(parameters, filename=files_to_process[i])

formatParsleyErrorMessage
    # with Error.exception(parameters, action='stop')


formatOSErrorMessage
    # with Error.exception(parameters, action='stop')

formatLxmlErrorMessage
    # with Error.exception(parameters, action='stop')

errorOptionalArgumentTypes
# Error.handler(  parameters, code, 'OptionalArgumentTypes', parameter_names, parameter_types)
errorOptionalArgumentNotDefined
  # Error.handler(  parameters, code, 'OptionalArgumentNotDefined', parameter_names)

errorArgumentTypes
        # Error.handler( parameters, code, 'ArgumentTypes',argument_types)

errorLanguageDefinition
      # with Error.exception(parameters,code,'LanguageDefinition' action='stop')

error_type
reason
line
filename
line_number
column_number

# ------------------------- exceptions -------------------------------

Jinja (exception, filename) -> (
  error_type -> "text"
  reason -> exception.message
  line -> line(exception.filename, exception.lineno)
  filename -> exception.filename
  line_number -> exception.lineno
  column_number X
  )

Parsley(exception) -> (
  error_type -> "text"
  reason ->  exception.formatReason()
  line -> line(exception.position, exception.inputv)
  filename -> X
  line_number -> line_number(exception.position, exception.input)
  column_number -> column_number(exception.position, exception.input)
)

OSError (exception) -> (
  error_type  -> "text"
  reason -> exception.strerror
  line -> X
  filename -> X
  line_number -> X
  column_number   -> X
)

xmlError (exception, text) -> (
  error_type -> "text"
  reason ->  error.message
  line -> line(text,error.line)
  filename -> X
  line_number -> error.line
  column_number -> error.column
)
# ------------------------- errors -------------------------------

SemanticError (code_text, parameters, position, error, reason) -> (
  error_type -> error
  reason -> reason
  line -> line(position, code_text)
  filename X
  line_number -> line_number(position, code_text)
  column_number -> column_number(position, code_text)
)

errorOptionalArgumentTypes(code, parameters, parameter_names, parameter_types) -> (
  error_type -> (parameter_names, parameter_types)
  reason -> "text"
  line -> code
  filename -> X
  line_number -> code
  column_number -> code
)


errorOptionalArgumentNotDefined(code, parameters, parameter_names) -> (
  error_type ->  parameter_names
  reason -> "text"
  line -> code
  filename -> X
  line_number -> code
  column_number -> code
)


errorArgumentTypes(code, parameters, argument_types)
  error_type ->  argument_types
  reason -> "text"
  line -> code
  filename -> X
  line_number -> code
  column_number -> code
)

errorLanguageDefinition(code, parameters)
  error_type ->  code
  reason -> "text"
  line -> code
  filename -> X
  line_number -> code
  column_number -> code



def message(key, *options):
  # try to get the chosen compiler language
  try:
    language = options['parameters']['globals']['compilerLanguage']
  except:
    # default to english
    language = 'en'

  # try to get the desired message
  try:
    message = Messages.message[key]
  except:
    Utilities.logger.error('Compiler error: message with key "{}" is not defined'.format(key))
    return ''

  # try to get the message in the right language
  try:
    translated_message = message[language]
  except:
    # try to revert to english
    try:
      translated_message = message['en']
    except:
      Utilities.logger.error('Compiler error: message with key "{}" is not defined for language "{}" or English.'.format(key, language))
      return ''

  # try to format message
  try:
    return translated_message.format(*options)
  except:
    Utilities.logger.error('Compiler error: parameters supplied to error message with key "{}" are incorrect'.format(key))
    return ''



def handler(parameters=None, code=None, key='', **options):
  pass



@contextmanager
def exception(parameters=None, code=None, key='', **options):
  try:
    yield
  except Exception as e:

    # get the logger level if defined. If not, default to error
    level = options['level'] if 'level' in options.keys() else 'error'

    # set the logger level
    logger = lambda *x, **y: Utilities.logger.log(level,*x, **y)

    if 'message' in options.keys():
      # check if there is a message defined for specific types of errors
      if isinstance(options['message'], dict):

        # get the type of error
        error_type = type(e).__name__
        if error_type in options['message'].keys():
          # use pre defined message for type of error
          logger(options['message'][error_type])
        else:
          # generic error message
          logger(level.title()+ ": {0}. Arguments:\n{1!r}".format(type(e).__name__, e.args))
      else:
        print options['message']
    else:
      # generic error message
      logger(level.title()+ ": {0}. Arguments:\n{1!r}".format(type(e).__name__, e.args))




class color:
  PURPLE = '\033[95m'
  CYAN = '\033[96m'
  DARKCYAN = '\033[36m'
  BLUE = '\033[94m'
  GREEN = '\033[92m'
  YELLOW = '\033[93m'
  RED = '\033[91m'
  BOLD = '\033[1m'
  UNDERLINE = '\033[4m'
  END = '\033[0m'





# -------------------------------------------------------------------------------------------------
#  Error handling
# -------------------------------------------------------------------------------------------------


# def logErrors(errors, parameters):
#   if isinstance(errors, list):
#     for error in errors:
#       logger.error(error)
#       parameters['errors'].append(error)
#   else:
#     logger.error(errors)
#     parameters['errors'].append(errors)


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

# generic error message


def errorMessage(error_type, reason, line='', filename='', line_number=0, column_number=0):

  line_text = '\n' + line.strip('\n') + '\n' + (' ' * column_number + '^') + '\n' if line is not '' else ''

  file_text = ' in file:\n"' + filename + '"\n' if filename is not '' else ''

  line_number_text = ' at line ' + str(line_number) if line_number > 0 else ''

  column_number_text = ' column ' + str(column_number) if column_number > 0 else ''

  return (line_text + error_type + ' error' + file_text + line_number_text + column_number_text + ': ' +
          color.BOLD + reason + color.END)

# creates error message from jinja exception


def formatJinjaErrorMessage(exception, filename=''):
  if isinstance(exception, TemplateSyntaxError):
    line = fileLineNumberToLine(exception.filename, exception.lineno)
    return errorMessage('Output template syntax', exception.message, line=line,
                        line_number=exception.lineno, filename=exception.filename)
  elif isinstance(exception, TemplateAssertionError):
    line = fileLineNumberToLine(exception.filename, exception.lineno)
    return errorMessage('Output template assertion', exception.message, line=line,
                        line_number=exception.lineno, filename=exception.filename)
  else:
    return errorMessage('Unexpected output template', exception.message, filename=filename)

# creates error message from parsley exception


def formatParsleyErrorMessage(exception):
  # get the line and column numbers
  line_number, column_number, line = positionToLineColumn(exception.position, exception.input)

  return errorMessage('Input syntax parsing', exception.formatReason(),
                      line_number=line_number, column_number=column_number, line=line)

# creates error message for file related issues


def formatOSErrorMessage(exception):
  return errorMessage('File system', exception.strerror)


def formatLxmlErrorMessage(exception, text=''):
  errors = []
  for error in exception.error_log:
    if text is not '':
      line = textLineNumberToLine(text, error.line)
    else:
      line = ''
    errors.append('\n' + errorMessage('XML parsing', error.message,
                                      line=line, line_number=error.line, column_number=error.column))
  return errors


def formatSemanticTypeErrorMessage(code_text, parameters, position, error, reason):
  # get the line and column numbers
  line_number, column_number, line = positionToLineColumn(int(position), code_text)

  parameters['errors'].append(error+reason)

  return errorMessage(error, reason,
                      line_number=line_number, column_number=column_number, line=line)



def errorOptionalArgumentTypes(code, parameters, parameter_names, parameter_types):
  message = 'Incorrect types for optional parameters. '

  for name, types in zip(parameter_names, parameter_types):
    if not parameters['language'][code.tag]['definition']['optionalArguments'][name](types):
      message += 'The type of the optional parameter "' + name + '" should be "' + parameters['language'][code.tag]['definition']['optionalArguments'][name].__doc__ +'" instead of "' + types +'"\n'
  # show error
  logger.error(formatSemanticTypeErrorMessage(parameters['text'], parameters, getTextMinimumPositionXML(code), 'Type', message))

def errorOptionalArgumentNotDefined(code, parameters, parameter_names):
  # Error! figure out which parameter is not defined
  message = ''
  keys = parameters['language'][code.tag]['definition']['optionalArguments'].keys()

  for x in set(parameter_names) - set(keys):
    message += 'The optional parameter "' + x + '" is not defined.\n'

  message += 'The list of defined optional parameters is: '+ str(keys)

  logger.error(formatSemanticTypeErrorMessage(parameters['text'], parameters, getTextMinimumPositionXML(code), 'Type', message))

def errorArgumentTypes(code, parameters, argument_types):
  message  = 'Incorrect argument types for function "' + code.tag +'". The expected argument types are:\n   '
  message += code.tag + '( '+ parameters['language'][code.tag]['definition']['argumentTypes'].__doc__ + ' )\n'
  message += '\nInstead received:\n   ' + code.tag + '( '+ ','.join(argument_types) + ' )\n'

  logger.error(formatSemanticTypeErrorMessage(parameters['text'], parameters, getTextMinimumPositionXML(code), 'Type', message))


def errorLanguageDefinition(code, parameters):
  message  = 'Language element "' + code.tag +'" ill defined. Please check definition.'

  logger.error(formatSemanticTypeErrorMessage(parameters['text'], parameters, getTextMinimumPositionXML(code), 'Type', message))

from contextlib import contextmanager

class ReturnException(Exception):
    pass

@contextmanager
def child(action):
  try:
    yield
  except Exception as e:
    print 'exception, then ' + action
    if action=='return':
      raise ReturnException
    else:
      pass




@contextmanager
def ignore():
  try:
    yield
  except Exception as e:
    if type(e).__name__ == 'ReturnException':
      pass
    else:
      raise Exception


def parent(x):
  with child(x):
    a=1+'3'

  z = 3+'df'
  print('got here')


def main():

  with ignore():
    parent('sdfs')

  with ignore():
    parent('return')

  with ignore():
    parent('sdfs')


main()






import parsley
from RoboticsLanguage.Base.Tools import ErrorHandling
from RoboticsLanguage.Base import Messages


parameters = {'messages':Messages.messages, 'globals':{'compilerLanguage':'pt'}}


grammar = '''
main = ws digit ws
'''

from parsley import ParseError as ZZZ

a = parsley.makeGrammar(grammar,{})

try:
  a(' ff').main()
except Exception as pp:
  q2 = pp

q2

type(q2) == parsley.ParseError

repr(type(w))
repr(parsley.ParseError)
repr(IOError)
w = parameters['errorExceptionFunctions'][e.__module__][type(e).__name__]['default'](e,parameters)

w


type(z).__name__
z.__module__
z.formatReason()
z.formatError()
z.position
z.input
z.args
z.error
z.trail




error_handling_functions = {'ometa.runtime':{'ParseError':{'default': lambda z: ErrorHandling.createErrorMessage(parameters,'Parsing',z.formatReason(),line=z.input,line_number=0, column_number=z.position)}}}


Parse error at line 1, column 0: expected a digit. trail: [digit main]

['__class__', '__delattr__', '__dict__', '__doc__', '__eq__', '__format__', '__getattribute__', '__getitem__', '__getslice__', '__hash__', '__init__', '__module__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__setstate__', '__sizeof__', '__str__', '__subclasshook__', '__unicode__', '__weakref__', 'args', 'error', 'formatError', 'formatReason', 'input', 'mergeWith', 'message', 'position', 'trail', 'withMessage']


exception jinja2.TemplateError(message=None)
exception jinja2.UndefinedError(message=None)
exception jinja2.TemplateNotFound(name, message=None)
exception jinja2.TemplatesNotFound(names=(), message=None)
exception jinja2.TemplateSyntaxError(message, lineno, name=None, filename=None)
exception jinja2.TemplateRuntimeError(message=None)
exception jinja2.TemplateAssertionError(message, lineno, name=None, filename=None)

NotImplementedError
ValueError
TypeError
ParseError
EOFError



def z(x):
  yield range(x)

for x in z(5):
  print x


@contextmanager
def handling(x):
  result = yield
  print result
  if result:
    print('yes' + x)
  else:
    print('no' + x)


def larger(a,b):
  return a>b

with handling('hello'):
  larger(14,2)

try:
  from jinja2 import Template

  template = Template("<{{texty}>")

  snippet = template.render(text = "hello")

  print snippet

except Exception as e:
  z = e
  print type(e).__name__
  print e.__module__


from lxml import etree
try:

  xml = etree.fromstring('<hello </>')

  print xml

except Exception as e:
  zz = e
  print type(e).__name__

str(type(zz))

from RoboticsLanguage.Base.Tools import ErrorHandling
from RoboticsLanguage.Transformers.Base import Messages
Messages.messages

ErrorHandling.createErrorMessage(parameters, '' , '')

ErrorHandling.tryMessageInLanguage('xml-syntax', parameters).title()


'\n'.join([ErrorHandling.createErrorMessage(parameters, 'Erro' , error.message, line=ErrorHandling.textLineNumberToLine(text, error.line),line_number=error.line, column_number=error.column) for error in zz.error_log])







def formatLxmlErrorMessage(exception, text=''):
  errors = []
  for error in exception.error_log:
    if text is not '':
      line = textLineNumberToLine(text, error.line)
    else:
      line = ''
    errors.append('\n' + errorMessage('XML parsing', error.message,
                                      line=line, line_number=error.line, column_number=error.column))
  return errors






from shutil import copy

try:
  copy('~/test.txt','~/Projects')
except Exception as e:
  w = e
  print type(e).__name__

  print dir(type(e))
y=q1

z.__class__
w.__class__
y.__class__

type(z).__name__
type(w).__name__
type(y).__name__

z
w
y

type(z).__name__
id(z)
repr(z)
repr(y)
repr(w)

unicode(type(z))
vars(y)
z.__doc__
y.__doc__
w.__doc__


IOError
['__class__', '__delattr__', '__dict__', '__doc__', '__format__', '__getattribute__', '__getitem__', '__getslice__', '__hash__', '__init__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__setstate__', '__sizeof__', '__str__', '__subclasshook__', '__unicode__', 'args', 'errno', 'filename', 'message', 'strerror']


IOError
['__class__', '__delattr__', '__dict__', '__doc__', '__format__', '__getattribute__', '__getitem__', '__getslice__', '__hash__', '__init__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__setstate__', '__sizeof__', '__str__', '__subclasshook__', '__unicode__', 'args', 'errno', 'filename', 'message', 'strerror']
