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

import os, curses
from utils import Singleton

@Singleton
class Screen(object):
    ''' This is abstraction of the user interface. It uses the curses library for
    displaying actual stuff on the screen.'''

    def __init__(self, buffer):
        self.current_buffer = buffer
        self.stdscr = curses.initscr()
        self.MAX_Y, self.MAX_X = self.getmaxyx()
        
        self.stdscr.keypad(True)
        curses.noecho()
        curses.cbreak()
        curses.curs_set(2)

    def destructor(self):

        self.stdscr.keypad(False)
        curses.nocbreak()
        curses.echo()
        curses.endwin()

    def draw(self, read):
        ''' Main drawing routine '''
        self.draw_cursor_position() # show y,x position of cursor on the screen
        self.draw_last_pressed(read) # display last character pressed'
        self.print_buffer() # display the contents of buffer
        self.draw_cursor() #show cursor on the screen 

    def clear(self):
        self.stdscr.clear()

    def refresh(self):
        self.stdscr.refresh()

    def getmaxyx(self):
        return self.stdscr.getmaxyx()

    def print_bar(self, message):
        ''' Prints message in the bottom bar '''
        curses.echo()
        self.stdscr.addstr(self.MAX_Y - 1, 0, str(message))
        self.refresh()

    def print_buffer(self):
        ''' prints the currently open buffer ''' 

        for i, line in enumerate(self.current_buffer):
            self.stdscr.addstr(i, 0, line)
        self.refresh()
        # fill the screen with '~' if file is shorter then maximal lines on
        # screen
        buffer_len = len(self.current_buffer)
        maximal_lines = self.MAX_Y-1
        difference = buffer_len - maximal_lines
        if difference < 0:
            for i in xrange(abs(difference)):
                self.stdscr.addstr(len(self.current_buffer) + i, 0, '~')

    def draw_cursor(self):
        ''' Show current position of cursor '''
        curses.curs_set(2)
        self.stdscr.refresh()
        curses.setsyx(self.current_buffer.current_line, self.current_buffer.current_letter)
        curses.doupdate()

    def draw_cursor_position(self):
        '''
        clears the screen
        then draws the cursor position in current buffer
        '''
        self.clear()
        curr_line = self.current_buffer.current_line
        curr_letter = self.current_buffer.current_letter
        positon = '{},{}'.format(curr_line,curr_letter)
        self.stdscr.addstr(self.MAX_Y-1, self.MAX_X-8, positon, curses.A_REVERSE)

    def draw_last_pressed(self, read):
        ''' show last pressed character on the bar '''
        if read != '\n':
            self.stdscr.addstr(self.MAX_Y-1, self.MAX_X-20, str(read))
    
    def normal_mode(self):
        ''' Set screen to be like normal mode in Vim '''
        curses.noecho()

    def option_mode(self):
        ''' Set screen to be in mode where you enter the commands on commandbar '''
        curses.curs_set(2)
        self.stdscr.addstr(self.MAX_Y-1, 2, ':')
        self.stdscr.refresh()
        curses.echo()

def insert_mode(func):
    ''' Set screen to be in insert mode then execute what needs executing '''
    def fun_wrap(*args, **kwargs):
        curses.echo()
        func(*args, **kwargs)
        curses.noecho()
    return fun_wrap 

