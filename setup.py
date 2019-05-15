#!/usr/bin/python
#
#   This is the Robotics Language compiler
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
import os
from setuptools import setup, find_packages


long_description = """
The Robotics Language (RoL) is an open extensible domain-specific (or model-based) language for robotics. RoL is an abstraction on top of ROS to efficiently and quickly develop ROS applications using a mathematics-centred language. RoL generates ROS c++ nodes, HTML interfaces, or any other elements.

The base RoL language has a structure similar to standard high-level programming languages

```coffeescript
# A simple topic echo node
node(
  name:'example echo',

  definitions: block(
    # the input signal
    echo_in in Signals(Strings, rosTopic:'/echo/in', onNew: echo_out = echo_in ),

    # the echo signal
    echo_out in Signals(Strings, rosTopic:'/echo/out')
  )
)
```

The power of the RoL is in its ability to integrate mini-abstraction languages:

```coffeescript
# A finite state machine
node(
  name:'example state machine',

  definitions: block(

    # a mini-language: code is defined within `<{ }>`
    FiniteStateMachine<{

      name:machine
      initial:idle

      (idle)-start->(running)-stop->(idle)
      (running)-error->(fault)-reset->(idle)
      (idle)-calibration->(calibrate)-reset->(idle)

    }>,

    # the start signal
    start in Signals(Empty, rosTopic:'/start', onNew: machine.fire('start')),

    # the stop signal
    stop in Signals(Empty, rosTopic:'/stop', onNew: machine.fire('stop'))

  )
)
```
The RoL is in practice an open compiler where users can develop their own languages by means of plug-ins. The RoL is programmed in python and uses XML as the internal abstract syntax tree.
"""

path = os.path.abspath(os.path.dirname(__file__))+'/RoboticsLanguage'
result = [os.path.join(dp, f) for dp, dn, filenames in os.walk(path) for f in filenames]


setup(name='RoboticsLanguage',
      version='0.3.21',
      description='The Robotics Language',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='http://github.com/robotcaresystems/roboticslanguage',
      author='Gabriel A. D. Lopes',
      author_email='g.lopes@rrcrobotics.com',
      license='Apache 2.0',
      packages=find_packages(),
      include_package_data=True,
      package_data={
          'RoboticsLanguage': result
      },
      scripts=['RoboticsLanguage/Scripts/rol',
               'RoboticsLanguage/Scripts/make/rol_make_documentation',
               'RoboticsLanguage/Scripts/docker/ros1/rol_docker',
               'RoboticsLanguage/Scripts/docker/ros1/rol_docker_development',
               'RoboticsLanguage/Scripts/docker/ros2/rol2_docker',
               'RoboticsLanguage/Scripts/docker/ros2/rol2_docker_development',
               ],
      install_requires=[
          'parsley', 'argparse', 'argcomplete', 'jinja2', 'dpath', 'coloredlogs', 'lxml', 'iso-639', 'funcy', 'dill', 'pygments', 'fso', 'pyyaml', 'autopep8', 'cloudpickle', 'coverage'
      ],
      classifiers=[
            'Development Status :: 3 - Alpha',
            'Environment :: Console',
            'Environment :: Web Environment',
            'Intended Audience :: Developers',
            'Intended Audience :: Education',
            'Intended Audience :: Science/Research',
            'License :: OSI Approved :: Apache Software License',
            'Operating System :: OS Independent',
            'Programming Language :: Python :: 2.7',
            'Topic :: Scientific/Engineering',
            'Topic :: Software Development :: Code Generators',
            'Topic :: Software Development :: Compilers'
        ],
      zip_safe=False)
