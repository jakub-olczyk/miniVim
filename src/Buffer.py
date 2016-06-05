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

from Utils import excepted

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
        self.current_line = 0
        self.current_letter = 0

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

    @excepted
    def cursor_left(self):
        """ Move cursor one character to the left """
        if self.current_letter > 0:
            self.current_letter -= 1

    @excepted
    def cursor_right(self):
        """ Move cursor one character to the right """
        if self.current_letter < len(self.main_buffer[self.current_line]):
            self.current_letter += 1

    @excepted
    def cursor_up(self):
        """ Move cursor one line up """
        if self.current_line > 0:
            self.current_line -= 1
        if self.current_letter > len(self.main_buffer[self.current_line]):
            self.current_letter = len(self.main_buffer[self.current_line])

    @excepted
    def cursor_down(self):
        """ Move cursor one line down """
        if self.current_line < len(self.main_buffer) - 1:
            self.current_line += 1
        if self.current_letter > len(self.main_buffer[self.current_line]):
            self.current_letter = len(self.main_buffer[self.current_line])

    def word_fwd(self):
        """ Jump one word forward to the beginning of next word """
        line = self.main_buffer[self.current_line]
        next_word = 0
        x_pos = self.current_letter
        found_next = False
        for i in xrange(x_pos, len(line)):
            if line[i] not in set(' \t\n,.'):
                if found_next: # jeśli to pierwsza litera w słowie
                    next_word = i
                    break # zakończ bo chcemy tylko dolecieć do następnego słowa
            else: # trafiliśmy na biały znak = znajdziemy następne słowo
                found_next = True
        self.current_letter = next_word

    def word_bkwd(self):
        """ Jump one word backward to the beginning """
        line = self.main_buffer[self.current_line]
        prev_word = 0
        x_pos = self.current_letter
        ws_count = 0
        first = True
        for i in xrange(x_pos, 0, -1): #poruszamy się w tył od x do 0
            if line[i] in set(' \n\t,.'):
                if first:
                    ws_count += 1
                    first = False
                if ws_count == 2:
                    prev_word = i+1 # *poprzedni* czyli następny w sekwencji
                    break
            else:
                first = True
        self.current_letter = prev_word
