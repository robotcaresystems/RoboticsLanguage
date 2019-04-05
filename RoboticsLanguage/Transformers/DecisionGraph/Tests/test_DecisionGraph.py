#
#   This is the Robotics Language compiler
#
#   test_decision_graph.py: Unit testing file
#
#   Created on: 14 March, 2019
#       Author: Gabriel Lopes
#      Licence: license
#    Copyright: Robot Care Systems BV
#

import unittest
from RoboticsLanguage.Transformers.DecisionGraph import Transform

class TestDecisionGraph(unittest.TestCase):

  # -------------------------------------------------------------------------------------------------
  #  Decision Graph tests
  # -------------------------------------------------------------------------------------------------
  def test_template(self):
    self.assertEqual(1,1)



if __name__ == '__main__':
  unittest.main()