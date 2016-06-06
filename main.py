#!/usr/bin/env python
# coding=utf8
# 
# Copyright (c) Jakub Olczyk 
# Published under GNU General Public License version 2 or above
# For full text of the license visit www.gnu.org/licenses/gpl.html

from src.Editor import Editor

if __name__ == "__main__":
    import sys
    file_to_open = ''

    if sys.argv[0] == 'minivimtutor' or sys.argv[0] == './minivimtutor':
        file_to_open = '/home/jakub/workbench/minivi/doc/demo-edytora'

    ed = Editor(file_to_open)
    ed.start()
