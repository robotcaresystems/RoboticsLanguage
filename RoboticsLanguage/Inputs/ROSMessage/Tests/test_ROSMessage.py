#
#   This is the Robotics Language compiler
#
#   test_ros_message.py: Unit testing file
#
#   Created on: 08 February, 2019
#       Author: Gabriel Lopes
#      Licence: license
#    Copyright: copyright
#

import unittest
from RoboticsLanguage.Inputs.ROSMessage import Transform

class TestROSMessage(unittest.TestCase):

  # -------------------------------------------------------------------------------------------------
  #  ROS Message tests
  # -------------------------------------------------------------------------------------------------
  def test_template(self):
    self.assertEqual(1,1)



if __name__ == '__main__':
  unittest.main()