#
#   This is the Robotics Language compiler
#
#   Topics.py: Processes all code for Ros topics, messages and types
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


def process(code, parameters):
  '''Processes all the ROS types in the RoL code'''

  packages = []
  message_dependency = []

  # find dependencies for locally defined messages
  for dependency in code.xpath('//rosm:message/rosm:definition/text()', namespaces={'rosm': 'rosm'}):
    for line in dependency.split('\n'):

      if len(line) > 0 and line.lstrip()[0] != '#':
        if len(line.split('/')) > 1:
          packages.append(line.split('/')[0])
          message_dependency.append(line.split('/')[0])

  for ros_type in code.xpath('//RosType/string/text()'):
    if len(ros_type.split('/')) > 1:
      packages.append(ros_type.split('/')[0])

  # add message generation dependencies
  map(lambda x: parameters['Transformers']['ROS']['messageDependencies'].add(x), message_dependency)
  map(lambda x: parameters['Transformers']['ROS']['buildDependencies'].add(x), packages)
  map(lambda x: parameters['Transformers']['ROS']['runDependencies'].add(x), packages)

  return code, parameters
