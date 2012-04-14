# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals
import wx

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


class PyxbMainFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)

        self.ButtonsPanel = wx.Panel(self, -1, style=wx.RAISED_BORDER | wx.TAB_TRAVERSAL)

        self.WidgetsPanel = wx.Panel(self, -1)
        self.WidgetsPanel.SetBackgroundColour(wx.Colour(216, 216, 191))

        self.frame_1_menubar = wx.MenuBar()
        self.SetMenuBar(self.frame_1_menubar)

        self.frame_1_statusbar = self.CreateStatusBar(1, 0)
        self.frame_1_statusbar.SetStatusWidths([-1])
        frame_1_statusbar_fields = ["frame_1_statusbar"]
        for i in range(len(frame_1_statusbar_fields)):
            self.frame_1_statusbar.SetStatusText(frame_1_statusbar_fields[i], i)

        self.RadioList = wx.StaticText(self.WidgetsPanel, -1, "Detected Devices", style=wx.ALIGN_CENTRE)
        self.RadioList.SetBackgroundColour(wx.Colour(216, 216, 191))
        self.list_box_1 = wx.ListBox(self.WidgetsPanel, -1, choices=[], style=wx.LB_SINGLE | wx.LB_NEEDED_SB)
        self.list_box_1.SetMinSize((45, 66))

        self.SepPanel = wx.Panel(self, -1, style=wx.RAISED_BORDER | wx.TAB_TRAVERSAL)
        self.SepPanel.SetMinSize((-1, 8))
        self.SepPanel.SetBackgroundColour(wx.Colour(216, 216, 191))

        self.CommPanel = wx.Panel(self, -1, style=wx.SUNKEN_BORDER | wx.TAB_TRAVERSAL)
        self.CommPanel.SetBackgroundColour(wx.Colour(216, 216, 191))
        self.CommPanel.SetForegroundColour(wx.Colour(0, 0, 0))

        self.CloseButton = wx.Button(self.ButtonsPanel, -1, "Close")
        self.CloseButton.SetBackgroundColour(wx.Colour(159, 191, 255))
        self.CloseButton.SetFont(wx.Font(10, wx.MODERN, wx.NORMAL, wx.BOLD, 0, "Sans"))
        self.ButtonsPanel.SetBackgroundColour(wx.Colour(216, 216, 191))

        self.SetSize((500, 600))
        self.__do_layout()

        self.Bind(wx.EVT_BUTTON, self.CloseApp, self.CloseButton)

    def build_button_panel(self):
        sizer_2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_2.Add(self.CloseButton, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.SHAPED, 4)
        self.ButtonsPanel.SetSizer(sizer_2)

    def build_widget_panel(self):
        WidgetsSizer = wx.FlexGridSizer(2, 3, 0, 0)
        WidgetsSizer.Add(self.RadioList, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 4)
        WidgetsSizer.Add(self.list_box_1, 1, wx.EXPAND, 0)
        self.WidgetsPanel.SetSizer(WidgetsSizer)

    def __do_layout(self):
        self.build_widget_panel()
        self.build_button_panel()
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_1.Add(self.WidgetsPanel, 0, wx.EXPAND, 0)
        sizer_1.Add(self.SepPanel, 0, wx.ALL | wx.EXPAND, 0)
        sizer_1.Add(self.CommPanel, 1, wx.EXPAND, 0)
        sizer_1.Add(self.ButtonsPanel, 0, wx.EXPAND, 0)
        self.SetSizer(sizer_1)
        #sizer_1.Fit(self)
        self.Layout()

    def CloseApp(self, event):
        self.Close()
        event.Skip()
