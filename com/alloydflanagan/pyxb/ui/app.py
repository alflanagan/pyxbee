#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals

#Copyright 2012 A. Lloyd Flanagan
#This file is part of Pyxb.

#Pyxb is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.

#Pyxb is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.

#You should have received a copy of the GNU General Public License
#along with Pyxb.  If not, see <http://www.gnu.org/licenses/>.

from PyxbMainFrame import PyxbMainFrame
import wx

def doApp():
    app = wx.PySimpleApp(0)
    wx.InitAllImageHandlers()
    frame_1 = PyxbMainFrame(None, -1, "")
    app.SetTopWindow(frame_1)
    frame_1.Show()
    app.MainLoop()

if __name__ == "__main__":
    import os
    os.environ['PYUSB_DEBUG_LEVEL'] = 'debug'
    #xs = XBees()
    doApp()
