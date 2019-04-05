#
#   This is the Robotics Language compiler
#
#   Parse.py: Parses the  language
#
#   Created on: 25 February, 2019
#       Author: Gabriel Lopes
#      Licence: license
#    Copyright: Robot Care Systems BV
#
import sys
import yaml
from lxml import etree
from RoboticsLanguage.Tools import DictionaryToXML
from RoboticsLanguage.Base import Utilities


def parse(text, parameters):
  Utilities.logging.info("Parsing Deep Inference language...")

  # parse JSON into dictionary
  text_dictionary = yaml.safe_load(text)

  # convert dictionary to xml string
  text_xml = DictionaryToXML.dicttoxml(text_dictionary, namespace='di')

  try:
    # create XML object from xml string
    code = etree.fromstring(text_xml)

  except etree.XMLSyntaxError as error:
    Utilities.logErrors(Utilities.formatLxmlErrorMessage(error, text = text),parameters)
    sys.exit(1)

  return code, parameters