#!/usr/bin/python
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
from RoboticsLanguage.Base import Transformations, Initialise, CommandLine


# =================================================================================================
#  Base Transformations
# =================================================================================================

class TestBaseTransformations(unittest.TestCase):

  def test_Apply(self):

    xml = etree.fromstring('<node><print><string>hello</string></print></node>')

    # initialise compiler
    parameters = Initialise.Initialise(False)

    # load partial parameters
    parameters = CommandLine.loadRemainingParameters(parameters)

    # load all parameters after the command line parser
    parameters = CommandLine.postCommandLineParser(parameters)


    xml_code, parameters = Transformations.Apply(xml, parameters)

    self.assertEqual(etree.tostring(xml_code),
                     '<node><print RosCpp="ROS_INFO_STREAM(&quot;hello&quot;)"><string RosCpp="&quot;hello&quot;">hello</string><option name="level" RosCpp="&quot;info&quot;"><string RosCpp="&quot;info&quot;">info</string></option></print><option name="name" RosCpp="&quot;unnamed&quot;"><string RosCpp="&quot;unnamed&quot;">unnamed</string></option><option name="rate" RosCpp="25"><real RosCpp="25">25</real></option><option name="initialise" RosCpp=""/><option name="definitions" RosCpp=""/><option name="finalise" RosCpp=""/><option name="cachedComputation" RosCpp=""/></node>')


if __name__ == '__main__':
  unittest.main()
