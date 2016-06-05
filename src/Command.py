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

""" Commands that modify the contents of buffer """

class Command(object): # pseudo-interface in Python
    """ A class to simulate an interface """

    def __init__(self):
        pass

    def execute(self):
        """ This is a method that is used to run the command """
        raise NotImplementedError("This is from interface!")

    def undo(self):
        """ This is a method to revert the commands wrongdoings :) """
        raise NotImplementedError("This is from interface!")

class Insert(Command):
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
        Command.__init__(self)
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
        for i, old in enumerate(self.document):
            if old != self.new_buff[i]: # add only differences
                self.changes.append(tuple([i, old, self.new_buff[i]]))

        # add the changes
        for i, old, new in self.changes:
            self.document[i] = new

    def undo(self):
        # revert the changes
        for i, old, new in self.changes:
            self.document[i] = old

class Delete(Command):
    ''' Delete depending on the other operand'''

    def __init__(self, buff, letter):
        Command.__init__(self)
        self.buffer = buff
        self.line = self.buffer.current_line
        self.start = self.buffer.current_letter
        self.text = (None, None) # (x,deleted text)
        self.letter = letter # the command used

    def execute(self):
        line = self.buffer[self.line] # alias to current line
        if self.letter in set("hldD"):
            if self.letter == 'D': # delete to the end of line
                try:
                    self.text = line[self.start:]
                    new_line = line[:self.start]
                    line = new_line
                except StandardError:
                    self.text = (None, None)
            elif self.letter == 'd': # delete current line
                self.text = line[:]
                self.buffer[self.line] = None
                self.buffer.remove(None)
            elif self.letter == 'l': #delete current letter
                x_pos = self.buffer.current_letter
                self.text = (x_pos, line[x_pos]) # we need to get the position in line
                line = line[:x_pos] + line[x_pos+1:]
            elif self.letter == 'h': #delete one before current letter
                x_pos = self.buffer.current_letter-1
                self.text = (x_pos, line[x_pos]) # we need to get the position in line
                line = line[:x_pos] + line[x_pos+1:]
            else:
                pass
        else:# not in set(hjkldD)
            pass


    def undo(self):
        line = self.buffer[self.line] # alias to current line
        if self.letter == 'D':
            line += self.text
        elif self.letter == 'd':
            line.insert(self.line, self.text)
        elif self.letter == 'l' or self.letter == 'h':
            x_pos, letter = self.text
            line = line[:x_pos] + letter + line[x_pos:]
        else:
            pass

class Replace(Command):
    ''' Replace first occurance of string with another one in current line'''

    def __init__(self, buff, old_text, new_text, line_num):
        Command.__init__(self)
        self.buffer = buff # handle for the buffer
        self.old_text = old_text
        self.new_text = new_text
        self.line_num = line_num
        self.old_line = ''
        self.new_line = ''

    def execute(self):
        self.old_line = self.buffer[self.line_num]
        self.new_line = self.old_line.replace(self.old_text, self.new_text, 1)
        self.buffer[self.line_num] = self.new_line

    def undo(self):
        self.buffer[self.line_num] = self.old_line
