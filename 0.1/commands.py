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
class iCommand(object): # pseudo-interface in Python
    def __init__(self, document, text, line, start, end):
        pass
    def execute(self):
        pass
    def undo(self):
        pass

class Insert(iCommand):
    ''' Acts similarly to Vi instert mode, but not quite :) '''

    def __init__(self, document, text, line, start, end):
        '''
        @document: handle for the buffer
        @text: actual change text
        @line: the line where insert was done 
        @start: the starting position of change
        @end: the ending position of change
        '''
        self.text = text
        self.changed = ''
        self.document = document
        self.line = line
        self.start = start 
        self.end = end
    
    def execute(self):
        def inserter(src, trgt, start):
            '''
            @src   : string
            @trgt  : string
            @start : number
            @return: new string based on src with trgt string in between the point start
            '''
            result = ''
            result += src[:start]
            result += trgt
            result += src[start:]
            return result
        try:
            self.changed = str(self.document[self.line]) 
        except:
            self.document.append('')
            self.changed = self.document[self.line]

        new_line = self.changed
        new_line = inserter(new_line, self.text, self.start) 
        self.document[self.line] = new_line

    def undo(self):
        self.document[self.line] = self.changed
        if self.changed == '':
            self.document.pop()

class Delete(iCommand):
    ''' Delete from cursor to end of line.  '''

    def __init__(self, buffer, text=None, end=None):
        self.buffer = buffer
        self.text = text #deleted text
        self.line = self.buffer.current_line
        self.start = self.buffer.current_letter
        self.end = end

    def execute(self):
        try:
            self.text = self.document[self.line][self.start:]
            new_line = self.document[self.line][:self.start]
            self.document[self.line] = new_line
        except:
            self.text = ''

    def undo(self):
        self.document[self.line] += self.text
