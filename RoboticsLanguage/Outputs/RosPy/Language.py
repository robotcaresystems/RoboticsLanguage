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
            'RosPy': '{{code.getchildren()[0].text|replace("/",".")}}'
        },
    },


    'print': {
        'output':
        {
            'RosPy': 'rospy.loginfo(str({{children|join(") + str(")}}))',
        },
    },

    'assign': {
        'output': {
            'RosPy': '{% if isDefined(parameters,"Transformers/Base/variables/"+children[0]+"/operators/assign/pre/Python") %}{{parameters["Transformers"]["Base"]["variables"][children[0]]["operators"]["assign"]["pre"]["Python"]|join(";\n")}}{% endif %}{{attributes["preRosPy"]}}{{attributes["prePy"]}}{{children[0]}}{{attributes["preAssignPy"]}}={{attributes["postAssignPy"]}}{{children[1]}}{{attributes["postPy"]}}{{attributes["postRosPy"]}}{% if isDefined(parameters,"Transformers/Base/variables/"+children[0]+"/operators/assign/post/Python") %}{{parameters["Transformers"]["Base"]["variables"][children[0]]["operators"]["assign"]["post"]["Python"]|join(";\n")}}{% endif %}'
        },
    },


}
