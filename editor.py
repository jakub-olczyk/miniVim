#!/usr/bin/env python
# coding=utf8
# 
# Copyright (c) Jakub Olczyk 
# Published under GNU General Public License version 2 or above
# For full text of the license visit www.gnu.org/licenses/gpl.html

"""
Mega uproszczony Vim stworzony w jakieś 3-4h
"""

def excepted(func):
    """ To jest dekorator do łapania wszelkich niepotrzebnych wyjatkow """
    def func_wrap(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except:
            pass
    return func_wrap 


class iCommand(object): # pseudo-interface in Python
    def __init__(self, document, text, line, start, end):
        pass
    def execute(self):
        pass
    def undo(self):
        pass

class Insert(iCommand):
    """
    Acts similarly to Vi instert mode, but not quite :)
    """
    def __init__(self, document, text, line, start, end):
        """
        document: handle for the buffer
        text: actual change text
        line: the line where insert was done 
        start: the starting position of change
        end: the ending position of change
        """
        self.text = text
        self.changed = ""
        self.document = document
        self.line = line
        self.start = start 
        self.end = end
    
    def execute(self):
        def inserter(src, trgt, start):
            """
            src   : string
            trgt  : string
            start : number
            return: new string based on src with trgt string in between the point start
            """
            result = ""
            result += src[:start]
            result += trgt
            result += src[start:]
            return result
        try:
            self.changed = str(self.document[self.line]) 
        except:
            self.document.append("")
            self.changed = self.document[self.line]

        new_line = self.changed
        new_line = inserter(new_line, self.text, self.start) # FIXME
        self.document[self.line] = new_line

    def undo(self):
        self.document[self.line] = self.changed
        if self.changed == "":
            self.document.pop()

class Delete(iCommand):
    """
    Delete from cursor to end of line.
    """
    def __init__(self, document, line, start, text=None, end=None):
        self.document = document
        self.text = text #deleted text
        self.line = line
        self.start = start
        self.end = end

    def execute(self):
        try:
            self.text = self.document[self.line][self.start:]
            new_line = self.document[self.line][:self.start]
            self.document[self.line] = new_line
        except:
            self.text = ""

    def undo(self):
        self.document[self.line] += self.text

class Editor(object):
    def __init__(self):
        self.file_name = ""
        self.main_buffer = [] # each string in this list is line of text
        self.command_stack = [] # stack of commands executed 
        self.undo_stack = [] # stack of undone commands for redo(?)

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

    def print_buffer(self, scr):
        for i,line in enumerate(self.main_buffer):
            scr.addstr(i,0,line)
        if (len(self.main_buffer) - (MAX_Y-1)) < 0:
            for i in xrange((MAX_Y-1) - len(self.main_buffer)):
                scr.addstr(len(self.main_buffer)+i,0,"~")

    @excepted
    def save_file(self, scr):
        if self.file_name == "":
            scr.addstr(MAX_Y-1,10,"name:")
            self.file_name = str(scr.getstr(MAX_Y-1,15,1024))

        with open("./"+self.file_name,'w+') as f:
            for line in self.main_buffer:
                line = str(line).strip()
                f.write(line+"\n")

    @excepted
    def open_file(self, filename):
        self.file_name = filename
        with open(filename, 'r') as f:
            self.main_buffer = f.readlines()
        
             
if __name__ == "__main__":
    import os, curses
    from curses.textpad import Textbox, rectangle

    ed = Editor()
    current_line = 0
    current_letter = 0

    stdscr = curses.initscr()

    curses.noecho()
    stdscr.keypad(True)
    curses.cbreak()
    curses.curs_set(2)

    MAX_Y, MAX_X = stdscr.getmaxyx()

    stdscr.refresh()

    stdscr.clear()
    stdscr.addstr(MAX_Y-1, MAX_X-5, "{},{}".format(current_line,current_letter), curses.A_REVERSE)
    ed.print_buffer(stdscr)

    while True:
        
        read = stdscr.getkey()

        #stdscr.addstr(MAX_Y-1, 1, str(read))
        stdscr.refresh()

        if read == 'h':
            if current_letter > 0:
                current_letter -= 1

        if read == 'l':
            try:
                if current_letter < len(ed.main_buffer[current_line]):
                    current_letter += 1
            except:
                pass

        if read == 'j':
            try:
                if current_line < len(ed.main_buffer) - 1 :
                    current_line += 1
            except:
                pass
            try:
                if current_letter > len(ed.main_buffer[current_line]):
                    current_letter = len(ed.main_buffer[current_line])
            except:
                pass

        if read == 'k':
            if current_line > 0:
                current_line -= 1
            try:
                if current_letter > len(ed.main_buffer[current_line]):
                    current_letter = len(ed.main_buffer[current_line])
            except:
                pass

        if read == 'i':
            curses.echo()
            #stdscr.standout()
            s = stdscr.getstr(current_line,current_letter,1024)
            ed.execute(Insert(ed.main_buffer, s, current_line, current_letter, current_letter + len(s)))
            current_letter += len(s)
            curses.noecho()
            #stdscr.standend()

        if read == 'd':
            cmd = Delete(ed.main_buffer,current_line,current_letter)
            ed.execute(cmd)

        if read == 'u':
            ed.undo_last()

        if read == 'r':
            ed.redo_last()

        if read == ':':
            curses.curs_set(2)
            stdscr.addstr(MAX_Y-1, 2, ":")
            stdscr.refresh()
            curses.echo()
            s = str(stdscr.getstr(MAX_Y-1, 3, 20))

            if s.startswith('q'): #exit and discard
                break

            if s.startswith('w'): #saving command
                ed.save_file(stdscr)
                stdscr.addstr(MAX_Y-1,0,str(ed.file_name) + "Saved")
                stdscr.refresh()

            if s.startswith('x'): #save and exit
                stdscr.addstr(MAX_Y-1,0,"Saving...")
                ed.save_file(stdscr)
                stdscr.refresh()
                break

            if s.startswith('e'): #edit file
                filename = s.split(' ')[1] 
                ed.open_file(filename)

        # Main drawing 
        stdscr.clear()
        # draw the line and letter number
        stdscr.addstr(MAX_Y-1, MAX_X-5, "{},{}".format(current_line,current_letter), curses.A_REVERSE)
        # display last character pressed'
        if read != '\n':
            stdscr.addstr(MAX_Y-1, MAX_X-20, str(read))
        # display the contents of buffer
        ed.print_buffer(stdscr)

        #DEBUG: print the command_stack
        if read == 'KEY_F(2)':
            stdscr.addstr(MAX_Y-1, 0, "cmd_stack: "+str(len(ed.command_stack))) 
        if read == 'KEY_F(3)':
            stdscr.addstr(MAX_Y-1, 0, "undo_stack: " +str(len(ed.undo_stack))) 

        #show cursor on the screen 
        curses.curs_set(2)
        stdscr.refresh()
        curses.setsyx(current_line,current_letter)
        curses.doupdate()
            
    curses.nocbreak()
    stdscr.keypad(False)
    curses.echo()
    curses.endwin()
