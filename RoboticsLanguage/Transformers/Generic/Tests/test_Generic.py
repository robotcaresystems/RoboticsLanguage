#
#   This is the Robotics Language compiler
#
#   test_generic.py: Unit testing file
#
#   Created on: 22 October, 2019
#       Author: Gabriel Lopes
#      Licence: Apache 2.0
#    Copyright: Gabriel Lopes
#
#   Licensed under the Apache License, Version 2.0 (the "License"); you may not use
#   this file except in compliance with the License. You may obtain a copy of the
#   License at http://www.apache.org/licenses/LICENSE-2.0 Unless required by
#   applicable law or agreed to in writing, software distributed under the License
#   is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
#   KIND, either express or implied. See the License for the specific language
#   governing permissions and limitations under the License.
#

import unittest
from RoboticsLanguage.Transformers.Generic import Transform

class TestGeneric(unittest.TestCase):

  # -------------------------------------------------------------------------------------------------
  #  generic tests
  # -------------------------------------------------------------------------------------------------
  def test_template(self):
    self.assertEqual(1,1)



if __name__ == '__main__':
  unittest.main()