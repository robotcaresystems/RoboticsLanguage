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
import re
from . import Utilities
from parsley import makeGrammar

# tags that are not type checked
type_atomic = [
    'string',
    'boolean',
    'natural',
    'real',
    'integer',
]

# dictionary tree defining type relations, e.g. a natural is a real, but the oposite may not be true
type_relations_default = {'real': {'integer': {'natural': {}}}}


def makeTypeRelationsGrammar(type_relations):
  '''Traverses a dictionary tree of type relationships and returns a grammar. For
  example, the relationship between reals, integers and naturals results in the grammar:

  real = ( integer | 'real' ) divider
  integer = ( natural | 'integer' ) divider
  natural = 'natural' divider
  '''
  text = ''
  keys = type_relations.keys()

  # for each children
  for type, value in type_relations.iteritems():
    if len(value.keys()) > 0:
      # if children exist, then add relationships to grammar
      text += type + ' = ( ' + '|'.join(value.keys()) + ' | \'' + type + '\' ) divider\n'
    else:
      # if not just define the type
      text += type + ' = \'' + type + '\' divider\n'
    # apply recursively
    recursive_text, recursive_keys = makeTypeRelationsGrammar(value)
    text += recursive_text
    keys += recursive_keys

  return text, keys


@Utilities.cache_function
def arguments(test, tag='nothing', type_relations=type_relations_default):
  """Creates a structure that defines the arguments of a function. Used for type checking.
  For example the operator "plus" has the definitions:

  'plus': {
      'definition': {
          'arguments': arguments('( real real+ | string string+)'),
          'returns': returns('same')
      },
    }

  The string '( real real+ | string string+)' dictates that the arguments of the plus operator
  are either two or more numbers or two or more strings. This function returns a dictionary with
  the keys:
  - documentation: used for printing materials and documentation
  - test: a function that tests a list of argument tags against the 'test' definition in this function
  - tag: a name used to create a tag for this element when creating new elements (e.g. filling in optional parameters)
  """
  if test == 'anything':
    return {'documentation': 'anything', 'test': lambda x: True, 'tag': tag}

  elif test == 'none':
    return {'documentation': '', 'test': lambda x: len(x) == 0, 'tag': tag}

  else:
    # use predefined type relationships
    type_grammar, type_keys = makeTypeRelationsGrammar(type_relations)
    # find new types, and remove duplicated types
    elements = set(re.findall(r'[a-zA-Z]+', test)) - set(type_keys)
    # define the grammar
    type_grammar += "divider = (';'){0,1}\n" + ''.join(["{} = '{}' divider\n".format(x, x) for x in elements])

    grammar = makeGrammar(type_grammar + 'result = (' + test + ')', {})

    # create a argument testing function
    def test_function(x):
      try:
        grammar(';'.join(x)).result()
        return True
      except Exception:
        return False

    return {'documentation': test, 'test': test_function, 'tag': tag}


def optional(name, value):
  '''Creates a structure that defines the optional arguments of a function. Used for type checking.'''

  # create new dictionary
  data = {}
  data['default'] = value
  # add possible cached elements
  data.update(arguments(name, tag=name))

  return data


@Utilities.cache_function
def returns(name):
  '''Creates a return type for a function. Used for type checking.'''
  if name == 'same':
    return lambda x: x[0]
  else:
    return lambda x: name
