#
#   This is the Robotics Language compiler
#
#   test_developer.py: Unit testing file
#
#   Created on: 07 February, 2019
#       Author: Gabriel Lopes
#      Licence: license
#    Copyright: copyright
#

import unittest
from RoboticsLanguage.Transformers.Developer import Transform

class TestDeveloper(unittest.TestCase):

  # -------------------------------------------------------------------------------------------------
  #  Developer tests
  # -------------------------------------------------------------------------------------------------
  def test_template(self):
    self.assertEqual(1,1)



if __name__ == '__main__':
  unittest.main()