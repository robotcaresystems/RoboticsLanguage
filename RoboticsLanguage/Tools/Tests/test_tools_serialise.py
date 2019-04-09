#!/usr/bin/env python
#
#   This is the Robotics Language compiler
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

import unittest
from lxml import etree
from RoboticsLanguage.Tools import Serialise

# =================================================================================================
#  Tools
# =================================================================================================


class TestToolsSerialise(unittest.TestCase):

  # -------------------------------------------------------------------------------------------------
  #  Module serialise
  # -------------------------------------------------------------------------------------------------

  def test_serialise(self):

    # @NOTE Could not test the filters yet. Could test 'keyword invalid' raise
    # create a xml structure
    root = etree.fromstring('<root><xml name="hello"><string option="1">some text</string></xml></root>')
    # note that the serialise fuction cannot work on the root node, so get one of the children first
    xml = [x for x in root.getchildren()][0]
    # define some sample language
    keywords = {'xml': {'output': {'cpp': '// {{children|first}}'}}, 'string': {'output': {'cpp': '\"{{text}}\"'}}}
    parameters = {}
    language = 'cpp'

    Serialise.serialise(xml, parameters, keywords, language)

    self.assertEqual(Serialise.serialise(xml, parameters, keywords, language), '// "some text"')

    # # now raise an error because the key is not defined
    # languages = {'xml':{'output': {'cpp':'// {{children|first}}'}}, }
    # self.assertRaises(Serialise.serialise(xml, parameters, keywords, language))


if __name__ == '__main__':
  unittest.main()
