# -*- coding: utf-8 -*-
#!/usr/bin/python
#
#   This is the Robotics Language compiler
#
#   Created on: June 22, 2017
#       Author: Gabriel A. D. Lopes
#      Licence: Apache 2.0
#    Copyright: 2014-2017 Robot Care Systems BV, The Hague, The Netherlands. All rights reserved.
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

import sys
import unittest
from lxml import etree
from RoboticsLanguage.Inputs.RoL import Parse
from RoboticsLanguage.Base import Utilities, Initialise, CommandLine


# initialise compiler
parameters = Initialise.Initialise(False)

# load partial parameters
parameters = CommandLine.loadRemainingParameters(parameters)

# load all parameters after the command line parser
parameters = CommandLine.postCommandLineParser(parameters)

# =================================================================================================
#  RoL Parse
# =================================================================================================


def removePositionAttributes(xml):
  for element in xml.xpath('//*[@p]'):
    element.attrib.pop('p')
  return xml


def check(self, text, result):
  global parameters
  code, __ = Parse.parse(text, parameters)
  self.assertEqual(etree.tostring(removePositionAttributes(code)), result)


class TestRolParse(unittest.TestCase):

  # -------------------------------------------------------------------------------------------------
  #  Functional composition
  # -------------------------------------------------------------------------------------------------
  def test_Functional_Composition(self):

    # test position of tags on text
    text = "node(print('hello'))"
    result, __ = Parse.parse(text, parameters)

    self.assertEqual(etree.tostring(result),
                     '<node p="20"><print p="19"><string p="18">hello</string></print></node>')

    # test basic function composition
    check(self, "node(print('hello'),print('ok'))",
          '<node><print><string>hello</string></print><print><string>ok</string></print></node>')

    # test optional parameters
    check(self, "node(print('hello',test:1))",
          '<node><print><string>hello</string><option name="test"><natural>1</natural></option></print></node>')

  # -------------------------------------------------------------------------------------------------
  #  Types
  # -------------------------------------------------------------------------------------------------

  def test_Types(self):

    # test integers
    check(self, "node(123)", '<node><natural>123</natural></node>')

    # @BUG currently -123 returns: <node><negative><integer>123</integer></negative></node>
    # check(self,"node(-123)",
    #       '<node><integer>-123</integer></node>')

    # @BUG returns <negative> instead of '-' directly
    # test reals
    check(self, "node(1.23)",     '<node><real>1.23</real></node>')
    check(self, "node(1.23e10)",  '<node><real>1.23e10</real></node>')
    check(self, "node(1.23e-10)", '<node><real>1.23e-10</real></node>')
    # check(self,"node(-1.23)",    '<node><real>-1.23</real></node>')
    # check(self,"node(-1.23e10)", '<node><real>-1.23e10</real></node>')
    # check(self,"node(-1.23e-10)",'<node><real>-1.23e-10</real></node>')
    check(self, "node(.23)",      '<node><real>.23</real></node>')
    check(self, "node(.23e10)",   '<node><real>.23e10</real></node>')
    check(self, "node(.23e-10)",  '<node><real>.23e-10</real></node>')
    # check(self,"node(-.23)",     '<node><real>-.23</real></node>')
    # check(self,"node(-.23e10)",  '<node><real>-.23e10</real></node>')
    # check(self,"node(-.23e-10)", '<node><real>-.23e-10</real></node>')

    # test booleans
    check(self, "node(true)", '<node><boolean>true</boolean></node>')
    check(self, "node(false)", '<node><boolean>false</boolean></node>')

    # test strings
    check(self, "node('hello')", '<node><string>hello</string></node>')

  # -------------------------------------------------------------------------------------------------
  #  Infix operators
  # -------------------------------------------------------------------------------------------------
  def test_Infix_Operators(self):

    # basic
    check(self, "node(1+2)",
          '<node><plus><natural>1</natural><natural>2</natural></plus></node>')

    # precedence order
    check(self, "node(1+2*3)",
          '<node><plus><natural>1</natural><times><natural>2</natural><natural>3</natural></times></plus></node>')

    # parenthesis order
    check(self, "node((1+2)*3)",
          '<node><times><plus><natural>1</natural><natural>2</natural></plus><natural>3</natural></times></node>')

    # complex precedence: (1 and ((2 + 3) != 4)) = (5 > (6 * 7))
    check(self, "node(1 and 2 + 3 != 4 = 5 >= 6 * 7)",
          '<node><assign><and><natural>1</natural><notEqual><plus><natural>2</natural><natural>3</natural></plus><natural>4</natural></notEqual></and><largerEqual><natural>5</natural><times><natural>6</natural><natural>7</natural></times></largerEqual></assign></node>')

    # using unicode symbols
    check(self, "node(1 ∧ 2 + 3 ≠ 4 = 5 ≥ 6 * 7)",
          '<node><assign><and><natural>1</natural><notEqual><plus><natural>2</natural><natural>3</natural></plus><natural>4</natural></notEqual></and><largerEqual><natural>5</natural><times><natural>6</natural><natural>7</natural></times></largerEqual></assign></node>')

  # -------------------------------------------------------------------------------------------------
  #  Prefix operators
  # -------------------------------------------------------------------------------------------------

  def test_Prefix_Operators(self):

    # negative
    check(self, "node(-a)", '<node><negative><variable name="a"/></negative></node>')

  # -------------------------------------------------------------------------------------------------
  #  Bracket operators
  # -------------------------------------------------------------------------------------------------

  def test_Bracket_Operators(self):

    check(self, "node([1,{2,3}])",
          '<node><vector><natural>1</natural><set><natural>2</natural><natural>3</natural></set></vector></node>')

  # -------------------------------------------------------------------------------------------------
  #  Custom operators
  # -------------------------------------------------------------------------------------------------
  def test_Custom_Operators(self):
    check(self, "node(define f(x in Reals)->Reals:print(x+1))",
          '<node><function_definition name="f"><function_arguments><element><variable name="x"/><Reals/></element></function_arguments><function_returns><Reals/></function_returns><function_content><print><plus><variable name="x"/><natural>1</natural></plus></print></function_content></function_definition></node>')

  # -------------------------------------------------------------------------------------------------
  #  Mini languages
  # -------------------------------------------------------------------------------------------------
  def test_Mini_Languages(self):
    check(self, "node(RoLXML<{ <print><string>hello</string></print> }>)",
          '<node><print><string>hello</string></print></node>')

  # # @TODO re-implement localisation
  # # -------------------------------------------------------------------------------------------------
  # #  language localisation
  # # -------------------------------------------------------------------------------------------------
  # def test_Language_Localisation(self):
  #   Utilities.removeCache()
  #   parameters['globals']['language'] = 'pt'
  #   text = "nó(imprimir('olá mundo'))"
  #   code, parameters = Parse.parse(text, parameters)
  #   result = etree.tostring(removePositionAttributes(code))
  #   self.assertEqual(result,'<node><print><string>ol&#225; mundo</string></print></node>')


if __name__ == '__main__':
  unittest.main()
