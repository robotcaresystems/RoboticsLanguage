# -*- coding: utf-8 -*-
#
#   This is the Robotics Language compiler
#
#   Default Parameters.py: These are the default parameters that are passed to the compiler
#
#   Created on: October 25, 2017
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

def dictionary(s,language):
  if s in dictionary_list.keys():
    if language in dictionary_list[s]:
      return dictionary_list[s][language]
  return s


dictionary_list = {
  'print': {
            'pt':'imprimir',
            'hi':'लिखो',
            'el':'εκτύπωσε',
            'nl':'afdrukken'
            }
}
