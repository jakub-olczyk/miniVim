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
    def __init__(self, buff, new_buff):
        pass
    def execute(self):
        pass
    def undo(self):
        pass

class Insert(iCommand):
    ''' Acts similarly to Vi instert mode, but not quite :) '''

    def __init__(self, old_buff, new_buff):
        '''
        @old_buff: handle for the buffer
        @new_buff: actual change text
        @changes: list of tuples of (numline, old, new)
                  where numline = the index of line changed
                        old = old content of line
                        new = new content of line
        '''
        self.document = old_buff
        self.new_buff = new_buff
        self.changes = []
    
    def execute(self):
        # make both same size
        longer, shorter = self.document, self.new_buff #references yay!
        if len(self.document) < len(self.new_buff):
            longer, shorter = shorter, longer
        diff = len(longer) - len(shorter)

        for i in xrange(diff):
            shorter.append('')

        # determine the changes
        for n, old in enumerate(self.document):
            if old != self.new_buff[n]: # add only differences
                self.changes.append(tuple([n, old, self.new_buff[n]]))

        # add the changes
        for i, old, new in self.changes:
            self.document[i] = new

    def undo(self):
        # revert the changes
        for n, old, new in self.changes:
            self.document[n] = old

class Delete(iCommand):
    ''' Delete depending on the other operand'''

    def __init__(self, buffer, letter):
        self.buffer = buffer
        self.line = self.buffer.current_line
        self.start = self.buffer.current_letter
        self.text = '' # deleted text
        self.letter = letter # the command used

    def execute(self): #FIXME
        if self.letter in set("hjkldD"):
            if self.letter == 'D':
                try:
                    self.text = self.buffer[self.line][self.start:]
                    new_line = self.buffer[self.line][:self.start]
                    self.buffer[self.line] = new_line
                except:
                    self.text = ''
            else:
                    pass
        else:# not in set(hjkldD)
            pass


    def undo(self):
        self.buffer[self.line] += self.text

class Replace(iCommand):
    ''' Replace first occurance of string with another one in current line'''

    def __init__(self, buff, old_text, new_text, line_num):
        self.buffer = buff # handle for the buffer 
        self.old_text = old_text
        self.new_text = new_text
        self.line_num = line_num
        self.old_line = ''
        self.new_line = ''

    def execute(self):
        self.old_line = self.buffer[self.line_num]
        self.new_line = self.old_line.replace(self.old_text, self.new_text)
        self.buffer[self.line_num] = self.new_line

    def undo(self):
        self.buffer[self.line_num] = self.old_line
