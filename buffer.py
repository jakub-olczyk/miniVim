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

from utils import excepted

class Buffer(object):
    ''' This class represents single file open in the editor. It is here for
    making it easier to add support for multiple tabs and editing of several
    files simultaneously '''

    def __init__(self, filename):
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

    @excepted
    def save_file(self, scr):
        '''
        If there is no file_name it will prompt the user for the file_name 
        before saving it.
        '''
        if self.file_name == '':
            scr.addstr(MAX_Y-1,10,'name:')
            self.file_name = str(scr.getstr(MAX_Y-1,15,1024))

        with open('./'+self.file_name,'w+') as f:
            for line in self.main_buffer:
                f.write(line)

    @excepted
    def open_file(self, filename):
        self.file_name = filename
        with open(filename, 'r') as f:
            self.main_buffer = f.readlines()
        
    @excepted
    def cursor_left(self):
        if self.current_letter > 0:
            self.current_letter -= 1

    @excepted
    def cursor_right(self):
        if self.current_letter < len(self.main_buffer[self.current_line]):
            self.current_letter += 1

    @excepted
    def cursor_up(self):
        if self.current_line > 0:
            self.current_line -= 1
        if self.current_letter > len(self.main_buffer[self.current_line]):
            self.current_letter = len(self.main_buffer[self.current_line])

    @excepted
    def cursor_down(self):
        if self.current_line < len(self.main_buffer) - 1 :
            self.current_line += 1
        if self.current_letter > len(self.main_buffer[self.current_line]):
            self.current_letter = len(self.main_buffer[self.current_line])
