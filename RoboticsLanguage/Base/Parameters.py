#
#   This is the Robotics Language compiler
#
#   Default Parameters.py: These are the default parameters that are passed to the compiler
#
#   Created on: October 25, 2017
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

import os
from iso639 import languages

parameters = {
    'globals': {
        'version': False,
        'output': 'RosCpp',
        'input': '',
        'debug': False,
        'compile': False,
        'launch': False,
        'beautify': False,
        'verbose': 'none',
        'deployOutputs': {
            'RosCpp': os.path.expanduser('~') + '/catkin_ws/src/',
            'Ros2Cpp': os.path.expanduser('~') + '/ros2_ws/src/'
        },
        'deploy': os.path.expanduser('~') + '/deploy/',
        'plugins': os.path.expanduser('~') + '/.rol/plugins/',
        'RoboticsLanguagePath': os.path.abspath(os.path.dirname(__file__) + '/../') + '/',
        'removeCache': False,
        'language': 'en',
        'compilerLanguage': 'en',
        'loadOrder': [],
        'skipCopyFiles': [],
        'skipTemplateFiles': [],
        'noColours': False
    },

    'developer': {
        'code': False,
        'codePath': '',
        'parameters': False,
        'parametersPath': '',
        'step': 1,
        'stepCounter': 0,
        'stepGroup': '',
        'stepName': '',
        'stop': False,
        'info': False,
        'infoPackage': '',
        'skip': '',
        'ignoreErrors': False,
        'intermediateTemplates': False,
        'progress': False,
        'progressBar': 0,
        'progressTotal': 10,
        'progressPercentage': 0,
        'progressStartTime': 0,
        'showOutputDependency': False
    },

    'symbols':
    {
        'functions': [],
        'variables': [],
        'types': []
    },

    'errors': [],

    'Information':
    {
        'user':
        {
            'name': 'user name',
            'email': 'email@email.edu',
            'web': 'web',
            'telephone': 'user telephone'
        },
        'company':
        {
            'name': 'company name',
            'address': 'company address',
            'zipcode': 'company zipcode',
            'city': 'company city',
            'country': 'company country',
            'email': 'company email',
            'web': 'email@email.edu',
            'telephone': 'company telephone',
            'logo': 'company logo'
        },
        'software':
        {
            'name': 'name',
            'version': '0.0.0',
            'description': 'description',
            'maintainer': {'name': 'name', 'email': 'email@email.edu'},
            'author': {'name': 'name', 'email': 'email@email.edu'},
            'url': 'url',
            'license': 'license',
            'copyright': 'copyright',
            'year': 'year'
        }
    }
}

command_line_flags = {
    'developer:info': {
        'noArgument': True,
        'longFlag': 'info',
        'fileNotNeeded': True,
        'description': 'Shows Rol and package information'
    },
    'developer:infoPackage': {
        'longFlag': 'info-package',
        'fileNotNeeded': True,
        'description': 'Shows information about a specific packages'
    },
    'developer:showOutputDependency': {
        'noArgument': True,
        'longFlag': 'show-output-dependencies',
        'fileNotNeeded': True,
        'description': 'Shows output package dependencies'
    },
    'developer:code': {
        'noArgument': True,
        'flag': 'x',
        'longFlag': 'show-code',
        'description': 'Prints the internal XML representation of the code'
    },
    'developer:codePath': {
        'flag': 'X',
        'longFlag': 'show-code-path',
        'description': 'Prints the internal XML representation of the code for a specific path'
    },
    'developer:parameters': {
        'flag': 'p',
        'longFlag': 'show-parameters',
        'noArgument': True,
        'fileNotNeeded': True,
        'description': 'Prints the internal parameters'
    },
    'developer:parametersPath': {
        'flag': 'P',
        'longFlag': 'show-parameters-path',
        'fileNotNeeded': True,
        'description': 'Prints the internal parameters for a specific path'
    },
    'developer:step': {
        'flag': 's',
        'longFlag': 'show-step',
        'description': 'Prints parameters or code for a specific compiler step'
    },
    'developer:stop': {
        'longFlag': 'show-stop',
        'noArgument': True,
        'description': 'Stops the compiler after the step defined by \'--show-step\''
    },
    'developer:skip': {
        'longFlag': 'skip',
        'description': 'Skip transformer modules',
        'numberArguments': '*'
    },
    'developer:ignoreErrors': {
        'longFlag': 'ignore-errors',
        'noArgument': True,
        'description': 'Ignores errors and attempts to generate code. Result may not compile.'
    },
    'developer:intermediateTemplates': {
        'longFlag': 'show-intermediate-templates',
        'noArgument': True,
        'description': 'Show the intermidiate templates created by the template engine.'
    },
    'developer:progress': {
        'longFlag': 'progress',
        'noArgument': True,
        'description': 'Shows progress.'
    },
    'globals:version': {
        'longFlag': 'version',
        'noArgument': True,
        'fileNotNeeded': True,
        'description': 'Shows the version of the Robotics Language and exit.'
    },
    'globals:output': {
        'flag': 'o',
        'longFlag': 'output',
        'description': 'Outputs',
        'choices': [],
        'numberArguments': '*'
    },
    'globals:input': {
        'flag': 'i',
        'longFlag': 'input',
        'description': 'Use a specific input parser',
        'choices': []
    },
    'globals:debug': {
        'flag': 'd',
        'longFlag': 'debug',
        'noArgument': True,
        'description': 'Turn on debug features for all modules'
    },
    'globals:compile': {
        'flag': 'c',
        'longFlag': 'compile',
        'noArgument': True,
        'description': 'Compiles the output of all modules'
    },
    'globals:beautify': {
        'flag': 'b',
        'longFlag': 'beautify',
        'noArgument': True,
        'description': 'beautifies the output code'
    },
    'globals:verbose': {
        'flag': 'v',
        'longFlag': 'verbose',
        'description': 'Shows verbose information for the compiler and its modules',
        'choices': ['none', 'debug', 'info', 'warn', 'error', 'fatal']
    },
    'globals:launch': {
        'flag': 'l',
        'longFlag': 'launch',
        'noArgument': True,
        'description': 'Launches the output generated by all modules'
    },
    'globals:deploy': {
        'longFlag': 'deploy-path',
        'description': 'The generic path where the generated code is saved'
    },
    'globals:deployOutputs:RosCpp': {
        'longFlag': 'deploy-ros-cpp-path',
        'description': 'The path where the generated ROS code is saved'
    },
    'globals:deployOutputs:Ros2Cpp': {
        'longFlag': 'deploy-ros-2-cpp-path',
        'description': 'The path where the generated ROS 2 code is saved'
    },
    'globals:removeCache': {
        'longFlag': 'remove-cache',
        'noArgument': True,
        'fileNotNeeded': True,
        'description': 'Deletes the compiler cache'
    },
    'globals:noColours': {
        'longFlag': 'no-colours',
        'noArgument': True,
        'description': 'Suppreses syntax highlighting when showing code'
    },
    'globals:language': {
        'longFlag': 'language',
        'description': 'Spoken language used for the robotics language file',
        'choices': languages.part1.keys()
    },
    'globals:compilerLanguage': {
        'longFlag': 'compiler-language',
        'description': 'Spoken language used by the compiler',
        'choices': languages.part1.keys()
    },

    'errors': {'suppress': True},
    'developer:stepCounter': {'suppress': True},
    'developer:stepGroup': {'suppress': True},
    'developer:stepName': {'suppress': True},
    'developer:progressBar': {'suppress': True},
    'developer:progressTotal': {'suppress': True},
    'developer:progressPercentage': {'suppress': True},
    'developer:progressStartTime': {'suppress': True},
    'globals:plugins': {'suppress': True},
    'globals:RoboticsLanguagePath': {'suppress': True},
    'globals:loadOrder': {'suppress': True},
    'globals:skipCopyFiles': {'suppress': True},
    'globals:skipTemplateFiles': {'suppress': True},
    'symbols:functions': {'suppress': True},
    'symbols:variables': {'suppress': True},
    'symbols:types': {'suppress': True},
    'Information:user:name': {'suppress': True},
    'Information:user:email': {'suppress': True},
    'Information:user:web': {'suppress': True},
    'Information:user:telephone': {'suppress': True},
    'Information:company:name': {'suppress': True},
    'Information:company:address': {'suppress': True},
    'Information:company:zipcode': {'suppress': True},
    'Information:company:city': {'suppress': True},
    'Information:company:country': {'suppress': True},
    'Information:company:email': {'suppress': True},
    'Information:company:web': {'suppress': True},
    'Information:company:telephone': {'suppress': True},
    'Information:company:logo': {'suppress': True},
    'Information:software:name': {'suppress': True},
    'Information:software:version': {'suppress': True},
    'Information:software:description': {'suppress': True},
    'Information:software:maintainer': {'suppress': True},
    'Information:software:author': {'suppress': True},
    'Information:software:url': {'suppress': True},
    'Information:software:license': {'suppress': True},
    'Information:software:copyright': {'suppress': True},
    'Information:software:year': {'suppress': True},
    'Information:software:maintainer:name': {'suppress': True},
    'Information:software:maintainer:email': {'suppress': True},
    'Information:software:author:name': {'suppress': True},
    'Information:software:author:email': {'suppress': True}
}
