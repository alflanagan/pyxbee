# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals
import wx
from serial.tools import list_ports
from com.alloydflanagan.hardware.xbee.XBee import XBee

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


class MyButton(wx.Button):
    """
    Convenience class to create buttons with a set of common attributes.

    @param addto: keyword argument. If present, button will be added to
    to the sizer
    @type addto: L{wx.Sizer}
    @param bindto: keyword argument. If present, button event will be bound
    to this value.
    @type bindto: Event handler (callable w/one argument)
    """
    def __init__(self, *args, **kwargs):
        addTo = None
        bind_to = None
        try:
            addTo = kwargs['addto']
            del kwargs['addto']
        except KeyError:
            #not a problem
            pass
        try:
            bind_to = kwargs['bind_to']
            del kwargs['bind_to']
        except KeyError:
            pass
        super(MyButton, self).__init__(*args, **kwargs)
        self.SetBackgroundColour(wx.Colour(159, 191, 255))
        self.SetFont(wx.Font(10, wx.MODERN, wx.NORMAL, wx.BOLD,
                                         0, "Sans"))
        if addTo:
            addTo.Add(self, 0,
                    wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.SHAPED, 4)
        if bind_to:
            self.Parent.Bind(wx.EVT_BUTTON, bind_to, self)


class PyxbMainFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        """
        Application window for pyxb UI.

        @param ports: A list of com ports to use. Defaults to all ports
        returned by comports().
        @type ports: Return type of L{serial.tools.list_ports.comports}

        """

        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)

        try:
            self.ports = kwds['ports']
        except KeyError:
            self.ports = list_ports.comports()

        self.frame_1_menubar = wx.MenuBar()
        self.SetMenuBar(self.frame_1_menubar)

        self.frame_1_statusbar = self.CreateStatusBar(1, 0)
        self.frame_1_statusbar.SetStatusWidths([-1])
        frame_1_statusbar_fields = ["frame_1_statusbar"]
        for i in range(len(frame_1_statusbar_fields)):
            self.frame_1_statusbar.SetStatusText(frame_1_statusbar_fields[i],
                                                 i)

        self.SetSize((500, 600))
        self.build_widget_panel()
        self.build_sep_panel()
        self.build_comm_panel()
        self.build_button_panel()
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_1.Add(self.WidgetsPanel, 0, wx.EXPAND, 0)
        sizer_1.Add(self.SepPanel, 0, wx.ALL | wx.EXPAND, 0)
        sizer_1.Add(self.CommPanel, 1, wx.EXPAND, 0)
        sizer_1.Add(self.ButtonsPanel, 0, wx.EXPAND, 0)
        self.SetSizer(sizer_1)
        self.Layout()

        self.xb = XBee('/dev/ttyUSB0', listeners=[self.xbee_listener])
        self.text_ctl.AppendText("XBee unit ID is {:#x}\r".format(
                                                        self.xb.get_ID()))

    def xbee_listener(self, data):
        if data:
            self.text_ctl.AppendText(data)

    def build_comm_panel(self):
        self.CommPanel = wx.Panel(self, -1,
                                  style=wx.SUNKEN_BORDER | wx.TAB_TRAVERSAL)
        self.CommPanel.SetBackgroundColour(wx.Colour(0, 216, 191))
        self.CommPanel.SetForegroundColour(wx.Colour(0, 0, 0))
        self.CommPanel.SetSizeWH(200, 200)
        self.text_ctl = wx.TextCtrl(self.CommPanel,
            wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_RICH |
            wx.TE_DONTWRAP | wx.BORDER_SUNKEN)
        self.comm_szr = wx.BoxSizer(wx.VERTICAL)
        self.comm_szr.Add(self.text_ctl, 1, wx.EXPAND)
        self.CommPanel.SetSizer(self.comm_szr)

    def build_sep_panel(self):
        """
        Separator between top and bottom panels.
        """
        self.SepPanel = wx.Panel(self, -1,
                                 style=wx.RAISED_BORDER | wx.TAB_TRAVERSAL)
        self.SepPanel.SetMinSize((-1, 8))
        self.SepPanel.SetBackgroundColour(wx.Colour(216, 216, 191))

    def build_button_panel(self):
        self.ButtonsPanel = wx.Panel(self, -1,
                                     style=wx.RAISED_BORDER | wx.TAB_TRAVERSAL)
        self.ButtonsPanel.SetBackgroundColour(wx.Colour(216, 216, 191))
        sizer_2 = wx.BoxSizer(wx.HORIZONTAL)

        self.TestButton = MyButton(self.ButtonsPanel, -1, "Test",
                                   addto=sizer_2, bind_to=self.Test)
        self.CloseButton = MyButton(self.ButtonsPanel, -1, "Close",
                                    addto=sizer_2, bind_to=self.CloseApp)
        self.ButtonsPanel.SetSizer(sizer_2)

    def build_widget_panel(self):
        self.WidgetsPanel = wx.Panel(self, -1)
        self.WidgetsPanel.SetBackgroundColour(wx.Colour(216, 216, 191))
        self.list_radio_label = wx.StaticText(self.WidgetsPanel, -1,
                                       "Detected Devices",
                                       style=wx.ALIGN_CENTRE)
        self.list_radio_label.SetBackgroundColour(wx.Colour(216, 216, 191))
        self.list_box_1 = wx.ListBox(self.WidgetsPanel, -1, choices=[],
                                     style=wx.LB_SINGLE | wx.LB_NEEDED_SB)
        self.list_box_1.SetMinSize((145, 166))
        self.list_box_szr = wx.BoxSizer(wx.VERTICAL)
        self.list_box_szr.Add(self.list_radio_label)
        self.list_box_szr.Add(self.list_box_1)
        WidgetsSizer = wx.FlexGridSizer(2, 3, 0, 0)
        WidgetsSizer.Add(self.list_box_szr, 0,
                         wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 4)
        self.WidgetsPanel.SetSizer(WidgetsSizer)

    def CloseApp(self, event):
        self.xb.close()
        self.Close()
        event.Skip()

    def Test(self, event):
        print("testing")
        self.xb.activate_at_mode()
        self.xb.send_line("ATID")
        self.xb.send_line("ATDH")
        self.xb.send_line("ATDL")
        ID = self.xb.get_ID()
        print("Got ID={:#x}".format(ID))
        event.Skip()
