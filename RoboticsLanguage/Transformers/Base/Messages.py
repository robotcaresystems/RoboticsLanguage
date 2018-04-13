# -*- coding: utf-8 -*-
#
#   This is the Robotics Language compiler
#
#   Messages.py: Definition of various messages
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

messages = {
    # base messages for error handling
    'default_error_message': {
        'en': 'An error has occured processing error messages. If you are developping a plug-in, please check your `Messages.py` file. If you are not developping a plug-in please contact the developpers of the Robotics Language.',
        'pt': 'Ocurreu um erros no processamento de mensagens. Se esta a desenvolver um module, por favor verifique o ficheiro `Messages.py`. Caso nao estaja a desenvolver um modulo entao contacte a equipa de desenvolvimento da linguagem da robotics.'
    },
    'error-in-file':
    {
        'en': ' in file:\n"{}"\n',
        'pt': ' no ficheiro:\n"{}"\n'
    },
    'error-at-line':
    {
        'en': ' in line {}',
        'pt': ' na linha {}'
    },
    'error-at-column':
    {
        'en': ' column {}',
        'pt': ' coluna {}'
    },
    'error-sentence':
    {
        # The structure of the sentence is the following:
        # 0 - the snipped of code where the error occurs
        # 1 - the error type
        # 2 - the filename
        # 3 - the line number
        # 4 - the column number
        # 5 - the description of the reason of the error
        'en': '{0} {1} error {2} {3} {4}: \033[1m {5} \033[0m',
        'pt': '{0} Erro {1} {2} {3} {4}: \033[1m {5} \033[0m'
    },
    'parsing':
    {
        'en': 'parsing',
        'pt': 'análise'
    },
    'eof-error':
    {
        'en': 'end-of-file',
        'pt': 'fim de ficheiro'
    },
    # other messages
    'template-syntax':
    {
        'en': 'template syntax',
        'pt': 'na sintaxe do modelo'
    },
    'template-assertion':
    {
        'en': 'template assertion',
        'pt': 'na asserção do modelo'
    },
    'file-system':
    {
        'en': 'file system',
        'pt': 'sistema de ficheiros'
    },
    'copy-error':
    {
        'en': 'copy',
        'pt': 'na copia'
    },
    'copy-error-reason':
    {
        'en': 'The file "{}" could not be copied to "{}".',
        'pt': 'Nao foi possivel copiar o ficheiro "{}" para "{}".'
    },
    'xml-syntax':
    {
        'en': 'XML syntax',
        'pt': 'na sintaxe do XML'
    }
}
