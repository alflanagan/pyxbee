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


class MyFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.SetTitle("ShowArgs")
        self.panel_1 = wx.Panel(self, wx.ID_ANY)

        self.txtOut = wx.TextCtrl(self.panel_1, wx.ID_ANY, "",
                                  style=wx.TE_MULTILINE | wx.TE_READONLY)
        self.txtOut.SetMinSize((600, 300))
        self.txtOut.SetBackgroundColour(wx.Colour(216, 216, 191))

        self.btnClose = wx.Button(self.panel_1, wx.ID_ANY, "Close")
        self.btnClose.SetMinSize((90, 30))
        self.btnClose.SetBackgroundColour(wx.Colour(154, 255, 194))

        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_2 = wx.FlexGridSizer(2, 1, 10, 0)
        sizer_2.Add(self.txtOut, 1, wx.ALL | wx.EXPAND, 0)
        sizer_2.Add(self.btnClose, 0,
                    wx.ALIGN_CENTER_HORIZONTAL |
                    wx.ALIGN_CENTER_VERTICAL | wx.FIXED_MINSIZE, 11)
        self.panel_1.SetSizer(sizer_2)
        sizer_2.AddGrowableRow(0)
        sizer_2.AddGrowableCol(0)
        sizer_1.Add(self.panel_1, 1, wx.EXPAND, 0)
        self.SetSizer(sizer_1)
        sizer_1.Fit(self)
        self.Layout()

        self.Bind(wx.EVT_BUTTON, self.OnClose, self.btnClose)

    def OnClose(self, event):
        self.Hide()
        self.Close()

    def SetValueLines(self, strIter):
        newVal = ""
        for x in strIter:
            newVal = "{}\n\n{}".format(newVal, x)
        self.txtOut.SetValue(newVal)


class ShowArgs(wx.App):
    def OnInit(self):
        wx.InitAllImageHandlers()
        frame_1 = MyFrame(None, -1, "")
        self.SetTopWindow(frame_1)
        frame_1.Show()
        return 1

if __name__ == "__main__":
    import sys
    ShowArgs = ShowArgs(0)
    ShowArgs.GetTopWindow().SetValueLines(sys.argv)
    ShowArgs.MainLoop()
