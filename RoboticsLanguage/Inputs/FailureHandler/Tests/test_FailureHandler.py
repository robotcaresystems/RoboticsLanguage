#
#   This is the Robotics Language compiler
#
#   test_failure_handler.py: Unit testing file
#
#   Created on: 08 March, 2019
#       Author: Gabriel Lopes
#      Licence: license
#    Copyright: copyright
#

import unittest
from RoboticsLanguage.Inputs.FailureHandler import Transform

class TestFailureHandler(unittest.TestCase):

  # -------------------------------------------------------------------------------------------------
  #  Failure Handler tests
  # -------------------------------------------------------------------------------------------------
  def test_template(self):
    self.assertEqual(1,1)



if __name__ == '__main__':
  unittest.main()