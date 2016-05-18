#coding=utf8
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

from utils import excepted

class Dispatcher(object):
    '''
    Analizer for keys pressed that is aware of the mode of operation and acts 
    accordingly.
    '''
    def __init__(self, editor):
        self.editor = editor
        self.mode = self.editor.mode
        self.commands = {
                'h': self.editor.current_buffer.cursor_left,
                'l': self.editor.current_buffer.cursor_right,
                'j': self.editor.current_buffer.cursor_down,
                'k': self.editor.current_buffer.cursor_up,
                'i': self.editor.enter_insert,
                'd': self.editor.enter_delete,
                'u': self.editor.undo_last,
                'r': self.editor.redo_last,
                ':': self.editor.settings
            }

    @excepted
    def execute(self, cmd_letter):
        cmd = self.commands[cmd_letter]
        return cmd()

