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

from commands import Insert, Delete
from utils import excepted, get_input, input_sanitizer
from dispatcher import Dispatcher

"""
Mega uproszczony Vim stworzony jako projekt zaliczeniowy
"""

class Editor(object):
    def __init__(self):
        self.file_name = ""
        self.main_buffer = [] # each string in this list is line of text
        self.command_stack = [] # stack of commands executed 
        self.undo_stack = [] # stack of undone commands for redo(?)
        self.current_line = 0
        self.current_letter = 0

    @excepted
    def undo_last(self):
        last = self.command_stack.pop()
        last.undo()
        self.undo_stack.append(last)

    @excepted
    def redo_last(self):
        last = self.undo_stack.pop()
        last.execute()
        self.command_stack.append(last)

    def execute(self, command):
        command.execute()
        self.command_stack.append(command)

    def print_buffer(self, scr):
        for i,line in enumerate(self.main_buffer):
            scr.addstr(i,0,line)
        if (len(self.main_buffer) - (MAX_Y-1)) < 0:
            for i in xrange((MAX_Y-1) - len(self.main_buffer)):
                scr.addstr(len(self.main_buffer)+i,0,"~")

    @excepted
    def save_file(self, scr):
        if self.file_name == "":
            scr.addstr(MAX_Y-1,10,"name:")
            self.file_name = str(scr.getstr(MAX_Y-1,15,1024))

        with open("./"+self.file_name,'w+') as f:
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
        
    def enter_insert(self):
        curses.echo()
        mb = self.main_buffer
        cli = self.current_line
        clt = self.current_letter
        s = get_input(stdscr, cli, clt)
        s = input_sanitizer(s) # now this is a list of NL ended strings
        for n,line in enumerate(s):
            i = Insert(mb, line, cli+n, clt, clt + len(line))
            ed.execute(i)
        ed.current_letter += len(s[-1])
        ed.current_line += len(s)
        curses.noecho()

    def enter_delete(self):
        cmd = Delete(self.main_buffer, self.current_line, self.current_letter)
        self.execute(cmd)

             
if __name__ == "__main__":
    import os, curses

    ed = Editor()
    stdscr = curses.initscr()
    curses.noecho()
    stdscr.keypad(True)
    curses.cbreak()
    curses.curs_set(2)

    dispatch = Dispatcher(ed)

    MAX_Y, MAX_X = stdscr.getmaxyx()

    stdscr.refresh()

    stdscr.clear()
    stdscr.addstr(MAX_Y-1, MAX_X-5, "{},{}".format(ed.current_line,ed.current_letter), curses.A_REVERSE)
    ed.print_buffer(stdscr)


    while True:
        read = stdscr.getkey()
        #stdscr.addstr(MAX_Y-1, 1, str(read))
        stdscr.refresh()

        dispatch.execute(read)

        if read == ':':
            curses.curs_set(2)
            stdscr.addstr(MAX_Y-1, 2, ":")
            stdscr.refresh()
            curses.echo()
            s = str(stdscr.getstr(MAX_Y-1, 3, 20))

            if s.startswith('q'): #exit and discard
                break

            if s.startswith('w'): #saving command
                ed.save_file(stdscr)
                stdscr.addstr(MAX_Y-1,0,str(ed.file_name) + "Saved")
                stdscr.refresh()

            if s.startswith('x'): #save and exit
                stdscr.addstr(MAX_Y-1,0,"Saving...")
                ed.save_file(stdscr)
                stdscr.refresh()
                break

            if s.startswith('e'): #edit file
                filename = s.split(' ')[1] 
                ed.open_file(filename)

            if s.startswith('p'):
                cmd, arg = s.split(' ')
                arg = int(arg)
                stdscr.addstr(MAX_Y-20,10,ed.main_buffer[arg])

        # Main drawing 
        stdscr.clear()
        # draw the line and letter number
        stdscr.addstr(MAX_Y-1, MAX_X-5, "{},{}".format(ed.current_line,ed.current_letter), curses.A_REVERSE)
        # display last character pressed'
        if read != '\n':
            stdscr.addstr(MAX_Y-1, MAX_X-20, str(read))
        # display the contents of buffer
        ed.print_buffer(stdscr)

        #DEBUG: print the command_stack
        if read == 'KEY_F(2)':
            stdscr.addstr(MAX_Y-1, 0, "cmd_stack: "+str(len(ed.command_stack))) 

        if read == 'KEY_F(3)':
            stdscr.addstr(MAX_Y-1, 0, "undo_stack: " +str(len(ed.undo_stack))) 

        if read == 'KEY_F(4)':
            stdscr.addstr(MAX_Y-1, 0, "main_buffer: " +str(len(ed.main_buffer))) 

        if read == 'KEY_F(5)':
            stdscr.addstr(MAX_Y-20,10,ed.main_buffer[ed.current_line])

        #show cursor on the screen 
        curses.curs_set(2)
        stdscr.refresh()
        curses.setsyx(ed.current_line,ed.current_letter)
        curses.doupdate()
            
    curses.nocbreak()
    stdscr.keypad(False)
    curses.echo()
    curses.endwin()
