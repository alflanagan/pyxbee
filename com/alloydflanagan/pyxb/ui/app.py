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
import wx
from PyxbMainFrame import PyxbMainFrame


class PyxbApp(wx.App):

    def checkWxVersion(self):
        ver = wx.version()
        major = int(ver[0], 10)
        assert major >= 2
        firstper = ver.find('.')
        if firstper > -1:
            minor = int(ver[firstper + 1], 10)
            assert minor >= 3

    def OnInit(self):
        self.checkWxVersion()
        self.top_frame = PyxbMainFrame(None, -1, "")
        #TODO: catch exception,log, return False
        self.SetTopWindow(self.top_frame)
        return True

    def Show(self):
        self.top_frame.Show()


def doApp():
    app = PyxbApp(0)
    app.Show()
    app.MainLoop()

if __name__ == "__main__":
    import os
    os.environ['PYUSB_DEBUG_LEVEL'] = 'debug'
    doApp()
