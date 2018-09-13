#
#   This is the Robotics Language compiler
#
#   Introspection.py: Introspection tools
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
import inspect

def printMsgInfo(type, indent=''):
  '''Print a tree structure of the message type'''

  names = filter(lambda x: x[0] == '__slots__', inspect.getmembers(type))[0][1]
  types = filter(lambda x: x[0] == '_slot_types', inspect.getmembers(type))[0][1]

  for t, n in zip(types, names):
    if '/' in t:
      print indent + n
      printMsgInfo(getattr(__import__(t.split('/')[0] + '.msg', globals(),
                                       locals(), [t.split('/')[1]]), t.split('/')[1]), indent + '  ')
    else:
      print indent + n + ': ' + t


def getMsgInfo(type):
  '''Returns a dictionary with the structure of the message type'''

  elements = {}

  names = filter(lambda x: x[0] == '__slots__', inspect.getmembers(type))[0][1]
  types = filter(lambda x: x[0] == '_slot_types', inspect.getmembers(type))[0][1]

  for t, n in zip(types, names):
    if '/' in t:
      elements[n] = getMsgInfo(getattr(__import__(t.split('/')[0] + '.msg', globals(),
                                                   locals(), [t.split('/')[1]]), t.split('/')[1]))
    else:
      elements[n] = t
  return elements
