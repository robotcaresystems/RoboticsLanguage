# -*- coding: utf-8 -*-
#
#   This is the Robotics Language compiler
#
#   ErrorHandling.py: Definition of various messages
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
from RoboticsLanguage.Base.Tools import ErrorHandling

error_exception_functions = {
    # parsley exceptions
    "ometa.runtime.EOFError": {
        'default': lambda e, parameters, **data: ErrorHandling.createErrorMessage(parameters, ErrorHandling.tryMessageInLanguage('eof-error', parameters).title(), e.formatReason(), line=e.input, line_number=0, column_number=e.position)
    },
    "ometa.runtime.ParseError": {
        'default': lambda e, parameters, **data: ErrorHandling.createErrorMessage(parameters, ErrorHandling.tryMessageInLanguage('parsing', parameters).title(), e.formatReason(), line=e.input, line_number=0, column_number=e.position)
    },

    # jinja2 exceptions
    "jinja2.exceptions.TemplateSyntaxError": {
        'default': lambda e, parameters, **data: ErrorHandling.createErrorMessage(parameters, ErrorHandling.tryMessageInLanguage('template-syntax', parameters).title(), e.message, line=ErrorHandling.fileLineNumberToLine(e.filename, e.lineno), line_number=e.lineno, filename=e.filename)
    },
    "jinja2.exceptions.TemplateAssertionError": {
        'default': lambda e, parameters, **data: ErrorHandling.createErrorMessage(parameters, ErrorHandling.tryMessageInLanguage('template-assertion', parameters).title(), e.message, line=ErrorHandling.fileLineNumberToLine(e.filename, e.lineno), line_number=e.lineno, filename=e.filename)
    },

    # system exceptions
    "exceptions.IOError": {
        'default': lambda e, parameters, **data: ErrorHandling.createErrorMessage(parameters, ErrorHandling.tryMessageInLanguage('file-system', parameters).title(), e.strerror),
        'copy-error': lambda e, parameters, **data: ErrorHandling.createErrorMessage(parameters, ErrorHandling.tryMessageInLanguage('copy-error', parameters).title(), ErrorHandling.tryMessageInLanguage('copy-error-reason', parameters).format(data['filename'], data['location'])),

    },

    # lxml exceptions
    "lxml.etree.XMLSyntaxError" : {
      'default': lambda e, parameters, **data: '\n'.join([ErrorHandling.createErrorMessage(parameters, 'Erro' , error.message, line=ErrorHandling.textLineNumberToLine(data['text'], error.line),line_number=error.line, column_number=error.column) for error in e.error_log])
    }
}

error_handling_functions = {}
