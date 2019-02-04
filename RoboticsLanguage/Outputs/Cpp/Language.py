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
        'output': {'Cpp': '{{children[0]}}'}
    },

    'Reals': {
        'output':
        {
            'Cpp': '{% if "bits" in options %}{% if options["bits"] == "64"%}double{% else %}float{% endif %}{% else %}float{% endif %}',
        },
    },

    'Integers': {
        'output':
        {
            'Cpp': 'int{% if "bits" in options %}{{options["bits"]}}{% else %}32{% endif %}_t',
        },
    },

    'Naturals': {
        'output':
        {
            'Cpp': 'uint{% if "bits" in options %}{{options["bits"]}}{% else %}32{% endif %}_t',
        },
    },

    'Strings': {
        'output':
        {
            'Cpp': 'std::string',
        },
    },

    'Booleans': {
        'output':
        {
            'Cpp': 'bool',
        },
    },

    'string': {
        'output':
        {
            'Cpp': '"{{text}}"',
        },
    },

    'integer': {
        'output':
        {
            'Cpp': '{% if parameters["Outputs"]["Cpp"]["strict"] %}int({{text}}){% else %}{{text}}{% endif %}',
        },
    },

    'natural': {
        'output':
        {
            'Cpp': '{% if parameters["Outputs"]["Cpp"]["strict"] %}uint({{text}}){% else %}{{text}}{% endif %}',
        },
    },

    'boolean': {
        'output':
        {
            'Cpp': '{{text}}',
        },
    },

    'number': {
        'output':
        {
            'Cpp': '{{text}}',
        },
    },

    'cpp': {
        'output':
        {
            'Cpp': '{{text}}',
        },
    },

    'real': {
        'output':
        {
            'Cpp': '{% if parameters["Outputs"]["Cpp"]["strict"] %}double({{text}}){% else %}{{text}}{% endif %}',
        },
    },


    'set': {
        'output':
        {
            'Cpp': '{% if parentTag=="assign"%}std::tie({{children|join(", ")}}){% else %}set({{children|join(", ")}}){% endif %}'
        },
    },


    'function': {
        'output':
        {
            'Cpp': '{{attributes["name"]}}({{children|join(", ")}})',
        },
    },

    'function_pointer': {
        'output':
        {
            'Cpp': 'std::bind(&{{camelCase(xpath(code,\'/node/option[@name="name"]/string/text()\'))}}Class::{{attributes["name"]}}, this)',
        },
    },


    'return': {
        'output':
        {
            'Cpp': '{% if children|length==1 %}return {{children|first}}{% else %}return std::make_tuple({{children|join(", ")}}){% endif %}'
        },
    },

    'function_definition': {
        'output':
        {
            'Cpp': '',
        },
    },

    'function_arguments': {
        'output':
        {
            'Cpp': '{{children|join(", ")}}',
        },
    },

    'function_content': {
        'output':
        {
            'Cpp': '{{children|join(";\n")}}',
        },
    },

    'function_returns': {
        'output':
        {
            'Cpp': '{% if children|length==0 %}void{% elif children|length==1 %}{{children|first}}{% else %}std::tuple<{{children|join(", ")}}>{% endif %}',
        },
    },

    'assign': {
        'output': {
            'Cpp': '{% if isDefined(parameters,"Transformers/Base/variables/"+children[0]+"/operators/assign/pre/Cpp") %}{{parameters["Transformers"]["Base"]["variables"][children[0]]["operators"]["assign"]["pre"]["Cpp"]|join(";\n")}}{% endif %}{{attributes["preCpp"]}}{{children[0]}}{{attributes["preAssignCpp"]}}={{attributes["postAssignCpp"]}}{{children[1]}}{{attributes["postCpp"]}}{% if isDefined(parameters,"Transformers/Base/variables/"+children[0]+"/operators/assign/post/Cpp") %}{{parameters["Transformers"]["Base"]["variables"][children[0]]["operators"]["assign"]["post"]["Cpp"]|join(";\n")}}{% endif %}'
        },
    },


    'variable': {
        'output':
        {
            'Cpp': '{{attributes["name"]}}{% if "returnDomainCpp" in attributes %}{{attributes["returnDomainCpp"]}}{% endif %}',
        },
    },

    'element': {
        'output':
        {
            'Cpp': '{% if children[1]|length > 0 %}{{children[1]}} {{attribute(code.xpath("variable"),"name")}}{% endif %}'
        },
    },

    'block': {
        'output':
        {
            'Cpp': '{{";\n".join(children)}}'
        },
    },


    'cycle': {
        'output':
        {
            'Cpp': '{{children|join(";\n")}};\n',
        },
    },

    'if': {
        'output':
        {
            'Cpp': 'if({{children[0]}})\n{ {{children[1]}}; }\n {% if children|length>2 %}else \n{ {{children[2]}}; }{% endif %}'
        }
    },

    'print': {
        'output':
        {
            'Cpp': 'std::cout << {{children|join(" << ")}} << std::endl',
        },
    },

    'part': {
        'output':
        {
            'Cpp': '{{children[0]}}[{{children[1]}}]',
        },
    },

    'index': {
        'output':
        {
            'Cpp': '{{children[0]}}',
        },
    },

    'domain': {
        'output':
        {
            'Cpp': '{{children|join(".")}}',
        },
    },

    # math
    'times': {
        'output': {
            'Cpp': '({{children|join(" * ")}})',
        },
    },
    'divide': {
        'output': {
            'Cpp': '({{children|join(" / ")}})',
        },
    },

    'plus': {
        'output': {
            'Cpp': '({{children|join(" + ")}})',
        },
    },
    'minus': {
        'output': {
            'Cpp': '({{children|join(" - ")}})',
        },
    },

    'larger': {
        'output': {
            'Cpp': '({{children|join(" > ")}})',
        },
    },
    'smaller': {
        'output': {
            'Cpp': '({{children|join(" < ")}})',
        },
    },
    'largerEqual': {
        'output': {
            'Cpp': '({{children|join(" >= ")}})',
        },
    },
    'smallerEqual': {
        'output': {
            'Cpp': '({{children|join(" <= ")}})',
        },
    },

    'equal': {
        'output': {
            'Cpp': '({{children|join(" == ")}})',
        },
    },
    'notEqual': {
        'output': {
            'Cpp': '({{children|join(" != ")}})',
        },
    },

    'and': {
        'output': {
            'Cpp': '({{children|join(" && ")}})',
        },
    },
    'or': {
        'output': {
            'Cpp': '({{children|join(" || ")}})',
        },
    },
    'not': {
        'output': {
            'Cpp': '!({{children[0]}})',
        },
    },

    'negative': {
        'output': {
            'Cpp': '-({{children[0]}})',
        },
    },

    'positive': {
        'output': {
            'Cpp': '({{children[0]}})',
        },
    },


}
