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
import sys

this = sys.modules[__name__]

this.EXCEPTION_COUNTER = 0

def excepted(func):
    ''' To jest dekorator do łapania wszelkich niepotrzebnych wyjatkow 
        dodatkowo ma za zadanie logować wszelkie wyjątki do pliku
    '''
    def func_wrap(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except:
            e = sys.exc_info()
            msg = str(e) + str(e[2])
            with open('vi.log', 'w+' if this.EXCEPTION_COUNTER == 0 else 'a') as log:
                log.write(str(this.EXCEPTION_COUNTER) + ":" + msg+'\n')
            # pass # Here should be some sort of logging given the amount of
                 # functions that uses this decorator
            this.EXCEPTION_COUNTER += 1
    return func_wrap 

def Singleton(class_):
    ''' Dekorator, który w prosty sposób pozwala na stworzenie Singleton '''
    instances = {} # słownik instancji obiektów, które mają być singletonami
    def Instance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]
    return Instance

