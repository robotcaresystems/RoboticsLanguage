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

import re
import os
import unittest
import itertools
from RoboticsLanguage.Base import CommandLine, Utilities, Initialise


def unique_file_name(file):
  ''' Append a counter to the end of file name if
  such file allready exist.

  source: https://snipplr.com/view/41834/
  '''
  if not os.path.isfile(file):
    # do nothing if such file doesn exists
    return file
  # test if file has extension:
  if re.match('.+\.[a-zA-Z0-9]+$', os.path.basename(file)):
    # yes: append counter before file extension.
    name_func = lambda f, i: re.sub('(\.[a-zA-Z0-9]+)$', '_%i\\1' % i, f)
  else:
    # filename has no extension, append counter to the file end
    name_func = lambda f, i: ''.join([f, '_%i' % i])
  for new_file_name in (name_func(file, i) for i in itertools.count(1)):
    if not os.path.exists(new_file_name):
      return new_file_name

# =================================================================================================
#  Base CommandLine
# =================================================================================================


class TestBaseCommandLine(unittest.TestCase):
  def test_ProcessArguments(self):
    Utilities.createFolder('/tmp/RoL/')
    Utilities.createFolder(os.path.expanduser('~') + '/.rol/')

    # create a user wide parameter files
    global_parameters_file = os.path.expanduser('~') + '/.rol/parameters.yaml'

    if os.path.isfile(global_parameters_file):
      # file exist!!! make a backup
      global_parameters_file_exists = True
      backup_file_name = unique_file_name(global_parameters_file)
      os.rename(global_parameters_file, backup_file_name)
    else:
      global_parameters_file_exists = False

    with open(global_parameters_file, 'w') as parameter_file:
      parameter_file.write('testing:\n  parameterA: 1\n  repeatedParameter: 1')

    # create a local parameter file
    with open('/tmp/RoL/.rol.parameters.yaml', 'w') as parameter_file:
      parameter_file.write('testing:\n  parameterB: 2\n  repeatedParameter: 2')

    # create extra parameter file 1
    with open('/tmp/RoL/test1.yaml', 'w') as parameter_file:
      parameter_file.write('testing:\n  parameterC: 3\n  repeatedParameter: 3')

    # create extra parameter file 2
    with open('/tmp/RoL/test2.yaml', 'w') as parameter_file:
      parameter_file.write('testing:\n  parameterD: 4\n  repeatedParameter: 4')

    # create RoL file
    with open('/tmp/RoL/test.rol', 'w') as template_file:
      template_file.write('print(\'hello\')')

    # set command line parameters
    command_line_parameters = ['rol', '/tmp/RoL/test.rol',
                               '/tmp/RoL/test1.yaml', '/tmp/RoL/test2.yaml', '-o', 'RoLXML']

    parameters = Initialise.Initialise(True)

    # run the command line parser
    filename, filetype, outputs, parameters = CommandLine.ProcessArguments(command_line_parameters, parameters)

    # clean up
    if global_parameters_file_exists:
      # delete test file
      os.remove(global_parameters_file)

      # put back the original file
      os.rename(backup_file_name, global_parameters_file)

    # check filename
    self.assertEqual(filename, '/tmp/RoL/test.rol')

    # check filetype
    self.assertEqual(filetype, 'rol')

    # check list of outputs
    self.assertEqual(outputs, ['RoLXML'])

    # check parameters
    self.assertEqual(parameters['testing']['parameterA'], 1)
    self.assertEqual(parameters['testing']['parameterB'], 2)
    self.assertEqual(parameters['testing']['parameterC'], 3)
    self.assertEqual(parameters['testing']['parameterD'], 4)
    self.assertEqual(parameters['testing']['repeatedParameter'], 4)


if __name__ == '__main__':
  unittest.main()
