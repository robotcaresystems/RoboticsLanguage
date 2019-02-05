#
#   This is the Robotics Language compiler
#
#   test_cpp.py: Unit testing file
#
#   Created on: 02 November, 2018
#       Author: Gabriel Lopes
#      Licence: license
#    Copyright: copyright
#

import unittest
from RoboticsLanguage.Outputs.Cpp import Transform

class TestCpp(unittest.TestCase):

  # -------------------------------------------------------------------------------------------------
  #  Cpp tests
  # -------------------------------------------------------------------------------------------------
  def test_template(self):
    self.assertEqual(1,1)



if __name__ == '__main__':
  unittest.main()