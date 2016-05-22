#!/usr/bin/env python

import curses
import curses.ascii

stdscr = curses.initscr()
esc_pressed = False
stdscr.clear()
curses.cbreak()
curses.noecho()
stdscr.keypad(True)
curses.curs_set(0)

while not esc_pressed:
    key = stdscr.getch()
    if key == curses.ascii.ESC:
        esc_pressed = True
    key = str(int(key))
    stdscr.addstr(0,0, "Klawisz: ")
    stdscr.addstr(1, 0, key)

stdscr.keypad(False)
curses.nocbreak()
curses.echo()
curses.endwin()
