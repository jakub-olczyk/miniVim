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

"""This is module containing the main abstraction for editor """

from src.Command import Insert, Delete, Replace
from src.Utils import excepted
from src.Dispatcher import Dispatcher
from src.Buffer import Buffer
from src.Settings import Settings
from src.Screen import Screen, insert_mode
from src.Input import Input

class Editor(object):
    '''
    This class represents the editor.
    It is responsible of keeping track of open buffers and commands issued.
    '''
    def __init__(self, file_to_open=''):
        self.running = True

        self.buffers = [Buffer(file_to_open)] # the list of open buffers
        self.current_buffer = self.buffers[0] # first of the buffers
        self.current_cursor = self.current_buffer.cursor

        self.screen = Screen(self.current_buffer)
        self.input = Input()

        self.command_stack = [] # stack of commands executed
        self.undo_stack = [] # stack of undone commands for redo

    @excepted
    def undo_last(self):
        """ Revert to the state that was before executing last Command """
        last = self.command_stack.pop()
        last.undo()
        self.undo_stack.append(last)

    @excepted
    def redo_last(self):
        """ Repeat the last command that was undone """
        last = self.undo_stack.pop()
        last.execute()
        self.command_stack.append(last)

    def execute(self, command):
        """ Execute the given command """
        command.execute()
        self.command_stack.append(command)

    @insert_mode
    def insert(self):
        """ Go to insert mode and execute the Insert Command """
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
        """ insert from the begining of the line """
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
        """ insert at the end of line """
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
        """insert one line below current cursor positon"""
        buff = self.current_buffer
        buff.append('')
        _y = buff.current_line + (1 if len(buff) != 1 else 0)
        _x = len(buff[_y])
        new_buff, cur_y, cur_x = self.input.get(buff, _y, _x)
        self.current_buffer.current_line = cur_y
        self.current_buffer.current_letter = cur_x
        i = Insert(buff, new_buff)
        self.execute(i)
        self.debug_buffer()

    def delete_move(self):
        """delete with movement command"""
        buff = self.current_buffer
        letter = self.input.getkey() # get the move key
        _del = Delete(buff, letter)
        self.execute(_del)

    def delete_to_end(self):
        """ delete from current positon to end of line """
        cmd = Delete(self.current_buffer, 'D')
        self.execute(cmd)

    def replace(self):
        """ Execute the Replace Command """
        result = self.input.prompt_bar('s/')
        try:
            old, new = result.split('/')
        except ValueError:
            old, new, _ = result.split('/')
        cmd = Replace(self.current_buffer, old, new, self.current_buffer.current_line)
        self.execute(cmd)

    def settings(self):
        """open editor settings changer"""
        _s = self.input.prompt_bar(":")
        setting = Settings(self)
        setting.execute(_s)

    def debug_buffer(self):
        """ save to file the debug information """
        with open("debug_editor", "w") as debug:
            debug.write(str(self.current_buffer))
            debug.write("EOF")

    def start(self):
        """ Main method that starts the READ-EVAL-DRAW loop that editor uses to work properly"""
        dispatcher = Dispatcher(self)
        self.screen.draw('') # we need to add the empty character
        try:
            while self.running:
                read = self.input.getkey()
                dispatcher.execute(read)
                self.screen.draw(read)
        except RuntimeError:
            self.screen.destructor() # do the cleanup, even if there was some problem with the app
        self.screen.destructor() # needs cleaning to be more Pythonic
