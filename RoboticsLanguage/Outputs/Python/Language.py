# -*- coding: utf-8 -*-
#
#   This is the Robotics Language compiler
#
#   Language.py: Definition of the language for this package
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

default_output = ''

language = {

    'option': {
        'output': {'Python': '{{children[0]}}'}
    },

    'Reals': {
        'output':
        {
            'Python': '',
        },
    },

    'Integers': {
        'output':
        {
            'Python': '',
        },
    },

    'Naturals': {
        'output':
        {
            'Python': '',
        },
    },

    'Strings': {
        'output':
        {
            'Python': '',
        },
    },

    'Booleans': {
        'output':
        {
            'Python': '',
        },
    },

    'string': {
        'output':
        {
            'Python': '"{{text}}"',
        },
    },

    'integer': {
        'output':
        {
            'Python': '{% if parameters["Outputs"]["Python"]["strict"] %}int({{text}}){% else %}{{text}}{% endif %}',
        },
    },

    'natural': {
        'output':
        {
            'Python': '{% if parameters["Outputs"]["Python"]["strict"] %}int({{text}}){% else %}{{text}}{% endif %}',
        },
    },

    'boolean': {
        'output':
        {
            'Python': '{{text|title}}',
        },
    },

    'number': {
        'output':
        {
            'Python': '{{text}}',
        },
    },

    'Python': {
        'output':
        {
            'Python': '{{text}}',
        },
    },

    'real': {
        'output':
        {
            'Python': '{% if parameters["Outputs"]["Python"]["strict"] %}float({{text}}){% else %}{{text}}{% endif %}',
        },
    },


    'set': {
        'output':
        {
            'Python': '{% if parentTag=="assign"%}{{children|join(", ")}}{% else %}set({{children|join(", ")}}){% endif %}'
        },
    },


    'function': {
        'output':
        {
            'Python': '{{attributes["name"]}}({{children|join(", ")}})',
        },
    },

    'function_pointer': {
        'output':
        {
            'Python': '{{attributes["name"]}}',
        },
    },


    'return': {
        'output':
        {
            'Python': 'return {{children|join(", ")}}'
        },
    },

    'function_definition': {
        'output':
        {
            'Python': '',
        },
    },

    'function_arguments': {
        'output':
        {
            'Python': '{{children|join(", ")}}',
        },
    },

    'function_content': {
        'output':
        {
            'Python': '{{children|join("\n")}}',
        },
    },

    'function_returns': {
        'output':
        {
            'Python': '',
        },
    },

    'assign': {
        'output': {
            'Python': '{% if isDefined(parameters,"Transformers/Base/variables/"+children[0]+"/operators/assign/pre/Python") %}{{parameters["Transformers"]["Base"]["variables"][children[0]]["operators"]["assign"]["pre"]["Python"]|join("\n")}}{% endif %}{{attributes["prePython"]}}{{children[0]}}{{attributes["preAssignPython"]}}={{attributes["postAssignPython"]}}{{children[1]}}{{attributes["postPython"]}}{% if isDefined(parameters,"Transformers/Base/variables/"+children[0]+"/operators/assign/post/Python") %}{{parameters["Transformers"]["Base"]["variables"][children[0]]["operators"]["assign"]["post"]["Python"]|join("\n")}}{% endif %}'
        },
    },


    'variable': {
        'output':
        {
            'Python': '{{attributes["name"]}}{% if "returnDomainPython" in attributes %}{{attributes["returnDomainPython"]}}{% endif %}',
        },
    },

    'element': {
        'output':
        {
            'Python': '{% if parentTag in ["assign", "function_arguments"]  %}{{attribute(code.xpath("variable"),"name")}}{% endif %}'
        },
    },

    'block': {
        'output':
        {
            'Python': '{{"\n".join(children)}}'
        },
    },


    'cycle': {
        'output':
        {
            'Python': '{{children|join("\n")}}\n',
        },
    },

    'if': {
        'output':
        {
            'Python': 'if {{children[0]}}:\n #>> \n {{children[1]}} \n #<<\n {% if children|length>2 %} else:  \n #>> \n {{children[2]}} \n #<< \n {% endif %}'
        }
    },

    'print': {
        'output':
        {
            'Python': 'print(str({{children|join(") + str(")}}))',
        },
    },

    'part': {
        'output':
        {
            'Python': '{{children[0]}}[{{children[1]}}]',
        },
    },

    'index': {
        'output':
        {
            'Python': '{{children[0]}}',
        },
    },

    'domain': {
        'output':
        {
            'Python': '{{children|join(".")}}',
        },
    },

    # math
    'times': {
        'output': {
            'Python': '({{children|join(" * ")}})',
        },
    },
    'divide': {
        'output': {
            'Python': '({{children|join(" / ")}})',
        },
    },

    'plus': {
        'output': {
            'Python': '({{children|join(" + ")}})',
        },
    },
    'minus': {
        'output': {
            'Python': '({{children|join(" - ")}})',
        },
    },

    'larger': {
        'output': {
            'Python': '({{children|join(" > ")}})',
        },
    },
    'smaller': {
        'output': {
            'Python': '({{children|join(" < ")}})',
        },
    },
    'largerEqual': {
        'output': {
            'Python': '({{children|join(" >= ")}})',
        },
    },
    'smallerEqual': {
        'output': {
            'Python': '({{children|join(" <= ")}})',
        },
    },

    'equal': {
        'output': {
            'Python': '({{children|join(" == ")}})',
        },
    },
    'notEqual': {
        'output': {
            'Python': '({{children|join(" != ")}})',
        },
    },

    'and': {
        'output': {
            'Python': '({{children|join(" and ")}})',
        },
    },
    'or': {
        'output': {
            'Python': '({{children|join(" or ")}})',
        },
    },
    'not': {
        'output': {
            'Python': 'not({{children[0]}})',
        },
    },

    'negative': {
        'output': {
            'Python': '-({{children[0]}})',
        },
    },

    'positive': {
        'output': {
            'Python': '({{children[0]}})',
        },
    },


}
