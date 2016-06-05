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

""" An abstraction for managing settings used in Editor """

from src.Screen import Screen
from src.Input import Input
from src.Utils import excepted

class Settings(object):
    """ Class used to group the code needed to set some settings in Editor """

    def __init__(self, editor):
        self.editor = editor
        self.screen = Screen()
        self.input = Input()
        self.action = {
            'q': self.action_quit,
            'w': self.action_write,
            # below we play on the fact that normally functions always return falsish stuff
            # so we just use it in boolean context and execute to "void" functions in one lambda
            # dirty hack to not make more functions than needed
            'x': lambda: self.action_write() or self.action_quit(),
            'e': self.action_edit
                 #'p': self.action_print_debug
        }

    @excepted
    def execute(self, desc):
        """ Execute action according to the command [desc]ription """
        desc = desc[0] # take only the first letter
        cmd = self.action[desc]
        cmd()

    def action_quit(self):
        """ Stop the editor """
        self.editor.running = False

    def action_write(self):
        """ Save current status """
        _buffer = self.editor.current_buffer
        if _buffer.file_name == '':
            _buffer.file_name = self.input.prompt_bar('name:')
        _buffer.save_file()
        self.screen.print_bar(_buffer.file_name + ': Saved')

    def action_edit(self):
        """ Open new file to for edit """
        _buffer = self.editor.current_buffer
        filename = self.input.prompt_bar('Open file:')
        _buffer.open_file(filename)
        # reset the command stacks, when starting with fresh new file
        self.editor.command_stack = []
        self.editor.undo_stack = []

    #def action_print_debug(self):
        #if s.startswith('p'): # undocumented feature used for debugging
            #cmd, arg = s.split()
            #arg = int(arg)
            #self.screen.stdscr.addstr(self.screen.MAX_Y-20,10, self.current_buffer[arg])
