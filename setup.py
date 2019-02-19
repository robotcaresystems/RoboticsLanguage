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


path = os.path.abspath(os.path.dirname(__file__))
result = [os.path.join(dp, f) for dp, dn, filenames in os.walk(path) for f in filenames]

setup(name='RoboticsLanguage',
      version='0.3.2',
      description='The Robotics Language',
      url='http://github.com/robotcaresystems/roboticslanguage',
      author='Gabriel A. D. Lopes',
      author_email='g.lopes@rrcrobotics.com',
      license='Apache 2.0',
      packages=find_packages(),
      scripts=['RoboticsLanguage/Scripts/rol',
               'RoboticsLanguage/Scripts/make/rol_make_examples',
               'RoboticsLanguage/Scripts/make/rol_make_documentation',
               'RoboticsLanguage/Scripts/tests/rol_run_tests',
               'RoboticsLanguage/Scripts/docker/rol_docker_join',
               'RoboticsLanguage/Scripts/docker/rol_docker_start',
               'RoboticsLanguage/Scripts/docker/rol_docker',
               'RoboticsLanguage/Scripts/docker/rol_2_docker_join',
               'RoboticsLanguage/Scripts/docker/rol_2_docker_start',
               'RoboticsLanguage/Scripts/docker/rol_2_docker'
               ],
      install_requires=[
          'parsley', 'argparse', 'argcomplete', 'jinja2', 'dpath', 'coloredlogs', 'lxml', 'iso-639', 'funcy', 'dill', 'pygments', 'fso', 'pyyaml'
      ],
      include_package_data=True,
      package_data={
          'RoboticsLanguage': result
      },
      zip_safe=False)
