#!/usr/bin/env python
# coding=utf8
# 
# Copyright (c) Jakub Olczyk 
# Published under GNU General Public License version 2 or above
# For full text of the license visit www.gnu.org/licenses/gpl.html

from utils import Singleton
from screen import Screen

@Singleton
class Input(object):
    ''' Most do komunikacji z częścią `curses' odpowiedzialną za komunikację z 
        użytkownikiem '''

    def __init__(self):
        self.screen = Screen() # łatwiejsze dobranie się do istniejącego już Singletona

    def getkey(self):
        return self.screen.stdscr.getkey()

    def getch(self):
        return self.screen.stdscr.getch()

    def prompt_bar(self, message):
        self.screen.print_bar(message)
        user_input = self.screen.stdscr.getstr(self.screen.MAX_Y-1, len(message), 1024)
        self.screen.normal_mode()
        return user_input

    def get(self, y, x):
        ''' Main functionality of Input class '''
        import curses.ascii
        esc_pressed = False
        input_str = ""
        key = None
        curr_y = y
        curr_x = x
        self.screen.stdscr.move(curr_y, curr_x)
        my,mx = self.screen.getmaxyx()
        while not esc_pressed:
            key = self.getch()
            if key == curses.ascii.ESC:
                esc_pressed = True
            elif key == curses.ascii.NL:
                curr_y += 1
                self.screen.stdscr.move(curr_y, curr_x)
                input_str += '\n'
                self.screen.refresh()
            elif key == curses.ascii.BS:
                input_str = input_str[:-1]
                self.screen.refresh()
            else:
                try:
                    input_str += chr(key)
                except:
                    pass
        return input_str

def input_sanitizer(text):
    """
    text: string, the user input that needs to be inserted to doc_buffer
    doc_buffer: list
    start_line: int, the line where we need to put the new lines
    """
    sanitazed = []
    if text.count('\n') >= 1:
        sanitazed = str(text).split('\n')
        sanitazed = [line+'\n' for line in sanitazed]
    else: # when we put new string inside one
        sanitazed = [str(text)]
    return sanitazed

def line_sanitizer(iterable):
    to_add = [(0,[])]
    for num, line in enumerate(iterable):
        if line.count('\n') > 1:
            more_lines = (num, input_sanitizer(line))
            to_add.append(more_lines)
    return to_add
