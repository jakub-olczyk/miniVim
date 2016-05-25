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
from utils import excepted
from dispatcher import Dispatcher
from buffer import Buffer
from screen import Screen, insert_mode
from input import Input,  input_sanitizer

''' Mega uproszczony Vim stworzony jako projekt zaliczeniowy '''

class Editor(object):
    ''' 
    This class represents the editor. 
    It is responsible of keeping track of open files and commands issued.
    '''
    def __init__(self):
        self.running = True

        self.buffers = [Buffer('')] # the list of open buffers
        self.current_buffer = self.buffers[0]

        self.screen = Screen(self.current_buffer)
        self.input = Input()

        self.command_stack = [] # stack of commands executed 
        self.undo_stack = [] # stack of undone commands for redo

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
        
    @insert_mode
    def enter_insert(self): # FIX THIS : separate model and view
        #self.current_buffer.sanitize()
        mb = self.current_buffer
        cli = mb.current_line
        clt = mb.current_letter
        new_buff = self.input.get(mb, cli, clt) # WIP on FIXing THIS!
        #s = input_sanitizer(s)
        i = Insert(mb, new_buff)
        ed.execute(i)
        #self.current_buffer.current_letter += len(s[-1])
        #self.current_buffer.current_line += len(s)

    def enter_delete(self):
        cmd = Delete(self.current_buffer)
        self.execute(cmd)

    def settings(self):
        #self.screen.option_mode() # enter option mode and show it by printing prompt ":"
        s = self.input.prompt_bar(":")

        if s.startswith('q'): #exit and discard
            self.running = False

        if s.startswith('w'): #saving command
            if self.current_buffer.file_name == '':
                self.current_buffer.file_name = self.input.prompt_bar('name:')
            self.current_buffer.save_file(self.screen.stdscr) #broken
            self.screen.print_bar(self.current_buffer.file_name + ': Saved')

        if s.startswith('x'): #save and exit
            self.stdscr.addstr(self.screen.MAX_Y-1,0,'Saving...')
            self.current_buffer.save_file(stdscr) #broken
            self.stdscr.refresh()
            self.running = False

        if s.startswith('e'): #edit file
            filename = s.split(' ')[1] # FIX : no argument?
            self.current_buffer.open_file(filename)

        if s.startswith('p'):
            cmd, arg = s.split(' ')
            arg = int(arg)
            stdscr.addstr(self.screen.MAX_Y-20,10, self.current_buffer[arg])

    def debug_buffer(self):
        with open("debug_editor", "w") as debug:
            debug.write(str(self.current_buffer))
            debug.write("EOF")

    def start(self):
        dispatcher = Dispatcher(self)
        self.screen.draw('')
        while self.running:
            read = self.input.getkey()
            dispatcher.execute(read)
            self.screen.draw(read) 
        self.screen.destructor() # needs cleaning to be more Pythonic

if __name__ == '__main__':
    ed = Editor()
    ed.start()
