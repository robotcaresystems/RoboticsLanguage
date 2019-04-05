#
#   This is the Robotics Language compiler
#
#   test_fault_detection_heartbeat.py: Unit testing file
#
#   Created on: 19 February, 2019
#       Author: Gabriel Lopes
#      Licence: license
#    Copyright: copyright
#

import unittest
from RoboticsLanguage.Inputs.FaultDetectionHeartbeat import Transform

class TestFaultDetectionHeartbeat(unittest.TestCase):

  # -------------------------------------------------------------------------------------------------
  #  Fault Detection Heartbeat tests
  # -------------------------------------------------------------------------------------------------
  def test_template(self):
    self.assertEqual(1,1)



if __name__ == '__main__':
  unittest.main()