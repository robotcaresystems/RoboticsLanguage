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

import unittest
from lxml import etree
from RoboticsLanguage.Inputs.RoL import Parse
from RoboticsLanguage.Base import Utilities


# =================================================================================================
#  RoL Parse
# =================================================================================================


class TestRolParse(unittest.TestCase):
  def test_Parse(self):

    def removePositionAttributes(xml):
      for element in xml.xpath('//*[@p]'):
          element.attrib.pop('p')
      return xml

    def check(self,parameters,text,result):
      code, __ = Parse.parse(text, parameters)
      self.assertEqual(etree.tostring(removePositionAttributes(code)),result)


    # using the base and linear algebra parameters
    parameters = {'manifesto': { 'Transformers': {'Base': {'order': 0,
                                  'packageName': 'Base',
                                  'packageShortName': 'base'},
                                  'LinearAlgebra': {'order': 100,
                                  'packageName': 'Linear Algebra',
                                  'packageShortName': 'lin'}}},
                  'globals': {'language':'en'},
                  'Inputs':{'RoL':{'debug':{'grammar':False}}}}


    # -------------------------------------------------------------------------------------------------
    #  Functional composition
    # -------------------------------------------------------------------------------------------------

    # test position of tags on text
    text = "node(print('hello'))"
    result, parameters = Parse.parse(text, parameters)

    self.assertEqual(etree.tostring(result),
                     '<node p="20"><print p="19"><string p="18">hello</string></print></node>')

    # test basic function composition
    check(self,parameters,"node(print('hello'),print('ok'))",
          '<node><print><string>hello</string></print><print><string>ok</string></print></node>')

    # test optional parameters
    check(self,parameters,"node(print('hello',test:1))",
          '<node><print><string>hello</string><optionalArgument><name>test</name><integer>1</integer></optionalArgument></print></node>')


    # -------------------------------------------------------------------------------------------------
    #  Types
    # -------------------------------------------------------------------------------------------------

    # test integers
    check(self,parameters,"node(123)",'<node><integer>123</integer></node>')

    # @BUG currently -123 returns: <node><negate><integer>123</integer></negate></node>
    # check(self,parameters,"node(-123)",
    #       '<node><integer>-123</integer></node>')

    # @BUG returns <negate> instead of '-' directly
    # test reals
    check(self,parameters,"node(1.23)",     '<node><real>1.23</real></node>')
    check(self,parameters,"node(1.23e10)",  '<node><real>1.23e10</real></node>')
    check(self,parameters,"node(1.23e-10)", '<node><real>1.23e-10</real></node>')
    # check(self,parameters,"node(-1.23)",    '<node><real>-1.23</real></node>')
    # check(self,parameters,"node(-1.23e10)", '<node><real>-1.23e10</real></node>')
    # check(self,parameters,"node(-1.23e-10)",'<node><real>-1.23e-10</real></node>')
    check(self,parameters,"node(.23)",      '<node><real>.23</real></node>')
    check(self,parameters,"node(.23e10)",   '<node><real>.23e10</real></node>')
    check(self,parameters,"node(.23e-10)",  '<node><real>.23e-10</real></node>')
    # check(self,parameters,"node(-.23)",     '<node><real>-.23</real></node>')
    # check(self,parameters,"node(-.23e10)",  '<node><real>-.23e10</real></node>')
    # check(self,parameters,"node(-.23e-10)", '<node><real>-.23e-10</real></node>')

    # test booleans
    check(self,parameters,"node(true)",'<node><boolean>true</boolean></node>')
    check(self,parameters,"node(false)",'<node><boolean>false</boolean></node>')

    # test strings
    check(self,parameters,"node('hello')",'<node><string>hello</string></node>')

    # -------------------------------------------------------------------------------------------------
    #  Infix operators
    # -------------------------------------------------------------------------------------------------

    # basic
    check(self,parameters,"node(1+2)",
          '<node><plus><integer>1</integer><integer>2</integer></plus></node>')

    # precedence order
    check(self,parameters,"node(1+2*3)",
          '<node><plus><integer>1</integer><times><integer>2</integer><integer>3</integer></times></plus></node>')

    # parenthesis order
    check(self,parameters,"node((1+2)*3)",
          '<node><times><plus><integer>1</integer><integer>2</integer></plus><integer>3</integer></times></node>')

    # complex precedence: (1 and ((2 + 3) != 4)) = (5 > (6 * 7))
    check(self,parameters,"node(1 and 2 + 3 != 4 = 5 >= 6 * 7)",
          '<node><assign><and><integer>1</integer><notEqual><plus><integer>2</integer><integer>3</integer></plus><integer>4</integer></notEqual></and><largerEqual><integer>5</integer><times><integer>6</integer><integer>7</integer></times></largerEqual></assign></node>')

    # using unicode symbols
    check(self,parameters,"node(1 ∧ 2 + 3 ≠ 4 = 5 ≥ 6 * 7)",
          '<node><assign><and><integer>1</integer><notEqual><plus><integer>2</integer><integer>3</integer></plus><integer>4</integer></notEqual></and><largerEqual><integer>5</integer><times><integer>6</integer><integer>7</integer></times></largerEqual></assign></node>')


    # -------------------------------------------------------------------------------------------------
    #  Prefix operators
    # -------------------------------------------------------------------------------------------------

    # negate
    check(self,parameters,"node(-a)",'<node><negate><variable>a</variable></negate></node>')


    # -------------------------------------------------------------------------------------------------
    #  Pre-in-postfix operators
    # -------------------------------------------------------------------------------------------------

    check(self,parameters,"node([1,{2,3}])",
          '<node><vector><integer>1</integer><set><integer>2</integer><integer>3</integer></set></vector></node>')

    # -------------------------------------------------------------------------------------------------
    #  Custom operators
    # -------------------------------------------------------------------------------------------------
    check(self,parameters,"node(define f:Reals->Reals,x->x+1)",
          '<node><functionDefinition><variable>f</variable><variable>Reals</variable><variable>Reals</variable><variable>x</variable><plus><variable>x</variable><integer>1</integer></plus></functionDefinition></node>')

    # -------------------------------------------------------------------------------------------------
    #  Mini languages
    # -------------------------------------------------------------------------------------------------
    check(self,parameters,"node(RoLXML<{ <print><string>hello</string></print> }>)",
          '<node><print><string>hello</string></print></node>')

    # @BUG need to fix localisation
    # # -------------------------------------------------------------------------------------------------
    # #  language localisation
    # # -------------------------------------------------------------------------------------------------
    # Utilities.removeCache()
    # parameters['globals']['language'] = 'pt'
    # text = "nó(imprimir('olá mundo'))"
    # code, parameters = Parse.parse(text, parameters)
    # result = etree.tostring(removePositionAttributes(code))
    # self.assertEqual(result,'<node><print><string>ol&#225; mundo</string></print></node>')



if __name__ == '__main__':
  unittest.main()
