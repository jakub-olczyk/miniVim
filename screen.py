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
'''
Here is all the code that interacts with the curses library.
It uses the Bridge pattern .
'''
import os, curses

class Screen(object):
    ''' This is abstraction of the user interface. It uses the curses library for
    displaying actual stuff on the screen.'''

    def __init__(self, buffer):
        self.current_buffer = buffer
        self.stdscr = curses.initscr()
        self.MAX_Y, self.MAX_X = self.stdscr.getmaxyx()
        
        self.stdscr.keypad(True)
        curses.noecho()
        curses.cbreak()
        curses.curs_set(2)

    def destructor(self):

        self.stdscr.keypad(False)
        curses.nocbreak()
        curses.echo()
        curses.endwin()


    def draw_cursor_position(self):
        '''
        clears the screen
        then draws the cursor position in current buffer
        '''

        self.stdscr.clear()
        curr_line = self.current_buffer.current_line
        curr_letter = self.current_buffer.current_letter
        positon = '{},{}'.format(curr_line,curr_letter)
        self.stdscr.addstr(self.MAX_Y-1, self.MAX_X-5, positon, curses.A_REVERSE)
    
    def print_buffer(self):
        ''' prints the currently open buffer ''' 

        for i, line in enumerate(self.current_buffer):
            self.stdscr.addstr(i, 0, line)
        # fill the screen with '~' if file is shorter then maximal lines on
        # screen
        buffer_len = len(self.current_buffer)
        maximal_lines = self.MAX_Y-1
        difference = buffer_len - maximal_lines
        if difference < 0:
            for i in xrange(abs(difference)):
                self.stdscr.addstr(len(self.current_buffer) + i, 0, '~')

    def normal_mode(self):
        ''' Set screen to be like normal mode in Vim '''
        pass

    def insert_mode(self):
        ''' Set screen to be in insert mode '''
        pass

    def option_mode(self):
        ''' Set screen to be in mode where you enter the commands on commandbar '''
        curses.curs_set(2)
        self.stdscr.addstr(self.MAX_Y-1, 2, ':')
        self.stdscr.refresh()
        curses.echo()
        
 
    def draw(self, read):
        ''' Main drawing routine '''
        self.stdscr.clear()
        # draw the line and letter number
        self.draw_cursor_position()
        # display last character pressed'
        if read != '\n':
            self.stdscr.addstr(self.MAX_Y-1, self.MAX_X-20, str(read))
        # display the contents of buffer
        self.print_buffer()

        # DEBUG keys ↓
        # print the command_stack
        if read == 'KEY_F(2)':
            self.stdscr.addstr(MAX_Y-1, 0, 'cmd_stack: ' + str(len(ed.command_stack))) 

        # print the undo_stack
        if read == 'KEY_F(3)':
            self.stdscr.addstr(MAX_Y-1, 0, 'undo_stack: ' + str(len(ed.undo_stack))) 

        if read == 'KEY_F(4)':
            self.stdscr.addstr(MAX_Y-1, 0, 'main_buffer: ' + str(len(ed.main_buffer))) 

        if read == 'KEY_F(5)':
            self.stdscr.addstr(MAX_Y - 20, 10, self.current_buffer[self.current_line])

        #show cursor on the screen 
        curses.curs_set(2)
        self.stdscr.refresh()
        curses.setsyx(self.current_buffer.current_line, self.current_buffer.current_letter)
        curses.doupdate()
