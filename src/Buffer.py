#!/usr/bin/env python
# coding=utf8
#
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

""" This is the module with main model for file that is being worked on """

from src.Utils import excepted
from src.Cursor import Cursor

class Buffer(object):
    ''' This class represents single file open in the editor. It is here for
    making it easier to add support for multiple tabs and editing of several
    files simultaneously .
    Kinda mimics the work of Python's list. '''

    def __init__(self, filename=''):
        '''
        @filename: the name of the file to be opened, visit doc for open to know more
        '''
        self.file_name = filename
        self.main_buffer = []
        if filename != '':
            self.open_file(self.file_name)
        self.cursor = Cursor(self.main_buffer)

    def __iter__(self):
        return iter(self.main_buffer)

    def __len__(self):
        return len(self.main_buffer)

    def __str__(self):
        return str(self.main_buffer)

    # support indexing
    def __getitem__(self, index):
        return self.main_buffer[index]

    def __setitem__(self, index, value):
        self.main_buffer[index] = value

    def append(self, string):
        """ interface to underlying structure of list """
        self.main_buffer.append(string)

    def insert(self, index, value):
        """ interface to underlying list """
        self.main_buffer.insert(index, value)

    def remove(self, value):
        """ remove first occurance of value. Raises ValueError when no value is
        present """
        self.main_buffer.remove(value)

    def count(self, obj):
        """ Access to list method """
        return self.main_buffer.count(obj)

    @excepted
    def save_file(self):
        """
        Expects that there is a self.file_name defined!
        """
        assert (self.file_name != ''), "Filename cannot be empty!"
        with open('./'+self.file_name, 'w+') as _file:
            for line in self.main_buffer:
                _file.write(line+'\n')

    @excepted
    def open_file(self, filename):
        """ A method used to load file to RAM """
        self.file_name = filename
        with open(filename, 'r') as _file:
            #self.main_buffer = _file.readlines()
            self.main_buffer = []
            for line in _file.readlines():
                self.main_buffer.append(line.rstrip())

    ############ Code for compatibility reasons with older part of the application
    @property
    def current_line(self):
        return self.cursor._nline

    @current_line.setter
    def current_line(self, value):
        self.cursor._nline = value

    @property
    def current_letter(self):
        return self.cursor._ncolumn

    @current_letter.setter
    def current_letter(self, value):
        self.cursor._ncolumn = value
    ############ Compatibility code end
