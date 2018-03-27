# -*- coding: utf-8 -*-
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



# from googletrans import Translator
# translator = Translator()
# result = translator.translate('안녕하세요.')
#
#  # https://translate.googleapis.com/translate_a/single?client=gtx&sl={0}&tl={1}&dt=t&q={2}

def sentence(s,language):
  if s in sentences_list.keys():
    if language in sentences_list[s]:
      return sentences_list[s][language]
  return s


sentences_list = {
 'the following files have unknown formal': {
   'pt':'os ficheiros seguintes têm um formato desconhecido'
 }
}
