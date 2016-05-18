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

def excepted(func):
    ''' To jest dekorator do łapania wszelkich niepotrzebnych wyjatkow 
        dodatkowo ma za zadanie logować wszelkie wyjątki do pliku
    '''
    import sys
    def func_wrap(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except:
            e = sys.exc_info()
            msg = str(e) + str(e[2])
            with open('vi.log','w+') as log:
                log.write(msg)
            # pass # Here should be some sort of logging given the amount of
                 # functions that uses this decorator
    return func_wrap 

def get_input(scr, y, x):
    import curses.ascii
    esc_pressed = False
    input_str = ""
    key = None
    scr.move(y,x)
    while not esc_pressed:
        my,mx = scr.getmaxyx()
        scr.addstr(my-20, mx-40, input_str)
        scr.move(y,x+len(input_str))
        key = scr.getch()
        if key == curses.ascii.ESC:
            esc_pressed = True
        elif key == curses.ascii.NL:
            scr.move(y+1,x)
            input_str += '\n'
        elif key == curses.ascii.BS:
            input_str = input_str[:-1]
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
