#
#   This is the Robotics Language compiler
#
#   Parameters.py: Definition of the parameters for this package
#
#   Created on: 11 July, 2018
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

from RoboticsLanguage.Base import Utilities


def transform(code, parameters):

  # define the namespace used by the finite state machine package
  namespace = {'namespaces': {'fsm': 'fsm'}}

  # this is the absolute path to the extra header file needed for finite state machines
  header_file = Utilities.myPluginPath(parameters) + '/Templates/Outputs/Cpp/_nodename_/include/_nodename_/FiniteStateMachine.h'

  # skip header file if no state machines are defined
  if len(code.xpath('//fsm:machine', **namespace)) == 0:
    parameters['globals']['skipCopyFiles'].append(header_file)

  else:
    # Perform semantic checking
    # look for all machines
    for machine in code.xpath('//fsm:machine', **namespace):

      # a buffer to store pairs of state/transition names
      pairs = []

      # look for all transitions in a machine
      for transition in machine.xpath('.//fsm:transition', **namespace):

        # extract state/transition pair
        pair = transition.xpath('.//*[self::fsm:begin or self::fsm:label]/text()', **namespace)

        # check if pairs already exist
        if pair in pairs:
          print('Error: repeated transitions in FSM "{}": ({}) -{}-> ... '.format(
              machine.xpath('.//fsm:name/text()', **namespace)[0], *pair))
        else:
          pairs.append(pair)

  return code, parameters
