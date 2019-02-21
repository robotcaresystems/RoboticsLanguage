#
#   This is the Robotics Language compiler
#
#   Language.py: Parses the Robotics Language
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

from Tools import Topics, Types, RosMessage


def transform(code, parameters):

  # make sure RosCpp is part of the output
  if any(x in parameters['globals']['output'] for x in ['RosCpp', 'HTMLGUI', 'Ros2Cpp', 'RosPy']):

    # Types
    code, parameters = Types.process(code, parameters)

    # Topics
    code, parameters = Topics.process(code, parameters)

    # Ros messages
    code, parameters = RosMessage.process(code, parameters)

  return code, parameters
