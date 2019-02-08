#
#   This is the Robotics Language compiler
#
#   test_ros_2_cpp.py: Unit testing file
#
#   Created on: 08 October, 2018
#       Author: Gabriel Lopes
#      Licence: license
#    Copyright: copyright
#

import unittest
from RoboticsLanguage.Outputs.Ros2Cpp import Transform

class TestRos2Cpp(unittest.TestCase):

  # -------------------------------------------------------------------------------------------------
  #  Ros 2 cpp tests
  # -------------------------------------------------------------------------------------------------
  def test_template(self):
    self.assertEqual(1,1)



if __name__ == '__main__':
  unittest.main()