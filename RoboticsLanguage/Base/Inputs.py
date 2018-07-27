#
#   This is the Robotics Language compiler
#
#   Inputs.py: Parses the Robotics Language and generates an XML structure
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

from . import Utilities

def Parse(file_name, file_type, parameters):
  """Parses the robotics language and converts to XML"""

  if file_name is not None:
    # open the file to compile
    with open(file_name) as file:
      text = file.read()

    # save the source code in the parameters
    parameters['text'] = text

    for key, value in parameters['manifesto']['Inputs'].iteritems():
      # @TODO Add support to multiple file extensions per format, e.g.:
      #       if file_type.lower() in value['fileFormat'].lower():
      if file_type.lower() == value['fileFormat'].lower():

        # update the compiler step
        parameters = Utilities.incrementCompilerStep(parameters, 'Input ' + value['packageShortName'])

        # import module
        parsing_function = Utilities.importModule('Inputs', value['packageShortName'],'Parse')

        # parse code
        code, parameters = parsing_function.Parse.parse(text, parameters)

        # show debug information
        Utilities.showDebugInformation(code, parameters)

        return code, parameters

  return None, parameters
