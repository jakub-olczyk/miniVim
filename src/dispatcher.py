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
    A substitute to tree of `if elif else`, with logging capabilities due to
    exepted decorator.
    '''
    def __init__(self, editor):
        self.editor = editor
        self.commands = {
                'h': self.editor.current_buffer.cursor_left,
                'l': self.editor.current_buffer.cursor_right,
                'j': self.editor.current_buffer.cursor_down,
                'k': self.editor.current_buffer.cursor_up,
                'i': self.editor.insert,
                'I': self.editor.insert_start,
                'A': self.editor.insert_end,
                'o': self.editor.insert_below,
                'd': self.editor.delete_move,
                'D': self.editor.delete_to_end,
                's': self.editor.replace,
                'u': self.editor.undo_last,
                'r': self.editor.redo_last,
                ':': self.editor.settings,
                'p': self.editor.debug_buffer
            }

    @excepted
    def execute(self, cmd_letter):
        cmd = self.commands[cmd_letter]
        return cmd()

