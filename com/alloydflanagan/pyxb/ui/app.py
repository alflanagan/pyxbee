#!/usr/bin/env python
# -*- coding: utf-8 -*-
# generated by wxGlade 0.6.3 on Sun Mar  4 12:32:40 2012
from __future__ import division, print_function

import wx
from PyxbMainFrame import PyxbMainFrame
from com.alloydflanagan.hardware.xbee.XBees import XBees

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
    xs = XBees()
    #doApp()