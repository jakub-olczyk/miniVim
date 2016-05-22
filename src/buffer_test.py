#!/usr/bin/env python

""" A program to test the new get implementation """
import curses
stdscr = curses.initscr()

def get(buff, y, x):
    ''' Main functionality of Input class '''
    import curses.ascii
    tmp_buff = buff[:] # shallow copy of the buffer
    if y == 0: # add first line if needed
        tmp_buff.append('')
    esc_pressed = False
    key = None
    curr_y = y
    curr_x = x
    stdscr.move(curr_y, curr_x)
    my, mx = stdscr.getmaxyx()
    input_str = ''
    while not esc_pressed:
        key = stdscr.getch()
        if key == curses.ascii.ESC:
            esc_pressed = True

        elif key == curses.ascii.NL: # newline
            # Add line to tmp_buff
            len_line = len(tmp_buff[curr_y])

            if len_line == curr_x:
                #tmp_buff[curr_y] += '\n'
                tmp_buff.insert(curr_y, '')

            else:
                line_to_split = tmp_buff[curr_y][:]
                stays = line_to_split[curr_x:] #+ '\n'
                new = line_to_split[:curr_x] #+ '\n'
                tmp_buff[curr_y] = stays
                tmp_buff.insert(curr_y, new)

            curr_y += 1
            curr_x = 0
            stdscr.move(curr_y, curr_x)
            stdscr.refresh()

        elif key == curses.ascii.BS: # backspace
            input_str = input_str[:-1]
            stdscr.refresh()

        else: 
            try:
                tmp_buff[curr_y] = tmp_buff[curr_y][:curr_x] + chr(key) + tmp_buff[curr_y][curr_x:]
                curr_x += 1
            except:
                pass
    return tmp_buff

def main():
    BUFFER = ['To jest pierwsza linijka', 'to jest druga']
    stdscr.clear()
    curses.cbreak()
    stdscr.keypad(True)
    for i, line in enumerate(BUFFER):
        stdscr.addstr(i, 0, line)
    stdscr.refresh()
    BUFFER = get(BUFFER, 0, 0)
    stdscr.keypad(False)
    curses.nocbreak()
    curses.echo()
    curses.endwin()
    print BUFFER


if __name__ == "__main__":
    main()
