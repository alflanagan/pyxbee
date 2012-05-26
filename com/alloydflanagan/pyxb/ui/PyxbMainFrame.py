# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals
import wx
from serial.tools import list_ports
from xbee import ZigBee
import serial
import sys
import time
import xbee

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

        """

        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)

        try:
            self.ports = kwds['ports']
        except KeyError:
            try:
                self.ports = list_ports.comports()
            except:
                self.ports = None

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
        #TODO: mutex to lock this while it's being filled.
        self.incoming_frame = None

        self.ser = None
        self.xb = None

    def build_comm_panel(self):
        self.CommPanel = wx.Panel(self, -1,
                                  style=wx.SUNKEN_BORDER | wx.TAB_TRAVERSAL)
        self.CommPanel.SetBackgroundColour(wx.Colour(0, 216, 191))
        self.CommPanel.SetForegroundColour(wx.Colour(0, 0, 0))
        self.CommPanel.SetSizeWH(200, 200)
        self.text_ctl = wx.TextCtrl(self.CommPanel, wx.ID_ANY, "",
                                    style=wx.TE_READONLY | wx.TE_MULTILINE)
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
        print("CloseApp")
        if self.xb:
            self.xb.halt()
        self.Close()
        event.Skip()

    def Test(self, event):
        print("Test")
        try:
            self.ser = serial.Serial('/dev/ttyUSB0',
                                bytesize=serial.EIGHTBITS,
                                parity=serial.PARITY_NONE,
                                stopbits=serial.STOPBITS_ONE,
                                #timeout=3,
                                xonxoff=False,
                                rtscts=False,
                                baudrate=9600)
            self.xb = ZigBee(self.ser, callback=self.get_frame, escaped=True)
            self.xb.at(command="ID")
            self.xb.at(command="MY")
            self.xb.at(command="%V")
        except Exception, e:
            self.show_exception(e)
            raise
        event.Skip()

    def read_frame(self):
        """
        Parse the most recent incoming frame's data into a hex string.
        """
        result = ''
        if self.incoming_frame:
            for bytein in self.incoming_frame['parameter']:
                print('{:02X}'.format(ord(bytein)))
                result += '{:02X}'.format(ord(bytein))
        return result

    def get_frame(self, frame):
        #TODO: lock this to prevent partial data
        self.incoming_frame = frame
        self.text_ctl.AppendText("\n" + self.read_frame())
        assert self.text_ctl.IsMultiLine()
        print("get_frame() got frame")

    def show_exception(self, e):
        self.text_ctl.AppendText("\n" + str(sys.exc_info()[1]))
#        self.xb.activate_at_mode()
#        self.xb.send_line("ATID")
#        self.xb.send_line("ATDH")
#        self.xb.send_line("ATDL")
#        ID = self.xb.get_ID()
#        print("Got ID={:#x}".format(ID))
#        event.Skip()

if __name__ == '__main__':
    import app
    import os
    os.environ['PYUSB_DEBUG_LEVEL'] = 'debug'
    app.doApp()
