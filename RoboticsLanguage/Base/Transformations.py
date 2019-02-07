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

import sys
from . import Utilities


@Utilities.cache_in_disk
def prepareTransformations(parameters):

  transformers = parameters['manifesto']['Transformers']

  return [{'data': transformers[x], 'name': x} for x in sorted(transformers, key=lambda k: transformers[k]['order'])]


def Apply(code, parameters):
  """Applies transformations to the XML structure"""

  # load the list of transformations by order
  ordered_transformations_list = prepareTransformations(parameters)

  # load the transform modules
  transform_function_list = [Utilities.importModule(t['data']['type'],
                                                    'Transformers', t['name'], 'Transform')
                             for t in ordered_transformations_list]

  # apply transformations
  for transform_function, transform_name in zip(transform_function_list, [x['name'] for x in ordered_transformations_list]):

    if transform_name not in parameters['developer']['skip']:

      # Checks if the plugin can run without code
      if (code is not None) or (code is None and 'requiresCode' in parameters['manifesto']['Transformers'][transform_name].keys() and not parameters['manifesto']['Transformers'][transform_name]['requiresCode']):

        # update the compiler step
        parameters = Utilities.incrementCompilerStep(parameters, 'Transformers', transform_name)

        # apply transformations
        code, parameters = transform_function.Transform.transform(code, parameters)

        # show developer information
        Utilities.showDeveloperInformation(code, parameters)

  # check if semantic errors have occured
  if len(parameters['errors']) > 0:
    Utilities.logging.error("Semantic errors found! Stopping.")
    sys.exit(1)

  return code, parameters
