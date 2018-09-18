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


default_output = '{% if parameters["Outputs"]["RoL"]["indentation"] %}\n{{" " * attributes["depth"]|int}}{% endif %}{{tag}}{% if children|length > 0 or options|length > 0 %}({% if parameters["Outputs"]["RoL"]["indentation"] %}\n{% endif %}{{children|reject("equalto","")|join(\',\')}}{% if options|length > 0 %},{{options.values()|reject("equalto","")|join(", ")}}{% endif %}){% endif %}'

language = {
    'option': {
        'output': {
            'RoL': '{% if children|length > 0 and children[0]!="" %}{% if parameters["Outputs"]["RoL"]["indentation"] %}\n{{" " * attributes["depth"]|int}}{% endif %}{{attributes["name"]}}:{{children[0]}}{% endif %}'
        },
    },
    'function': {
        'output': {
            'RoL': '{% if parameters["Outputs"]["RoL"]["indentation"] %}\n{{" " * attributes["depth"]|int}}{% endif %}{{attributes["name"]}}({% if children|length > 0 or options|length > 0 %}({% if parameters["Outputs"]["RoL"]["indentation"] %}\n{% endif %}{{children|reject("equalto","")|join(\',\')}}{% if options|length > 0 %},{{options.values()|reject("equalto","")|join(", ")}}{% endif %}){% endif %})'
        },
    },
    'variable': {
        'output': {
            'RoL': '{{attributes["name"]}}'
        },
    },
    'element': {
        'output': {
            'RoL': '{{children[0]}} ∈ {{children[1]}}'
        },
    },
    'element': {
        'output': {
            'RoL': '{{children[0]}} ∈ {{children[1]}}'
        },
    },
    'string': {
        'output': {
            'RoL': '\'{{text}}\''
        },
    },
    'natural': {
        'output': {
            'RoL': '{{text}}'
        },
    },
    'real': {
        'output': {
            'RoL': '{{text}}'
        },
    },
    'integer': {
        'output': {
            'RoL': '{{text}}'
        },
    },
    'times': {
        'output': {
            'RoL': '({{children|join(" * ")}})',
        },
    },
    'divide': {
        'output': {
            'RoL': '({{children|join(" / ")}})',
        },
    },
    'plus': {
        'output': {
            'RoL': '({{children|join(" + ")}})',
        },
    },
    'minus': {
        'output': {
            'RoL': '({{children|join(" - ")}})',
        },
    },
    'larger': {
        'output': {
            'RoL': '({{children|join(" > ")}})',
        },
    },
    'smaller': {
        'output': {
            'RoL': '({{children|join(" < ")}})',
        },
    },
    'largerEqual': {
        'output': {
            'RoL': '({{children|join(" ≥ ")}})',
        },
    },
    'smallerEqual': {
        'output': {
            'RoL': '({{children|join(" ≤ ")}})',
        },
    },
    'equal': {
        'output': {
            'RoL': '({{children|join(" ≡ ")}})',
        },
    },
    'notEqual': {
        'output': {
            'RoL': '({{children|join(" ≠ ")}})',
        },
    },
    'and': {
        'output': {
            'RoL': '({{children|join(" ∧ ")}})',
        },
    },
    'or': {
        'output': {
            'RoL': '({{children|join(" ∨ ")}})',
        },
    },
    'not': {
        'output': {
            'RoL': '¬({{children[0]}})',
        },
    },
    'negative': {
        'output': {
            'RoL': '-({{children[0]}})',
        },
    },
    'positive': {
        'output': {
            'RoL': '+({{children[0]}})',
        },
    },
    'assign': {
        'output': {
            'RoL': '({{children[0]}} = {{children[1]}})',
        },
    },
    'anything': {
        'output': {
            'RoL': '',
        },
    },
}
