#
#   This is the Robotics Language compiler
#
#   test_deep_inference.py: Unit testing file
#
#   Created on: 25 February, 2019
#       Author: Gabriel Lopes
#      Licence: license
#    Copyright: Robot Care Systems BV
#

import unittest
from RoboticsLanguage.Inputs.DeepInference import Transform

class TestDeepInference(unittest.TestCase):

  # -------------------------------------------------------------------------------------------------
  #  Deep Inference tests
  # -------------------------------------------------------------------------------------------------
  def test_template(self):
    self.assertEqual(1,1)



if __name__ == '__main__':
  unittest.main()