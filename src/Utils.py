# coding=utf8
#    miniVim
#    Copyright (c) Jakub Olczyk
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

""" Helper functions, classes and what-not """

import sys
import traceback

THIS = sys.modules[__name__]
THIS.EXCEPTION_COUNTER = 0

class Singleton(type):
    ''' A class that should be used as __metaclass__ for other classes '''
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


def excepted(func):
    ''' This decorator is used to catch all exceptions and then log them '''
    def excepted_wrapper(*args, **kwargs):
        """ This is the part of @excepted that does the logging """
        try:
            func(*args, **kwargs)
        except StandardError:
            msg = traceback.format_exc()
            with open('vi.log', 'w+' if THIS.EXCEPTION_COUNTER == 0 else 'a') as log:
                log.write(str(THIS.EXCEPTION_COUNTER) + ":" + msg+'\n')
            THIS.EXCEPTION_COUNTER += 1
    return excepted_wrapper 



