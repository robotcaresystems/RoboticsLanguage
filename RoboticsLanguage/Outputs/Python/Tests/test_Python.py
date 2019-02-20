#
#   This is the Robotics Language compiler
#
#   test_Python.py: Unit testing file
#
#   Created on: 02 November, 2018
#       Author: Gabriel Lopes
#      Licence: license
#    Copyright: copyright
#

import unittest
from RoboticsLanguage.Outputs.Python import Transform

class TestPython(unittest.TestCase):

  # -------------------------------------------------------------------------------------------------
  #  Python tests
  # -------------------------------------------------------------------------------------------------
  def test_template(self):
    self.assertEqual(1,1)



if __name__ == '__main__':
  unittest.main()