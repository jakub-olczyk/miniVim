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

""" This module contains the Cursor class"""

from src.Utils import excepted

class Cursor(object):
    """ This is the abstraction of the cursor that is in the Buffer """

    def __init__(self, _buffer):
        self._nline = 0
        self._ncolumn = 0
        self.main_buffer = _buffer


    @excepted
    def go_left(self):
        """ Move cursor one character to the left """
        if self._ncolumn > 0:
            self._ncolumn -= 1

    @excepted
    def go_right(self):
        """ Move cursor one character to the right """
        if self._ncolumn < len(self.main_buffer[self._nline]):
            self._ncolumn += 1

    @excepted
    def go_up(self):
        """ Move cursor one line up """
        if self._nline > 0:
            self._nline -= 1
        if self._ncolumn > len(self.main_buffer[self._nline]):
            self._ncolumn = len(self.main_buffer[self._nline])

    @excepted
    def go_down(self):
        """ Move cursor one line down """
        if self._nline < len(self.main_buffer) - 1:
            self._nline += 1
        if self._ncolumn > len(self.main_buffer[self._nline]):
            self._ncolumn = len(self.main_buffer[self._nline])

    def word_fwd(self):
        """ Jump one word forward to the beginning of next word """
        line = self.main_buffer[self._nline]
        next_word = 0
        x_pos = self._ncolumn
        found_next = False
        for i in xrange(x_pos, len(line)):
            if line[i] not in set(' \t\n,.'):
                if found_next: # jeśli to pierwsza litera w słowie
                    next_word = i
                    break # zakończ bo chcemy tylko dolecieć do następnego słowa
            else: # trafiliśmy na biały znak = znajdziemy następne słowo
                found_next = True
        self._ncolumn = next_word

    def word_bkwd(self):
        """ Jump one word backward to the beginning """
        line = self.main_buffer[self._nline]
        prev_word = 0
        x_pos = self._ncolumn
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
        self._ncolumn = prev_word
