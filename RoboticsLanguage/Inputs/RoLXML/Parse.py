#
#   This is the Robotics Language compiler
#
#   Parse.py: An XML parser
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

from lxml import etree
from RoboticsLanguage.Base import Utilities
import sys

# @REFACTOR same code in inputs/RoL/Parse.py. However, it is specific to RoL, so add to Utilities?
# @TODO generalise when RoL parameters become dictionaries
def nodeParametersToDictionary(xml):
  return {'node': { key:value.text for (key, value) in Utilities.optionalArguments(xml).iteritems() } }


def parse(text, parameters):

  try:
    # create XML object from xml string
    parsed_xml = etree.fromstring(text)

  except etree.XMLSyntaxError as error:
    Utilities.logErrors(Utilities.formatLxmlErrorMessage(error,text = text),parameters)
    sys.exit(1)

  # If the node has parameters, then add them to the global parameters dictionary
  parameters = Utilities.mergeDictionaries(nodeParametersToDictionary(parsed_xml),parameters)

  return parsed_xml, parameters
