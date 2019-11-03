#
#   This is the Robotics Language compiler
#
#   Manifesto.py: Definition of the manifesto for this package
#
#   Created on: 01 November, 2019
#       Author: user name
#      Licence: license
#    Copyright: copyright
#
#   longLicense
#
manifesto = {
    'packageName': 'AWS Robomaker',
    'packageShortName': 'AWSRobomaker',
    'order': 100,
    'version': '0.0.0',
    'requiresCode': False,

    'information': {
        'author':
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
        }
    },
    'environments':
    {
        'AWSRobomakerHelloWorld':
        {
            'Transformers': {
                'ROS': {
                    'useSimulationTime': True
                }
            },
            'Outputs':
            {
                'RosCpp':
                {
                    'rosBuildingEngine': 'colcon'
                }
            },
            'globals':
            {
                'output': 'RosCpp',
                'deployOutputs':
                {
                    'RosCpp': '/home/ubuntu/environment/HelloWorld/robot_ws/src'
                }
            }
        }

    }

}
