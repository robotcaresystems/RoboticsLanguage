#
#   This is the Robotics Language compiler
#
#   parsing.py: Implements Error Handling functions
#
#   Created on: September 26, 2018
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
from lxml import etree
from RoboticsLanguage.Base import Utilities


def xml(tag, content=[], attributes={}, text='', namespace=''):

  if namespace == '':
    # create element without namespace
    code = etree.Element(tag, attributes)
  else:
    # create element with namespace
    code = etree.Element('{' + namespace + '}' + tag, attributes, nsmap={namespace: namespace})

  # add text
  code.text = text

  # append content (make sure to deep copy elements, in case there is re-use)
  [code.insert(0, x) for x in reversed(Utilities.ensureList(content))]

  return code


def xmlNamespace(name):
  return lambda *arguments, **options: xml(namespace=name, *arguments, **options)
