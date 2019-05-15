#
#   This is the Robotics Language compiler
#
#   test_fault_handler.py: Unit testing file
#
#   Created on: 05 March, 2019
#       Author: Gabriel Lopes
#      Licence: license
#    Copyright: copyright
#

import unittest
from RoboticsLanguage.Inputs.FaultHandler import Parse

class TestFaultHandler(unittest.TestCase):

  # -------------------------------------------------------------------------------------------------
  #  Fault Handler tests
  # -------------------------------------------------------------------------------------------------
  def test_template(self):
    self.assertEqual(1,1)



if __name__ == '__main__':
  unittest.main()
