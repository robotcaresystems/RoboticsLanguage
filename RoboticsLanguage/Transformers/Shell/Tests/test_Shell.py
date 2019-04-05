#
#   This is the Robotics Language compiler
#
#   test_shell.py: Unit testing file
#
#   Created on: 15 February, 2019
#       Author: Gabriel Lopes
#      Licence: license
#    Copyright: copyright
#

import unittest
from RoboticsLanguage.Transformers.Shell import Transform

class TestShell(unittest.TestCase):

  # -------------------------------------------------------------------------------------------------
  #  Shell tests
  # -------------------------------------------------------------------------------------------------
  def test_template(self):
    self.assertEqual(1,1)



if __name__ == '__main__':
  unittest.main()