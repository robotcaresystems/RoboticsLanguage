#
#   This is the Robotics Language compiler
#
#   Outputs.py: Generates the outputs
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


@Utilities.cache_in_disk
def prepareOutputs(parameters):

  outputs = parameters['manifesto']['Outputs']

  return [{'data': outputs[x], 'name': x} for x in sorted(outputs, key=lambda k: outputs[k]['order'])]


def Generate(code, parameters):
  """Generates the outputs"""

  outputs = parameters['globals']['output']

  # get a list of the outputs soted by order
  sorted_outputs = prepareOutputs(parameters)

  for output in map(lambda k: k['name'], sorted_outputs):

    if output in outputs:

      # Checks if the plugin can run without code
      if (code is not None) or (code is None and 'requiresCode' in parameters['manifesto']['Outputs'][output].keys() and not parameters['manifesto']['Outputs'][output]['requiresCode']):

        # update the compiler step
        parameters = Utilities.incrementCompilerStep(parameters, 'Outputs', output)

        # load the module
        output_function = Utilities.importModule(
            parameters['manifesto']['Outputs'][output]['type'], 'Outputs', output, 'Output')

        # apply transformations
        output_function.Output.output(code, parameters)

        # show developer information
        Utilities.showDeveloperInformation(code, parameters)

  # show final message
  if parameters['developer']['progress']:
    Utilities.progressDone(parameters)
