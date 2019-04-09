#
#   This is the Robotics Language compiler
#
#   test_fault_tolerance_system.py: Unit testing file
#
#   Created on: 08 March, 2019
#       Author: Gabriel Lopes
#      Licence: license
#    Copyright: copyright
#

import unittest
from RoboticsLanguage.Inputs.FaultToleranceSystem import Parse

class TestFaultToleranceSystem(unittest.TestCase):

  # -------------------------------------------------------------------------------------------------
  #  Fault Tolerance system tests
  # -------------------------------------------------------------------------------------------------
  def test_template(self):
    self.assertEqual(1,1)



if __name__ == '__main__':
  unittest.main()
