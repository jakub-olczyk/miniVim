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

from Command import Insert, Delete, Replace
from Utils import excepted
from Dispatcher import Dispatcher
from Buffer import Buffer
from Screen import Screen, insert_mode
from Input import Input

''' Mega uproszczony Vim stworzony jako projekt zaliczeniowy '''

class Editor(object):
    ''' 
    This class represents the editor. 
    It is responsible of keeping track of open buffers and commands issued.
    '''
    def __init__(self):
        self.running = True

        self.buffers = [Buffer('')] # the list of open buffers
        self.current_buffer = self.buffers[0] # first of the buffers

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
    def insert(self): 
        buff = self.current_buffer
        cursor_y = buff.current_line
        cursor_x = buff.current_letter
        new_buff, cursor_y, cursor_x = self.input.get(buff, cursor_y, cursor_x) 
        self.current_buffer.current_line = cursor_y
        self.current_buffer.current_letter = cursor_x
        i = Insert(buff, new_buff)
        self.execute(i)

    @insert_mode
    def insert_start(self):
        buff = self.current_buffer
        cur_y = buff.current_line
        cur_x = buff.current_letter
        cur_x = 0
        new_buff, cur_y, cur_x = self.input.get(buff, cur_y, cur_x)
        self.current_buffer.current_line = cur_y
        self.current_buffer.current_letter = cur_x
        i = Insert(buff, new_buff)
        self.execute(i)

    @insert_mode
    def insert_end(self):
        buff = self.current_buffer
        cur_y = buff.current_line
        cur_x = buff.current_letter
        cur_x = len(buff[cur_y])
        new_buff, cur_y, cur_x = self.input.get(buff, cur_y, cur_x)
        self.current_buffer.current_line = cur_y
        self.current_buffer.current_letter = cur_x
        i = Insert(buff, new_buff)
        self.execute(i)

    @insert_mode
    def insert_below(self):
        buff = self.current_buffer
        buff.append('')
        y = buff.current_line + (1 if len(buff) != 1 else 0)
        x = len(buff[y])
        new_buff, cur_y, cur_x = self.input.get(buff, y, x)
        self.current_buffer.current_line = cur_y
        self.current_buffer.current_letter = cur_x
        i = Insert(buff, new_buff)
        self.execute(i)
        self.debug_buffer()

    def delete_move(self):
        buff = self.current_buffer
        curr_line = buff.current_line
        curr_letter = buff.current_letter
        letter = self.input.getkey()
        d = Delete(buff, letter)
        self.execute(d)

    def delete_to_end(self):
        cmd = Delete(self.current_buffer, 'D') 
        self.execute(cmd)

    def replace(self):
        old, new = self.input.prompt_bar('s/').split('/')
        cmd = Replace(self.current_buffer, old, new, self.current_buffer.current_line)
        self.execute(cmd)

    def settings(self):
        s = self.input.prompt_bar(":")

        if s.startswith('q'): #exit and discard
            self.running = False

        if s.startswith('w'): #saving command
            if self.current_buffer.file_name == '':
                self.current_buffer.file_name = self.input.prompt_bar('name:')
            self.current_buffer.save_file() 
            self.screen.print_bar(self.current_buffer.file_name + ': Saved')

        if s.startswith('x'): #save and exit
            self.screen.stdscr.addstr(self.screen.MAX_Y-1,0,'Saving...')
            self.current_buffer.save_file()
            self.screen.stdscr.refresh()
            self.running = False

        if s.startswith('e'): #edit file
            args = s.split(' ')
            filename = ''
            try:
                filename = args[1]
            except:
                pass
            self.current_buffer.open_file(filename)

        if s.startswith('p'): # undocumented feature used for debugging
            cmd, arg = s.split(' ')
            arg = int(arg)
            self.screen.stdscr.addstr(self.screen.MAX_Y-20,10, self.current_buffer[arg])

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
