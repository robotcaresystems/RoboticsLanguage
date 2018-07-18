#
#   This is the Robotics Language compiler
#
#   Transformations.py: Applies transformations to the XML structure
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
import sys


@Utilities.cache
def prepareTransformations(parameters):
  # get the list of transformations
  transformations_list = {x: y['order'] for x, y in parameters['manifesto']['Transformers'].iteritems()}

  # sort them according to the desired order
  ordered_transformations_list = sorted(transformations_list, key=transformations_list.__getitem__)

  return ordered_transformations_list


def Apply(code, parameters):
  """Applies transformations to the XML structure"""

  # fill in defaults in optional arguments
  code, parameters = Utilities.fillDefaultsInOptionalArguments(code, parameters)

  # first do all semantic checking
  code, parameters = Utilities.semanticChecking(code, parameters)

  # load the list of transformations by order
  ordered_transformations_list = prepareTransformations(parameters)

  # load the transform modules
  transform_function_list = [Utilities.importModule('Transformers', t, 'Transform')
                             for t in ordered_transformations_list]

  # apply transformations
  for transform_function, transform_name in zip(transform_function_list, ordered_transformations_list):

    # update the compiler step
    parameters = Utilities.incrementCompilerStep(parameters, 'Transforming ' + transform_name)

    # apply transformations
    code, parameters = transform_function.Transform.transform(code, parameters)

    # show debug information
    Utilities.showDebugInformation(code, parameters)

  # serialize for each output
  for language in Utilities.ensureList(parameters['globals']['output']):
    for xml_child in code.getchildren():
      Utilities.serialise(xml_child, parameters, parameters['language'], language)

  # check if semantic errors have occured
  if len(parameters['errors']) > 0:
    Utilities.logging.error("Semantic errors found! Stopping.")
    sys.exit(1)

  return code, parameters
