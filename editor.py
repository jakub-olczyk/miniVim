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
from dispatcher import Dispatcher, enter_insert_o
from buffer import Buffer
from screen import Screen

''' Mega uproszczony Vim stworzony jako projekt zaliczeniowy '''

class Editor(object):
    ''' 
    This class represents the editor. 
    It is responsible of keeping track of open files and commands issued.
    '''
    def __init__(self):
        self.buffers = [Buffer('')] # the list of open buffers
        self.current_buffer = self.buffers[0]
        self.screen = Screen(self.current_buffer)
        self.command_stack = [] # stack of commands executed 
        self.undo_stack = [] # stack of undone commands for redo
        self.commands = {
                'h': self.current_buffer.cursor_left,
                'l': self.current_buffer.cursor_right,
                'j': self.current_buffer.cursor_down,
                'k': self.current_buffer.cursor_up,
                'i': self.enter_insert,
                # 'o': lambda: enter_insert_o(ed), #FIXME
                'd': self.enter_delete,
                'u': self.undo_last,
                'r': self.redo_last
            }

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
        
    def enter_insert(self): # FIX THIS : separate model and view
        curses.echo()
        mb = self.current_buffer
        cli = self.mb.current_line
        clt = self.mb.current_letter
        s = get_input(stdscr, cli, clt) # FIX this!!!
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

    def start(self):
        normal_dispatcher = Dispatcher(self)
        self.screen.print_buffer()
        
        while True:
            read = self.screen.stdscr.getkey()
            normal_dispatcher.execute(read)

            # This is broken
            if read == ':':
                self.screen.option_mode() # enter option mode and show it 
                s = str(self.screen.stdscr.getstr(self.screen.MAX_Y-1, 3, 20)) # Ugly but works FIX ME

                if s.startswith('q'): #exit and discard
                    break

                if s.startswith('w'): #saving command
                    self.current_buffer.save_file(stdscr) #broken
                    stdscr.addstr(MAX_Y-1,0,str(ed.file_name) + 'Saved')
                    stdscr.refresh()

                if s.startswith('x'): #save and exit
                    stdscr.addstr(MAX_Y-1,0,'Saving...')
                    ed.save_file(stdscr)
                    stdscr.refresh()
                    break

                if s.startswith('e'): #edit file
                    filename = s.split(' ')[1] 
                    self.current_buffer.open_file(filename)

                if s.startswith('p'):
                    cmd, arg = s.split(' ')
                    arg = int(arg)
                    stdscr.addstr(MAX_Y-20,10,ed.main_buffer[arg])

            self.screen.draw(read) 
        self.screen.destructor() # needs cleaning to be more Pythonic

if __name__ == '__main__':
    ed = Editor()
    ed.start()

