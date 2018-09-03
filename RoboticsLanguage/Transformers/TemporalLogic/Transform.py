#
#   This is the Robotics Language compiler
#
#   Language.py: Parses the Robotics Language
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

import copy
from lxml import etree
from RoboticsLanguage.Base import Utilities


def transform(code, parameters):

  logic_properties = []
  counter = 0

  if len(code.xpath('//always|//eventually')) > 0:

    for logic_code in code.xpath('//always|//eventually'):
      properties = {}

      # create a unique id
      counter = counter + 1
      properties['id'] = counter
      logic_code.attrib['TemporalLogicId'] = str(counter)

      # create text element for the GUI
      if 'HTMLGUI' in parameters['globals']['output']:

        # make a copy of the code to not polute it with extra attributes
        xml_copy = copy.deepcopy(logic_code)
        root = etree.Element("root")
        root.append(xml_copy)

        # use the RoL serialiser to create the text tag
        Utilities.serialise(root.getchildren()[0], parameters, parameters['language'], 'RoL')
        properties['text'] = root.getchildren()[0].attrib['RoL']

      logic_properties.append(properties)

  parameters['Transformers']['TemporalLogic']['properties'] = logic_properties

  return code, parameters
