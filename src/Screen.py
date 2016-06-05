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

""" This module contains class to communicate with the ``curses'' module """
import curses
import locale
from src.Utils import Singleton

class Screen(object):
    ''' This is abstraction of the user interface. It uses the curses library for
    displaying actual stuff on the screen.'''

    __metaclass__ = Singleton
    locale.setlocale(locale.LC_ALL, '')
    __code = locale.getpreferredencoding()

    def __init__(self, buff=None):
        self.current_buffer = buff
        self.stdscr = curses.initscr()
        self.MAX_Y, self.MAX_X = self.getmaxyx()

        self.stdscr.keypad(True)
        curses.noecho()
        curses.cbreak()
        curses.curs_set(2)

    def destructor(self):
        """ a clean-up function """
        self.stdscr.keypad(False)
        curses.nocbreak()
        curses.echo()
        curses.endwin()

    def draw(self, read):
        ''' Main drawing routine.
        Read is used to display lastpressed character'''
        self.draw_cursor_position() # show y,x position of cursor on the screen
        self.draw_last_pressed(read) # display last character pressed'
        self.print_buffer() # display the contents of buffer
        self.draw_cursor() #show cursor on the screen

    def clear(self):
        """ Clear the Screen """
        self.stdscr.clear()

    def refresh(self):
        """ Refresh the Screen """
        self.stdscr.refresh()

    def getmaxyx(self):
        return self.stdscr.getmaxyx()

    def print_bar(self, message):
        ''' Prints message in the bottom notification bar '''
        curses.echo()
        self.stdscr.addstr(self.MAX_Y - 1, 0, str(message))
        self.refresh()

    def print_buffer(self):
        ''' Show the contents of currently worked on Buffer '''

        for i, line in enumerate(self.current_buffer):
            if i < self.MAX_Y-1:
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
        ''' Show the cursor in its current position '''
        curses.curs_set(2)
        self.stdscr.refresh()
        curses.setsyx(self.current_buffer.current_line, self.current_buffer.current_letter)
        curses.doupdate()

    def draw_cursor_position(self):
        '''
        Clear the screen then draw the coordinates of cursor in current buffer
        '''
        self.clear()
        curr_line = self.current_buffer.current_line
        curr_letter = self.current_buffer.current_letter
        positon = '{},{}'.format(curr_line, curr_letter)
        self.stdscr.addstr(self.MAX_Y-1, self.MAX_X-8, positon, curses.A_REVERSE)

    def draw_last_pressed(self, read):
        ''' Show last pressed character on the bar '''
        if read != '\n':
            self.stdscr.addstr(self.MAX_Y-1, self.MAX_X-20, str(read))

    def normal_mode(self):
        ''' Set screen to not print pressed keys like in normal mode in Vim '''
        curses.noecho()

    def option_mode(self):
        ''' Set screen to be in mode where you enter the commands on commandbar '''
        curses.curs_set(2)
        self.stdscr.addstr(self.MAX_Y-1, 2, ':')
        self.stdscr.refresh()
        curses.echo()

def insert_mode(func):
    ''' Set screen to show the keys pressed and then execute what needs executing '''
    def insert_wrap(*args, **kwargs):
        curses.echo()
        func(*args, **kwargs)
        curses.noecho()
    return insert_wrap

