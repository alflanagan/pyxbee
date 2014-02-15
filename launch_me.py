#!/usr/bin/env python3
import os
import sys

#we use fakegir to generate package info for editor autocomplete. If it's present in PATH, remove it
fakegir_path = os.path.join(os.path.expanduser('~'), '.cache', 'fakegir')
if fakegir_path in sys.path:
    #print("fakegir found; ignoring it")
    sys.path.remove(fakegir_path)

from gi.repository import Gtk
from view.gtk3.main_win import PyxbMainWin


if __name__ == '__main__':
    win = PyxbMainWin(38400)
    Gtk.main()
