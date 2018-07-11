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

ros_type_mapping = {
    'Booleans': 'Bool',
    'Reals32': 'Float32',
    'Reals64': 'Float64',
    'Integers8': 'Int8',
    'Integers16': 'Int16',
    'Integers32': 'Int32',
    'Integers64': 'Int64',
    'Naturals8': 'UInt8',
    'Naturals16': 'UInt16',
    'Naturals32': 'UInt32',
    'Naturals64': 'UInt64',
    'Strings': 'String',
}

cpp_type_mapping = {
    'Booleans': 'bool',
    'Reals32': 'float',
    'Reals64': 'double',
    'Integers8': 'int8_t',
    'Integers16': 'int16_t',
    'Integers32': 'int32_t',
    'Integers64': 'int64_t',
    'Naturals8': 'uint8_t',
    'Naturals16': 'uint16_t',
    'Naturals32': 'uint32_t',
    'Naturals64': 'uint64_t',
    'Strings': 'string',
}

def processTopics(code, parameters):
  '''Processes all the ROS topics in the RoL code'''

  # a place to store the information needed for the topics
  parameters['Transformers']['ROS']['topicDefinitions'] = []

  # find all the signals in definitions
  for signal in code.xpath('/node/option[@name="definitions"]/*//element/Signals'):

    # get the parent element to extract the variable name
    variable = signal.getparent().xpath('variable/@name')[0]

    # Save the variable name on the `Signals` tag. Helps simplifying code
    signal.attrib['ROSvariable'] = variable

    # look for assignments for this variable
    assignments = code.xpath('//assign/variable[1][@name="' + variable + '"]')

    if len(assignments) > 0:
      # Tell every assignment with this variable in the left side to use to data domain
      for element in assignments:
        element.getparent().attrib['assignDomain'] = '.data'

    # look for usages of this variable
    usages = code.xpath('//variable[@name="' + variable + '"]')

    # for those that are not assignments use the data domain
    if len(usages) > 0:
      for use in usages:
        if 'assignFunction' not in use.getparent().attrib.keys() and use.getparent().tag != 'element':
          use.attrib['returnDomain'] = '.data'

    # get the type of the signal
    topic_type = signal.getchildren()[0]

    # get options
    topic_name = signal.xpath('option[@name="rosTopic"]')[0].getchildren()[0].text
    flow = signal.xpath('option[@name="flow"]')[0].getchildren()[0].text

    # Find the type for the topic
    if topic_type.tag in ['Reals', 'Integers', 'Naturals']:

      # default value for bits
      bits = '32'

      # try to get the specified bits parameter
      for option in topic_type.xpath('option'):
        if option.attrib['name'] is 'bits':
          bits = option.getchildren()[0].attrib['RosCpp']

      ros_type = 'std_msgs::' + ros_type_mapping[topic_type.tag + bits]
      cpp_type = cpp_type_mapping[topic_type.tag + bits]

    elif topic_type.tag in ['Booleans', 'Strings']:
      ros_type = 'std_msgs::' + ros_type_mapping[topic_type.tag]
      cpp_type = cpp_type_mapping[topic_type.tag]

    else:
      # @REFACTOR just a placeholder for now
      ros_type = 'std_msgs::Empty'
      cpp_type = 'int'

    # add header file for msg
    parameters['Outputs']['RosCpp']['globalIncludes'].add(ros_type.replace('::','/') + '.h')

    # save the topic definitions
    parameters['Transformers']['ROS']['topicDefinitions'].append({'variable': variable,
                                                                  'ros_type': ros_type,
                                                                  'cpp_type': cpp_type,
                                                                  'topic_name': topic_name,
                                                                  'flow': flow})
  return code, parameters


def transform(code, parameters):

  # make sure RosCpp is part of the output
  if any(x in parameters['globals']['output'] for x in ['RosCpp', 'HTMLGUI']):

    # Topics
    code, parameters = processTopics(code, parameters)

  return code, parameters
