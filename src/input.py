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

    def get(self, buff, y, x):
        ''' Main functionality of Input class '''
        tmp_buff = buff[:]
        import curses.ascii
        if y == 0 and len(tmp_buff) == 0: # add first line if needed
            tmp_buff.append('')
        esc_pressed = False
        key = None
        curr_y = y
        curr_x = x
        self.screen.stdscr.move(curr_y, curr_x)
        my, mx = self.screen.getmaxyx()
        while not esc_pressed:
            key = self.getch()
            if key == curses.ascii.ESC:
                esc_pressed = True

            elif key == curses.ascii.NL: # newline
                # Add line to tmp_buff
                len_line = len(tmp_buff[curr_y])

                if len_line == curr_x:
                    tmp_buff.insert(curr_y+1, '')
                else:
                    line_to_split = tmp_buff[curr_y][:]
                    stays = line_to_split[curr_x:]
                    new = line_to_split[:curr_x]
                    tmp_buff[curr_y] = stays
                    tmp_buff.insert(curr_y, new)

                curr_y += 1
                curr_x = 0
                self.screen.stdscr.move(curr_y, curr_x)
                self.screen.refresh()

            elif key == 263: # backspace : the curses.ascii.bs didn't work :(
                new = tmp_buff[curr_y][:curr_x-1] + tmp_buff[curr_y][curr_x:]
                curr_x -= 1
                tmp_buff[curr_y] = new
                self.screen.refresh()
            elif key in range(0,255): #add one character
                try:
                    tmp_buff[curr_y] = tmp_buff[curr_y][:curr_x] + chr(key) + tmp_buff[curr_y][curr_x:]
                    curr_x += 1
                except:
                    pass
            else: # non-ascii characters or special keys
                pass
        return (tmp_buff, curr_y, curr_x)

def input_sanitizer(text):
    sanitazed = []
    if text.count('\n') >= 1:
        sanitazed = str(text).split('\n')
        sanitazed = [line+'\n' for line in sanitazed]
    else: # when we put new string inside one
        sanitazed = [str(text)]
    return sanitazed
