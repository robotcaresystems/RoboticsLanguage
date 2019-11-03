#
#   This is the Robotics Language compiler
#
#   Transform.py: AWS Robomaker code transformer
#
#   Created on: 01 November, 2019
#       Author: user name
#      Licence: license
#    Copyright: copyright
#
#   longLicense
#
import os
import shutil

def transform(code, parameters):

  try:
    # Copy examples here
    if parameters['Transformers']['AWSRobomaker']['copyAWSExamplesHere']:
      from_path = os.path.dirname(__file__) + '/Examples'
      here_path = os.getcwd()

      # copytree workaround to ignore existing folders and maintain folder structure. slightly adjusted from here:
      # https://stackoverflow.com/questions/1868714/how-do-i-copy-an-entire-directory-of-files-into-an-existing-directory-using-pyth
      for item in os.listdir(from_path):
        s = os.path.join(from_path, item)
        d = os.path.join(here_path, item)
        if os.path.isdir(s):
          shutil.copytree(s, d)
        else:
          shutil.copy2(s, d)
  except Exception as e:
    print(e)

  return code, parameters
