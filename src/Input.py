#!/usr/bin/env python
# coding=utf8
#
# Copyright (c) Jakub Olczyk
# Published under GNU General Public License version 2 or above
# For full text of the license visit www.gnu.org/licenses/gpl.html

""" Main module with the abstraction for getting input from user """

from src.Utils import Singleton
from src.Screen import Screen

class Input(object):
    """ This is a bridge to the part of ``curses'' that is used to get user input """

    __metaclass__ = Singleton

    def __init__(self):
        self.screen = Screen() # łatwiejsze dobranie się do istniejącego już Singletona

    def getkey(self):
        """ Get key in letter representation from Curses module """
        return self.screen.stdscr.getkey()

    def getch(self):
        """ Get key as numeric value; might not be in range [0, 255] """
        return self.screen.stdscr.getch()

    def prompt_bar(self, message):
        """ Show prompt and get the user input """
        self.screen.print_bar(message)
        user_input = self.screen.stdscr.getstr(self.screen.MAX_Y-1, len(message), 1024)
        self.screen.normal_mode()
        return user_input

    def get(self, buff, y_pos, x_pos):
        ''' main functionality of input class. This is used in insert mode to get the user input '''
        tmp_buff = buff[:] # we want to work on copy
        import curses.ascii
        if y_pos == 0 and len(tmp_buff) == 0: # add first line if needed
            tmp_buff.append('')
        esc_pressed = False
        key = None
        self.screen.stdscr.move(y_pos, x_pos)
        while not esc_pressed:
            key = self.getch()
            if key == curses.ascii.ESC:
                esc_pressed = True
            elif key == curses.ascii.NL: # newline
                # add line to tmp_buff
                len_line = len(tmp_buff[y_pos])

                if len_line == x_pos:
                    tmp_buff.insert(y_pos+1, '')
                else:
                    line_to_split = tmp_buff[y_pos][:]
                    stays = line_to_split[x_pos:]
                    new = line_to_split[:x_pos]
                    tmp_buff[y_pos] = stays
                    tmp_buff.insert(y_pos, new)
                y_pos += 1
                x_pos = 0
                self.screen.stdscr.move(y_pos, x_pos)
                self.screen.refresh()

            elif key == 263: # backspace : the curses.ascii.bs didn't work :(
                new = tmp_buff[y_pos][:x_pos-1] + tmp_buff[y_pos][x_pos:]
                x_pos -= 1
                tmp_buff[y_pos] = new
                self.screen.refresh()
            elif key in range(0, 255): # add one character, bc ascii
                try:
                    tmp_buff[y_pos] = tmp_buff[y_pos][:x_pos] + chr(key) + tmp_buff[y_pos][x_pos:]
                    x_pos += 1
                except StandardError:
                    pass
            else: # non-ascii characters or special keys
                pass
        return (tmp_buff, y_pos, x_pos)
