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
        'output': {'Ros2Cpp': '{{children[0]}}'}
    },

    'Reals': {
        'output':
        {
            'Ros2Cpp': '{% if "bits" in options %}{% if options["bits"] == "64"%}double{% else %}float{% endif %}{% else %}float{% endif %}',
        },
    },

    'Integers': {
        'output':
        {
            'Ros2Cpp': 'int{% if "bits" in options %}{{options["bits"]}}{% else %}32{% endif %}_t',
        },
    },

    'Naturals': {
        'output':
        {
            'Ros2Cpp': 'uint{% if "bits" in options %}{{options["bits"]}}{% else %}32{% endif %}_t',
        },
    },

    'Strings': {
        'output':
        {
            'Ros2Cpp': 'std::string',
        },
    },

    'Booleans': {
        'output':
        {
            'Ros2Cpp': 'bool',
        },
    },

    'string': {
        'output':
        {
            'Ros2Cpp': '"{{text}}"',
        },
    },

    'integer': {
        'output':
        {
            'Ros2Cpp': '{% if parameters["Outputs"]["Ros2Cpp"]["strict"] %}int({{text}}){% else %}{{text}}{% endif %}',
        },
    },

    'natural': {
        'output':
        {
            'Ros2Cpp': '{% if parameters["Outputs"]["Ros2Cpp"]["strict"] %}uint({{text}}){% else %}{{text}}{% endif %}',
        },
    },

    'boolean': {
        'output':
        {
            'Ros2Cpp': '{{text}}',
        },
    },

    'number': {
        'output':
        {
            'Ros2Cpp': '{{text}}',
        },
    },

    'cpp': {
        'output':
        {
            'Ros2Cpp': '{{text}}',
        },
    },

    'real': {
        'output':
        {
            'Ros2Cpp': '{% if parameters["Outputs"]["Ros2Cpp"]["strict"] %}double({{text}}){% else %}{{text}}{% endif %}',
        },
    },


    'set': {
        'output':
        {
            'Ros2Cpp': '{% if parentTag=="assign"%}std::tie({{children|join(", ")}}){% else %}set({{children|join(", ")}}){% endif %}'
        },
    },


    'function': {
        'output':
        {
            'Ros2Cpp': '{{attributes["name"]}}({{children|join(", ")}})',
        },
    },

    'function_pointer': {
        'output':
        {
            'Ros2Cpp': 'std::bind(&{{camelCase(xpath(code,\'/node/option[@name="name"]/string/text()\'))}}Class::{{attributes["name"]}}, this)',
            # 'Ros2Cpp': '&(this->{{attributes["name"]}})',
        },
    },


    'return': {
        'output':
        {
            'Ros2Cpp': '{% if children|length==1 %}return {{children|first}}{% else %}return std::make_tuple({{children|join(", ")}}){% endif %}'
        },
    },

    'function_definition': {
        'output':
        {
            'Ros2Cpp': '{% set returns = attribute(xpaths(code,"function_returns"),"Ros2Cpp") %}{% if returns=="" %}void{% else %}{{returns}}{% endif %} {{attributes["name"]}}({{attribute(xpaths(code,"function_arguments"),"Ros2Cpp")}})',
        },
    },

    'function_arguments': {
        'output':
        {
            'Ros2Cpp': '{{children|join(", ")}}',
        },
    },

    'function_content': {
        'output':
        {
            'Ros2Cpp': '{{children|join(";\n")}}',
        },
    },

    'function_returns': {
        'output':
        {
            'Ros2Cpp': '{% if children|length==0 %}void{% elif children|length==1 %}{{children|first}}{% else %}std::tuple<{{children|join(", ")}}>{% endif %}',
        },
    },

    'assign': {
        'output': {
            'Ros2Cpp': '{{attributes["preRos2Cpp"]}}{{children[0]}}{{attributes["preAssignRos2Cpp"]}}={{attributes["postAssignRos2Cpp"]}}{{children[1]}}{{attributes["postRos2Cpp"]}}'
            # ,
            #
            # 'Ros2Cpp2': '{% if "assignFunction" in attributes %}{{children[0]}}_assign({{children[1]}}){% else %}{{children[0]}}{% if "assignDomain" in attributes %}{{attributes["assignFunction"]}}{% endif %} = {{children[1]}}{% endif %}',
        },
    },


    'variable': {
        'output':
        {
            'Ros2Cpp': '{{attributes["name"]}}{% if "returnDomainRos2Cpp" in attributes %}{{attributes["returnDomainRos2Cpp"]}}{% endif %}',
        },
    },

    'element': {
        'output':
        {
            'Ros2Cpp': '{% if children[1]|length > 0 %}{{children[1]}} {{attribute(code.xpath("variable"),"name")}}{% endif %}'
        },
    },

    'block': {
        'output':
        {
            'Ros2Cpp': '{{";\n".join(children)}}'
        },
    },


    'RosType': {
        'output':
        {
            'Ros2Cpp': '{{code.getchildren()[0].text|replace("/","::")}}'
        },
    },


    'cycle': {
        'output':
        {
            'Ros2Cpp': '{{children|join(";\n")}};\n',
        },
    },

    'if': {
        'output':
        {
            'Ros2Cpp': 'if({{children[0]}})\n{ {{children[1]}}; }\n {% if children|length>2 %}else \n{ {{children[2]}}; }{% endif %}'
        }
    },

    'print': {
        'output':
        {
            'Ros2Cpp': 'std::cout << {{children|join(" << ")}} << std::endl',
        },
    },

    'part': {
        'output':
        {
            'Ros2Cpp': '{{children[0]}}[{{children[1]}}]',
        },
    },

    'index': {
        'output':
        {
            'Ros2Cpp': '{{children[0]}}',
        },
    },

    'domain': {
        'output':
        {
            'Ros2Cpp': '{{children|join(".")}}',
        },
    },

    # math
    'times': {
        'output': {
            'Ros2Cpp': '({{children|join(" * ")}})',
        },
    },
    'divide': {
        'output': {
            'Ros2Cpp': '({{children|join(" / ")}})',
        },
    },

    'plus': {
        'output': {
            'Ros2Cpp': '({{children|join(" + ")}})',
        },
    },
    'minus': {
        'output': {
            'Ros2Cpp': '({{children|join(" - ")}})',
        },
    },

    'larger': {
        'output': {
            'Ros2Cpp': '({{children|join(" > ")}})',
        },
    },
    'smaller': {
        'output': {
            'Ros2Cpp': '({{children|join(" < ")}})',
        },
    },
    'largerEqual': {
        'output': {
            'Ros2Cpp': '({{children|join(" >= ")}})',
        },
    },
    'smallerEqual': {
        'output': {
            'Ros2Cpp': '({{children|join(" <= ")}})',
        },
    },

    'equal': {
        'output': {
            'Ros2Cpp': '({{children|join(" == ")}})',
        },
    },
    'notEqual': {
        'output': {
            'Ros2Cpp': '({{children|join(" != ")}})',
        },
    },

    'and': {
        'output': {
            'Ros2Cpp': '({{children|join(" && ")}})',
        },
    },
    'or': {
        'output': {
            'Ros2Cpp': '({{children|join(" || ")}})',
        },
    },
    'not': {
        'output': {
            'Ros2Cpp': '!({{children[0]}})',
        },
    },

    'negative': {
        'output': {
            'Ros2Cpp': '-({{children[0]}})',
        },
    },

    'positive': {
        'output': {
            'Ros2Cpp': '({{children[0]}})',
        },
    },

}
