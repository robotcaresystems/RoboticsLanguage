#
#   This is the Robotics Language compiler
#
#   Parameters.py: Definition of the parameters for this package
#
#   Created on: 17 August, 2018
#       Author: Gabriel Lopes
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
from RoboticsLanguage.Tools import Serialise


def transform(code, parameters):


  # look for all variables with an assign function
  for variable, value in parameters['Transformers']['Base']['variables'].iteritems():
    if 'assign' in value.keys():
      for assignment in code.xpath('//assign/variable[@name="' + variable + '"]/..'):
        assignment.attrib['assignFunction'] = 'true'

  # # find all relevant outputs
  # package_parents = []
  # for element in Utilities.ensureList(parameters['globals']['output']):
  #   package_parents += Utilities.getPackageOutputParents(parameters, element)
  #
  # # make them unique
  # package_parents = list(set(package_parents))
  #
  # # serialize for each output
  # for language in package_parents:
  #   for xml_child in code.getchildren():
  #     Serialise.serialise(xml_child, parameters, parameters['language'], language)


  for language in Utilities.ensureList(parameters['globals']['output']):
    for xml_child in code.getchildren():
      Serialise.serialise(xml_child, parameters, parameters['language'], language)

  return code, parameters
