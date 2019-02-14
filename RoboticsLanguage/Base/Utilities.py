#
#   This is the Robotics Language compiler
#
#   Utilities.py: Utility functions
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
import os
import sys
import time
import dill
import errno
import pprint
import hashlib
import logging
import inspect
import datetime
import dpath.util
import coloredlogs
from lxml import etree
from funcy import decorator
from pygments import highlight
from shutil import copy, rmtree
from pygments.formatters import Terminal256Formatter
from pygments.lexers import PythonLexer, XmlLexer, get_lexer_by_name
from jinja2 import Environment, FileSystemLoader, Template, TemplateSyntaxError, TemplateAssertionError, TemplateError

# -------------------------------------------------------------------------------------------------
#  Default encoding is Unicode
# -------------------------------------------------------------------------------------------------

reload(sys)
sys.setdefaultencoding('utf-8')


# -------------------------------------------------------------------------------------------------
#  Helping functions
# -------------------------------------------------------------------------------------------------

def printSource(text, language, parameters=None, style='monokai'):
  if parameters is not None and parameters['globals']['noColours']:
    print(text)
  else:
    print(highlight(text, get_lexer_by_name(language), Terminal256Formatter(style=Terminal256Formatter().style)))


def printCode(code, parameters=None, style='monokai'):
  if not isinstance(code, list):
    code = [code]

  # a list of xml elements
  for element in code:
    if isinstance(element, etree._Element):
     if parameters is not None and parameters['globals']['noColours']:
       print(etree.tostring(element, pretty_print=True))
     else:
       print(highlight(etree.tostring(element, pretty_print=True), XmlLexer(), Terminal256Formatter(style=Terminal256Formatter(style=style).style)))
  # a list of string
  if all([isinstance(element, etree._ElementStringResult) for element in code]):
    print(code)


def printParameters(elements, parameters=None, style='monokai'):
  if parameters is not None and parameters['globals']['noColours']:
    pprint.pprint(elements)
  else:
    print(highlight(pprint.pformat(elements), PythonLexer(),
                    Terminal256Formatter(style=Terminal256Formatter(style=style).style)))


def printVariable(x):
  frame = inspect.currentframe().f_back
  s = inspect.getframeinfo(frame).code_context[0]
  r = re.search(r"\((.*)\)", s).group(1)
  print("{} = {}".format(r, x))


# -------------------------------------------------------------------------------------------------
#  Error handling
# -------------------------------------------------------------------------------------------------


def logErrors(errors, parameters):
  if isinstance(errors, list):
    for error in errors:
      logging.error(error)
      parameters['errors'].append(error)
  else:
    logging.error(errors)
    parameters['errors'].append(errors)

# given a file name and a line number, returns the text line


def fileLineNumberToLine(filename, line_number):
  with open(filename) as file:
    line = [next(file) for x in xrange(line_number)][-1]
  return line

# given a text string and a line number, returns the text line


def textLineNumberToLine(text, line_number):
  return text.split('\n')[line_number - 1]


# given a position (byte counter) and text, returns the line, line number and column number
def positionToLineColumn(position, text):
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

  column_number_text = ' column ' + \
      str(column_number) if column_number > 0 else ''

  return (line_text + error_type + ' error' + file_text + line_number_text + column_number_text + ': ' + color.BOLD + reason + color.END)

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
  line_number, column_number, line = positionToLineColumn(
      exception.position, exception.input)

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
  line_number, column_number, line = positionToLineColumn(
      int(position), code_text)

  parameters['errors'].append(error + reason)

  return errorMessage(error, reason,
                      line_number=line_number, column_number=column_number, line=line)


def errorOptionalArgumentTypes(code, parameters, optional_names, optional_types):
  message = 'Incorrect types for optional parameters. '

  for name, types in zip(optional_names, optional_types):
    if not parameters['language'][code.tag]['definition']['optional'][name]['test'](types):
      message += 'The type of the optional parameter "' + name + '" should be "' + \
          parameters['language'][code.tag]['definition']['optional'][name]['documentation'] + \
          '" instead of "' + types + '"\n'
  # show error
  logger.error(formatSemanticTypeErrorMessage(
      parameters['text'], parameters, getTextMinimumPositionXML(code), 'Type', message))


def errorOptionalArgumentNotDefined(code, parameters, optional_names):
  # Error! figure out which parameter is not defined
  message = ''
  keys = parameters['language'][code.tag]['definition']['optional'].keys()

  for x in set(optional_names) - set(keys):
    message += 'The optional parameter "' + x + '" is not defined.\n'

  message += 'The list of defined optional parameters is: ' + str(keys)

  logger.error(formatSemanticTypeErrorMessage(
      parameters['text'], parameters, getTextMinimumPositionXML(code), 'Type', message))


def errorArgumentTypes(code, parameters, argument_types):
  message = 'Incorrect argument types for function "' + \
      code.tag + '". The expected argument types are:\n   '
  message += code.tag + \
      '( ' + parameters['language'][code.tag]['definition']['arguments']['documentation'] + ' )\n'
  message += '\nInstead received:\n   ' + code.tag + \
      '( ' + ','.join(argument_types) + ' )\n'

  logger.error(formatSemanticTypeErrorMessage(
      parameters['text'], parameters, getTextMinimumPositionXML(code), 'Type', message))


def errorLanguageDefinition(code, parameters):
  message = 'Language element "' + code.tag + \
      '" ill defined. Please check definition.'

  logger.error(formatSemanticTypeErrorMessage(
      parameters['text'], parameters, getTextMinimumPositionXML(code), 'Type', message))


# -------------------------------------------------------------------------------------------------
#  Decorators for performance and debug
# -------------------------------------------------------------------------------------------------


@decorator
def log_all_calls(function):
  print('function name: ' + function._func.__name__ + ' arguments: ' + str(function._args))
  return function()


@decorator
def name_all_calls(function):
  print('function name:' + function._func.__name__)
  return function()


@decorator
def time_all_calls(function):
  start = time.time()
  sys.stdout.write('<<<')
  sys.stdout.flush()
  result = function()
  print('function name: ' + function._func.__name__ + 'execution time: ' + str(time.time() - start) + ' seconds>>>')
  return result


@decorator
def cache_in_disk(function):
  cache_path = '/.rol/cache/'

  # create a name based on the module and function name
  name = __name__ + '.' + function._func.__name__

  # create a the path name for the file to cache
  path = os.path.expanduser("~") + cache_path + name + '.cache'

  if os.path.isfile(path):
    # if file exists just load it
    return dill.load(open(path, "rb"))
  else:
    # otherwise run function
    data = function()

    # save the data in a file
    createFolder(os.path.expanduser("~") + cache_path)
    dill.dump(data, open(path, "wb"))  # , protocol=dill.HIGHEST_PROTOCOL)
    return data


global_function_cache = {}


def cache_function(function):
  def wrapper(*arguments, **options):
    global global_function_cache
    hash = hashlib.md5(function.__name__ + str(arguments) + str(options)).hexdigest()
    # hash = hash(function.__name__ + str(arguments) + str(options))
    # print '<<<call: [' + hash + ']' + function.__name__ + str(arguments) + str(options)
    if hash not in global_function_cache.keys():
      result = function(*arguments, **options)
      global_function_cache[hash] = result
      # print 'cache: + ' + str(hash) + '>>>'
    else:
      result = global_function_cache[hash]
      # print 'use: - ' + str(hash) + '>>>'
    return result
  return wrapper


# -------------------------------------------------------------------------------------------------
#  logging utilities
# -------------------------------------------------------------------------------------------------


# Create a logger object.
logger = logging.getLogger(__name__)
coloredlogs.install(fmt='%(levelname)s: %(message)s')
coloredlogs.install(level='WARN')

# install colours in the logger


def setLoggerLevel(level):
  coloredlogs.install(level=level.upper())

# command line codes for colors


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


def incrementCompilerStep(parameters, group, name):
  # update the compiler step
  parameters['developer']['stepCounter'] = parameters['developer']['stepCounter'] + 1
  parameters['developer']['stepGroup'] = group
  parameters['developer']['stepName'] = name

  # log the current step
  logger.info(
      'Step [' + str(parameters['developer']['stepCounter']) + "]: " + group + " - " + name)

  return parameters


def progressMessage(parameters):
  parameters['developer']['progressPercentage'] = parameters['developer']['progressPercentage'] + 1
  progress_percentage = parameters['developer']['progressPercentage']
  progress_total = parameters['developer']['progressTotal']
  progress_bar = parameters['developer']['progressBar']

  sys.stdout.write('\r[{:04.1f}%] {} {}                         '.format(
      progress_percentage * 100 / progress_total, '\\|/-'[progress_bar % 4], \
      parameters['developer']['stepGroup'] + ', ' + parameters['developer']['stepName']))
  sys.stdout.flush()


def progressSpin(parameters):
  parameters['developer']['progressBar'] = parameters['developer']['progressBar'] + 1
  progress_percentage = parameters['developer']['progressPercentage']
  progress_total = parameters['developer']['progressTotal']
  progress_bar = parameters['developer']['progressBar']

  sys.stdout.write('\r[{:04.1f}%] {}'.format(
      progress_percentage * 100 / progress_total, '\\|/-'[progress_bar % 4]))
  sys.stdout.flush()


def progressDone(parameters):
  final_time = time.time() - parameters['developer']['progressStartTime']
  sys.stdout.write('\r[{:04.1f}%] {}                         \n'.format(
      100 , 'Done in {}.'.format(time.strftime("%Hh %Mm %Ss", time.gmtime(final_time)))))
  sys.stdout.flush()


def checkQueryNamespaces(text):
  '''Looks for namespace references in the query text and add them explicitely to xpath'''
  namespaces = {'namespaces': {}}
  name = re.split('([a-zA-Z0-9]+):[a-zA-Z0-9]+', text)
  if name is not None:
    namespaces['namespaces'] = {value: value for value in name[1::2]}

  return text, namespaces


def showDeveloperInformation(code, parameters):

  if parameters['developer']['progress']:
    progressMessage(parameters)

  if parameters['developer']['step'] == parameters['developer']['stepCounter']:

      # show developer information for xml code
    if parameters['developer']['code'] and code is not None:
      printCode(code, parameters)

    # show developer information for parameters
    if parameters['developer']['parameters']:
      printParameters(parameters, parameters)

    # show developer information for specific xml code
    if parameters['developer']['codePath'] is not '' and code is not None:
      try:
        query, namespaces = checkQueryNamespaces(parameters['developer']['codePath'])
        printCode(code.xpath(query, **namespaces), parameters)
      except:
        logger.warning(
            "The path'" + parameters['developer']['codePath'] + "' is not present in the code")

    # show developer information for specific parameters
    if parameters['developer']['parametersPath'] is not '':
      try:
        for element in paths(parameters, parameters['developer']['parametersPath']):
          printParameters(element, parameters)
      except:
        logger.warning(
            "The path'" + parameters['developer']['parametersPath'] + "' is not defined in the internal parameters.")

    if parameters['developer']['stop']:
      sys.exit(0)


# -------------------------------------------------------------------------------------------------
#  Module utilities
# -------------------------------------------------------------------------------------------------


def importModule(z, a, b, c):
  return __import__(z + '.' + a + '.' + b, globals(), locals(), ensureList(c))


def removeCache(cache_path='/.rol/cache'):
  global logger
  logger.debug('Removing caching...')
  path = os.path.expanduser("~") + cache_path
  if os.path.isdir(path):
    rmtree(path)


def myPluginPath(parameters):
  return parameters['manifesto'][parameters['developer']['stepGroup']][parameters['developer']['stepName']]['path']


def myOutputPath(parameters):
  if parameters['developer']['stepName'] in parameters['globals']['deployOutputs'].keys():
    return parameters['globals']['deployOutputs'][parameters['developer']['stepName']]
  else:
    return parameters['globals']['deploy']



def getPackageOutputParents(parameters, package):
  if 'parent' in parameters['manifesto']['Outputs'][package].keys():
    return [package] + getPackageOutputParents(parameters, parameters['manifesto']['Outputs'][package]['parent'])
  else:
    return [package]


# -------------------------------------------------------------------------------------------------
#  Dictionary utilities
# -------------------------------------------------------------------------------------------------


def isKeyDefined(key, d):
  if isinstance(d, dict):
    return key in d.keys()
  else:
    return False


def isDefined(dictionary, element):
  return len(dpath.util.values(dictionary, element)) > 0


def getDictValue(key, d):
  if isKeyDefined(key, d):
    return d[key]
  else:
    return None


# @REFACTOR remove this function later
def mergeDictionaries(a, b):
  dpath.util.merge(b, a)
  return b


def flatDictionary(d, s='-', list=None, name=''):
  if list is None:
    list = {}
  for key, value in d.iteritems():
    if isinstance(value, dict):
      list.update(flatDictionary(value, s, list, name + s + key))
    else:
      list[name + s + key] = value
  return list


def unflatDictionary(l, s='-'):
  dictionary = {}
  for key, value in l.iteritems():
    dpath.util.new(dictionary, key.replace(s, '/'), value)
  return dictionary


def path(dictionary, dictionary_path):
  return dpath.util.get(dictionary, dictionary_path)


def paths(dictionary, dictionary_path):
  return dpath.util.values(dictionary, dictionary_path)

# -------------------------------------------------------------------------------------------------
#  String utilities
# -------------------------------------------------------------------------------------------------


def replaceLast(string, source, destination):
  return source.join(string.split(source)[0:-1])+destination+string.split(source)[-1]


def replaceFirst(string, source, destination):
  return string.replace(source, destination, 1)


def lowerNoSpace(s):
  return s.replace(' ', '').lower()


def lowerSpaceToDash(s):
  return s.replace(' ', '-').lower()


def underscore(text):
  return text.replace('/', '_').replace(' ', '_').replace('.', '_').lower()


def underscoreFullCaps(text):
  return text.replace('/', '_').replace(' ', '_').replace('.', '_').upper()


def fullCaps(text):
  return text.replace('/', '').replace(' ', '').replace('.', '').replace('_', '').upper()


def smartTitle(s):
  return ' '.join(w[0].upper() + w[1:] for w in s.split())


def camelCase(text):
  return smartTitle(text.replace('/', ' ').replace('.', ' ').replace('_', ' ')).replace(' ', '')


# thanks to https://stackoverflow.com/questions/1175208/elegant-python-function-to-convert-camelcase-to-snake-case
first_cap_re = re.compile('(.)([A-Z][a-z]+)')
all_cap_re = re.compile('([a-z0-9])([A-Z])')


def camelCaseToUnderscore(name):
    s1 = first_cap_re.sub(r'\1_\2', name)
    return all_cap_re.sub(r'\1_\2', s1).lower()


def initials(text):
  return ''.join(c for c in smartTitle(text) if c.isupper())


# -------------------------------------------------------------------------------------------------
#  List utilities
# -------------------------------------------------------------------------------------------------

def mergeManyOrdered(list_of_lists):
  """Non-optimized generalization of mergeOrdered"""
  return reduce(mergeOrdered, list_of_lists)


def mergeOrdered(a, b):
  """Merges two lists, while keeping the order of the elements and trying to find
  minimum number of repetitions. E.g.:
  a = [0,1,3,8,9]
  b = [1,2,4,5,8,9]
  mergeOrdered(a, b) -> [0, 1, 2, 4, 5, 3, 8, 9]
  """
  c = []
  while len(a) > 0 and len(b) > 0:
    if a[0] == b[0]:
      c.append(a.pop(0))
      b.pop(0)
    elif a[0] in b and b[0] not in a:
      c.append(b.pop(0))
    elif a[0] not in b and b[0] in a:
      c.append(a.pop(0))
    else:
      if len(a) > len(b):
        c.append(a.pop(0))
      else:
        c.append(b.pop(0))

  return c + a + b


def ensureList(a):
  if isinstance(a, list):
    return a
  else:
    return [a]


def unique(a):
  return list(set(a))


def sortListCodeByAttribute(list, attribute):
  return sorted(list, key=lambda x: x.attrib[attribute])


# -------------------------------------------------------------------------------------------------
#  File utilities
# -------------------------------------------------------------------------------------------------


def findFileType(extension='py', path='.', followlinks=True):
  for entry in ensureList(path):
    for root, dirs, files in os.walk(entry, followlinks=followlinks):
      for eachfile in files:
        fileName, fileExtension = os.path.splitext(eachfile)
        if fileExtension.lower() == '.' + extension:
          yield root + '/' + eachfile


def findFileName(name, path='.', followlinks=True):
  for entry in ensureList(path):
    for root, dirs, files in os.walk(entry, followlinks=followlinks):
      for eachfile in files:
        if os.path.basename(eachfile) == name:
          yield root + '/' + eachfile


def createFolder(path):
  if not os.path.exists(path):
    try:
      os.makedirs(path)
    except OSError as exc:  # Guard against race condition
      if exc.errno != errno.EEXIST:
        raise


def createFolderForFile(filename):
  createFolder(os.path.dirname(filename))


# -------------------------------------------------------------------------------------------------
#  XML utilities used in parsers
# -------------------------------------------------------------------------------------------------


def xml(tag, content, position=0):
  '''creates XML text for entry'''
  text = ''.join(content) if isinstance(content, list) else content
  return '<' + tag + ' p="' + str(position) + '" >' + text + '</' + tag + '>'


def xmlAttributes(tag, content, position=0, attributes={}):
  '''creates XML text for entry with attributes'''
  attributes_text = ' '.join(
      [key + '="' + str(value) + '"' for key, value in attributes.iteritems()])
  text = ''.join(content) if isinstance(content, list) else content
  return '<' + tag + ' p="' + str(position) + '" ' + attributes_text + '>' + text + '</' + tag + '>'


def xmlFunction(parameters, tag, content, position=0):
  '''creates XML for functions'''
  if tag in parameters['language'].keys():
    # its a known function
    return xml(tag, content, position)
  else:
    # its not part of the language
    return xmlAttributes('function', content, position, attributes={'name': tag})


def xmlFunctionDefinition(parameters, name, arguments, returns, content, position=0):

  parameters['symbols']['functions'].append(name)

  arguments_text = xml('function_arguments', arguments,
                       position) if isinstance(arguments, basestring) else ''
  returns_text = xml('function_returns', returns, position) if isinstance(
      returns, basestring) else ''
  content_text = xml('function_content', content, position) if isinstance(
      content, basestring) else ''

  return xmlAttributes('function_definition', arguments_text + returns_text + content_text, position, attributes={'name': name})


def xmlVariable(parameters, name, position=0):
  '''creates XML for variables'''
  if name in parameters['language'].keys():
    # its a known function
    return xmlFunction(parameters, name, '', position)
  else:
    # its not part of the language
    if name in parameters['symbols']['functions']:
      # could point to a function
      return xmlAttributes('function_pointer', '', position, attributes={'name': name})
    else:
      # or point to a variable
      parameters['symbols']['variables'].append(name)
      return xmlAttributes('variable', '', position, attributes={'name': name})


def xmlMiniLanguage(parameters, key, text, position):
  '''Calls a different parser to process inline mini languages'''
  try:
    code, parameters = importModule(parameters['manifesto']['Inputs'][key]['type'], 'Inputs', key, 'Parse').Parse.parse(text, parameters)
    result = etree.tostring(code)
    return result
  except:
    logging.error("Failed to parse mini-language " + key)


# -------------------------------------------------------------------------------------------------
#  XML utilities used in code generators
# -------------------------------------------------------------------------------------------------

def children(xml):
  return xml.getchildren()


def parent(xml):
  return xml.getparent()


def xpath(xml, path, namespaces={}):
  result = xml.xpath(path, namespaces=namespaces)
  if isinstance(result, list):
    return result[0]
  else:
    return result


def xpaths(xml, path, namespaces={}):
  return xml.xpath(path, namespaces=namespaces)


def text(xml):
  if xml.text is None:
    return ''
  else:
    return xml.text


def tag(xml):
  return xml.tag


def attributes(xml):
  return xml.attrib


def attribute(xml, name):
  try:
    if isinstance(xml, list):
      if len(xml) > 0:
        xml = xml[0]
      else:
        return ''
    if name in xml.attrib.keys():
      return xml.attrib[name]
    else:
      return ''
  except:
    return ''


def allAttribute(xml_list, name):
  if isinstance(xml_list, list):
    return map(lambda xml: attribute(xml, name), xml_list)
  else:
    return attribute(xml_list, name)

def option(xml, name, debug=''):
  try:
    return optionalArguments(xml)[name]
  except:
    return None


def optionalArguments(xml):
  return {a.attrib['name']: a for a in xml.xpath('option')}


def getTextMinimumPositionXML(xml):
  minimum = xml.attrib['p'] if 'p' in xml.attrib else sys.maxint

  childrens_minimum = [getTextMinimumPositionXML(x) for x in xml.getchildren()]

  if childrens_minimum == []:
    return minimum
  else:
    return min(min(childrens_minimum), minimum)

def getFirstParent(code, parent_name):
  try:
    if code.getparent().tag == parent_name:
      return code.getparent()
    else:
      return getFirstParent(code.getparent(), parent_name)
  except:
    return None

# -------------------------------------------------------------------------------------------------
#  Other utilities
# -------------------------------------------------------------------------------------------------


def todaysDate(format):
  today = datetime.date.today()
  return today.strftime(format)


def fillDefaultsInOptionalArguments(code, parameters):
  '''Fill in defaults in optional arguments in case they are not explicitely defined.'''
  try:
    for element in code.xpath('*[not(self::option)]'):
      __, parameters = fillDefaultsInOptionalArguments(element, parameters)

    # if this tag has optional parameters defined
    if len(dpath.util.values(parameters['language'][code.tag], 'definition/optional')) > 0:

      # find all optional parameters
      optional_names = code.xpath('option/@name')

      # get the list of missing parameters
      missing_parameters = list(set(
          parameters['language'][code.tag]['definition']['optional'].keys()) - set(optional_names))

      for parameter in missing_parameters:

        # create XML structure
        optional_argument_tag = etree.Element('option')

        # add the name of the optional parameter
        optional_argument_tag.attrib['name'] = parameter

        # get the tag
        value_tag = etree.Element(
            parameters['language'][code.tag]['definition']['optional'][parameter]['tag'])

        if parameters['language'][code.tag]['definition']['optional'][parameter]['default'] is not None:
          # set the default value
          value_tag.text = str(
              parameters['language'][code.tag]['definition']['optional'][parameter]['default'])

          # append new tag to the code
          optional_argument_tag.append(value_tag)

        code.append(optional_argument_tag)

    # fill in parameters for children
    for element in code.xpath('option'):
      for child in element.getchildren():
        __, parameters = fillDefaultsInOptionalArguments(child, parameters)
  except:
    pass
  return code, parameters


# -------------------------------------------------------------------------------------------------
#  template engine
# -------------------------------------------------------------------------------------------------


default_template_engine_filters = {'todaysDate': todaysDate,
                                   'dpath': path,
                                   'xpath': xpath,
                                   'dpaths': paths,
                                   'xpaths': xpaths,
                                   'isDefined': isDefined,
                                   'ensureList': ensureList,
                                   'text': text,
                                   'tag': tag,
                                   'attributes': attributes,
                                   'attribute': attribute,
                                   'option': option,
                                   'optionalArguments': optionalArguments,
                                   'initials': initials,
                                   'underscore': underscore,
                                   'fullCaps': fullCaps,
                                   'camelCase': camelCase,
                                   'underscoreFullCaps': underscoreFullCaps}
# @TODO add list of files to ignore


def templateEngine(code, parameters, filepatterns, templates_path, deploy_path,
                   filters=default_template_engine_filters):

  files_to_process = []
  files_to_copy = []

  try:
    # find all the template files in the template folder
    for root, dirs, files in os.walk(templates_path, followlinks=True):
      for file in files:
        if file.endswith(".template"):
          files_to_process.append(os.path.join(root, file))
        else:
          files_to_copy.append(os.path.join(root, file))

    # rename files and directory names from template
    # @WARNING For paths that contain duplicate strings this might fail
    new_files = [x.replace(templates_path, deploy_path).replace(
        '.template', '') for x in files_to_process]
    new_copy_files = [x.replace(templates_path, deploy_path)
                      for x in files_to_copy]

    # rename files acording to file pattern names
    for key, value in filepatterns.iteritems():
      for i in range(len(new_files)):
        new_files[i] = new_files[i].replace('_' + key + '_', value)
      for i in range(len(new_copy_files)):
        new_copy_files[i] = new_copy_files[i].replace('_' + key + '_', value)

    # create the Jinja environment
    env = Environment(loader=FileSystemLoader('/'))

    # add filters
    for key, value in filters.iteritems():
      env.filters[key] = value

    # process all files
    for i in range(0, len(files_to_process)):
      try:
        # open templates
        template_body = env.get_template(files_to_process[i])

        # fill in the text
        text_body = template_body.render(code=code, parameters=parameters)
      except TemplateError as e:
        # with Error.exception(parameters, filename=files_to_process[i])
        logErrors(formatJinjaErrorMessage(
            e, filename=files_to_process[i]), parameters)
        return False

      # create paths for the new files if needed
      createFolderForFile(new_files[i])

      # write files
      new_package_file = open(new_files[i], 'w')
      new_package_file.write(text_body)
      new_package_file.close()
      logging.debug('Wrote file ' + new_files[i] + '...')

    # copy support files
    for i in range(0, len(files_to_copy)):
      # create paths for the new files if needed
      createFolderForFile(new_copy_files[i])

      # copy files
      copy(files_to_copy[i], new_copy_files[i])
      logging.debug('Copied file ' + new_copy_files[i] + '...')

  except OSError as e:
    # with Error.exception(parameters, stop=True)
    logErrors(formatOSErrorMessage(e), parameters)
    return False
  return True

#
# # @WARNING this function does not work on the root node (since it uses the getparent function)
# def serialise(code, parameters, keywords, language, filters=default_template_engine_filters):
#
#   snippet = ''
#
#   try:
#
#     # load keyword template text
#     keyword = keywords[code.tag]['output'][language]
#
#     try:
#       # start the template for this tag
#       template = Template(keyword)
#
#       # load the text filters
#       for key, value in filters.iteritems():
#         template.globals[key] = value
#
#       # get all children that are not 'option'
#       children_elements = code.xpath('*[not(self::option)]')
#
#       # get all children
#       # children_elements = code.getchildren()
#
#       # render tags according to dictionary
#       snippet = template.render(children=map(lambda x: serialise(x, parameters, keywords, language, filters), children_elements),
#                                 childrenTags=map(
#           lambda x: x.tag, children_elements),
#           options=dict(zip(code.xpath('option/@name'), map(lambda x: serialise(x,
#                                                                                parameters, keywords, language, filters), code.xpath('option')))),
#           attributes=code.attrib,
#           parentAttributes=code.getparent().attrib,
#           parentTag=code.getparent().tag,
#           text=text(code),
#           tag=code.tag,
#           parameters=parameters,
#           code=code)
#
#       # save text in attribute
#       code.attrib[language] = snippet
#
#     except TemplateError as e:
#       # with Error.exception(parameters)
#       logErrors(formatJinjaErrorMessage(e), parameters)
#
#   except KeyError:
#     # get the line and column numbers
#     line_number, column_number, line = positionToLineColumn(
#         int(code.attrib['p']), parameters['text'])
#
#     # create error message
#     logErrors(errorMessage('Language semantic', 'Keyword \'' + code.tag + '\' not defined',
#                            line_number=line_number, column_number=column_number, line=line), parameters)
#
#   return snippet


# -------------------------------------------------------------------------------------------------
#  Parsing utilities
# -------------------------------------------------------------------------------------------------

def ExtractLanguageDefinitions(language, type, module):
  return {key: value[type][module] for key, value in dpath.util.search(language, '/*/' + type + '/' + module + '/*').iteritems()}


def CreateBracketGrammar(definitions):
  # extract only bracket operators
  bracket = dpath.util.search(definitions, '/*/bracket')

  text = '\n# Bracket operators\n'

  for key, value in bracket.iteritems():
    text += key + ' = \'' + value['bracket']['open'] + '\' wws ' + value['bracket']['arguments'] + \
        ':a wws \'' + value['bracket']['close'] + \
        '\' -> xml(\'' + key + '\',a,self.input.position)\n'

  return text, bracket.keys()


def CreateGenericGrammar(definitions):
  # extract only generic operators
  generic = dpath.util.search(definitions, '/*/generic')

  text = '\n# Generic operators\n'

  for key, value in generic.iteritems():
    text += key + 'Generic = \'' + ''.join([x + '\' wws values:'+chr(97+y)+' wws \'' for x, y in zip(value['generic'], range(len(value['generic'])))][:-1]) + value['generic'][-1] + '\' -> xml(\'' + key + '\',' + '+'.join([chr(97+x) for x in range(len(value['generic'])-1)]) + ',self.input.position)\n'

  return text, [x + 'Generic' for x in generic.keys()]


def CreatePreInPostFixGrammar(definitions):

  # partition by type of operator
  infix = dpath.util.search(definitions, '/*/infix')
  prefix = dpath.util.search(definitions, '/*/prefix')
  postfix = dpath.util.search(definitions, '/*/postfix')
  alternatives = dpath.util.search(definitions, '/*/alternatives')

  # get the precedence orders
  orders = list(set(dpath.util.values(definitions, '/*/*/order')))
  orders.sort()
  previousOrder = dict(zip(orders + ['max'], ['min'] + orders))

  text = ''

  # create grammar for alternatives
  text += '\n# function names alternatives\n'

  for key, value in alternatives.iteritems():
    text += key + \
        ' = ( \'' + ' | '.join(value['alternatives']) + \
        '\' | \'' + key + '\' ) -> \'' + key + '\'\n'

  if len(alternatives.keys()) > 0:
    text += 'functionName = ( ' + \
        ' | '.join(alternatives.keys()) + ' | objectName )\n'
  else:
    text += 'functionName = objectName\n'

  # create grammar for infix operators
  text += '\n# Infix operators\n'

  for key, value in infix.iteritems():

    flat = 'flat' in value['infix'] and value['infix']['flat'] is True

    text += key + ' = P' + str(value['infix']['order']) + ':a '

    if flat:
      text += '( wws '
    else:
      text += 'wws '

    if isinstance(value['infix']['key'], list):
      text += '( \'' + '\' | \''.join(value['infix']['key']) + '\' )'
    else:
      text += '\'' + value['infix']['key'] + '\''

    text += ' wws P' + str(value['infix']['order'])

    if flat:
      text += ')+:b -> xml(\'' + key + '\',[a]+b,self.input.position)\n'
    else:
      text += ':b -> xml(\'' + key + '\',a+b,self.input.position)\n'

  # create grammar for prefix operators
  text += '\n# Prefix operators\n'

  for key, value in prefix.iteritems():

    text += key + ' = '

    if isinstance(value['prefix']['key'], list):
      text += '( \'' + '\' | \''.join(value['prefix']['key']) + '\' )'
    else:
      text += '\'' + value['prefix']['key'] + '\''

    text += ' wws P' + str(value['prefix']['order']) + \
        ':a -> xml(\'' + key + '\',a)\n'

  # create grammar for postfix operators
  text += '\n# Postfix operators\n'

  for key, value in postfix.iteritems():

    text += key + ' = P' + str(value['postfix']['order']) + ':a wws '

    if isinstance(value['postfix']['key'], list):
      text += '( \'' + '\' | \''.join(value['postfix']['key']) + '\' )'
    else:
      text += '\'' + value['postfix']['key'] + '\''

    text += ' -> xml(\'' + key + '\',a)\n'

  # create precedence order
  text += '\n# Precedence order operators\n'

  for order in orders:

    keys = dpath.util.search(definitions, '*/*/order',
                             afilter=lambda x: x == order)

    text += 'P' + str(previousOrder[order]) + ' = ( ' + \
        ' | '.join(keys.keys()) + ' | P' + str(order) + ' )\n'

  if len(orders) > 0:
    return text, orders[-1]
  else:
    return text, 'min'
