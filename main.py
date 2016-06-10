#!/usr/bin/env python
# coding=utf8
# 
# Copyright (c) Jakub Olczyk 
# Published under GNU General Public License version 2 or above
# For full text of the license visit www.gnu.org/licenses/gpl.html

from src.Editor import Editor
import sys

def main(argv):
    file_to_open = ''
    if not (sys.argv[0] == 'minivimtutor' or sys.argv[0] == './minivimtutor'):
        import getopt
        try:
            opts, args = getopt.getopt(sys.argv[1:], 'h')
        except getopt.GetoptError as e:
            print str(e)
            sys.exit(2)
        
        if opts:
            print "miniVim\nusage: [option] [filename]\n\t-h : prints this help"
            sys.exit(0)
        elif args:
            file_to_open=args[0]
    else:
        file_to_open = './doc/demo-edytora'

    ed = Editor(file_to_open)
    ed.start()

if __name__ == "__main__":
    main(sys.argv)
