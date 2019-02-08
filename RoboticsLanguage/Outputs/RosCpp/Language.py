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


    'RosType': {
        'output':
        {
            'RosCpp': '{{code.getchildren()[0].text|replace("/","::")}}'
        },
    },


    'print': {
        'output':
        {
            'RosCpp': 'ROS_INFO_STREAM({{children|join(" << ")}})',
        },
    },

    'assign': {
        'output': {
            'RosCpp': '{% if isDefined(parameters,"Transformers/Base/variables/"+children[0]+"/operators/assign/pre/Cpp") %}{{parameters["Transformers"]["Base"]["variables"][children[0]]["operators"]["assign"]["pre"]["Cpp"]|join(";\n")}}{% endif %}{{attributes["preRosCpp"]}}{{attributes["preCpp"]}}{{children[0]}}{{attributes["preAssignCpp"]}}={{attributes["postAssignCpp"]}}{{children[1]}}{{attributes["postCpp"]}}{{attributes["postRosCpp"]}}{% if isDefined(parameters,"Transformers/Base/variables/"+children[0]+"/operators/assign/post/Cpp") %}{{parameters["Transformers"]["Base"]["variables"][children[0]]["operators"]["assign"]["post"]["Cpp"]|join(";\n")}}{% endif %}'
        },
    },


}
