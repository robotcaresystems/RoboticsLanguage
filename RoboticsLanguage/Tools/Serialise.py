#
#   This is the Robotics Language compiler
#
#   Serialise.py: code generation tools
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
from RoboticsLanguage.Base import Utilities
from jinja2 import Template, TemplateError

default_template_engine_filters = {'todaysDate': Utilities.todaysDate,
                                   'dpath': Utilities.path,
                                   'xpath': Utilities.xpath,
                                   'dpaths': Utilities.paths,
                                   'xpaths': Utilities.xpaths,
                                   'children': Utilities.children,
                                   'parent': Utilities.parent,
                                   'isDefined': Utilities.isDefined,
                                   'ensureList': Utilities.ensureList,
                                   'text': Utilities.text,
                                   'tag': Utilities.tag,
                                   'unique': Utilities.unique,
                                   'attributes': Utilities.attributes,
                                   'attribute': Utilities.attribute,
                                   'option': Utilities.option,
                                   'optionalArguments': Utilities.optionalArguments,
                                   'initials': Utilities.initials,
                                   'underscore': Utilities.underscore,
                                   'fullCaps': Utilities.fullCaps,
                                   'camelCase': Utilities.camelCase,
                                   'underscoreFullCaps': Utilities.underscoreFullCaps,
                                   'sortListCodeByAttribute': Utilities.sortListCodeByAttribute
                                   }





# @WARNING this function does not work on the root node (since it uses the getparent function)
def serialise(code, parameters, keywords, language, filters=default_template_engine_filters):

  snippet = ''

  try:

    # load keyword template text
    keyword = keywords[code.tag]['output'][language]
    # keyword = getTemplateTextForOutputPackage(parameters, code.tag, language)

    try:
      # start the template for this tag
      template = Template(keyword)

      # load the text filters
      for key, value in filters.iteritems():
        template.globals[key] = value

      # get all children that are not 'option'
      children_elements = code.xpath('*[not(self::option)]')

      # get all children
      # children_elements = code.getchildren()

      # render tags according to dictionary
      snippet = template.render(children=map(lambda x: serialise(x, parameters, keywords, language, filters),
                                             children_elements),
                                childrenTags=map(
          lambda x: x.tag, children_elements),
          options=dict(zip(code.xpath('option/@name'), map(lambda x: serialise(x,
                                                                               parameters, keywords, language, filters),
                                                           code.xpath('option')))),
          attributes=code.attrib,
          parentAttributes=code.getparent().attrib,
          parentTag=code.getparent().tag,
          text=Utilities.text(code),
          tag=code.tag,
          parameters=parameters,
          code=code)

      # save text in attribute
      code.attrib[language] = snippet

    except TemplateError as e:
      # with Error.exception(parameters)
      Utilities.logErrors(Utilities.formatJinjaErrorMessage(e), parameters)

  except KeyError:
    # get the line and column numbers
    if 'p' in code.keys():
      line_number, column_number, line = Utilities.positionToLineColumn(
          int(code.attrib['p']), parameters['text'])
    else:
      line_number = 0
      column_number = 0
      line = ''

    # create error message
    Utilities.logErrors(Utilities.errorMessage('Language semantic', 'Keyword \'' + code.tag + '\' not defined',
                                               line_number=line_number, column_number=column_number, line=line),
                        parameters)

  return snippet
