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

""" Funkcje pomocnicze """

import sys
import traceback

THIS = sys.modules[__name__]
THIS.EXCEPTION_COUNTER = 0

def excepted(func):
    ''' To jest dekorator do łapania wszelkich niepotrzebnych wyjatkow
        dodatkowo ma za zadanie logować wszelkie wyjątki do pliku
    '''
    def func_wrap(*args, **kwargs):
        """ cześć dekoratora """
        try:
            func(*args, **kwargs)
        except StandardError:
            msg = traceback.format_exc()
            with open('vi.log', 'w+' if THIS.EXCEPTION_COUNTER == 0 else 'a') as log:
                log.write(str(THIS.EXCEPTION_COUNTER) + ":" + msg+'\n')
            THIS.EXCEPTION_COUNTER += 1
    return func_wrap

def Singleton(class_):
    ''' Dekorator, który w prosty sposób pozwala na stworzenie Singleton '''
    instances = {} # słownik instancji obiektów, które mają być singletonami
    def getinstance(*args, **kwargs):
        """ cześć dekoratora """
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]
    return getinstance

