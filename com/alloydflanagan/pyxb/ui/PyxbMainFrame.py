# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals
import wx
from serial.tools import list_ports
from xbee import ZigBee
import serial
import sys

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


def hex_str(data):
    result = ''
    for bytein in data:
            result += '{:02X}'.format(ord(bytein))
    return result


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


class NotebookPage1Panel(wx.Panel):

    def __init__(self, parent, *args, **kwargs):
        super(NotebookPage1Panel, self).__init__(parent, *args, **kwargs)
        labels = ["PAN ID", "Serial", "Destination", "Address",
                  "Children Avail", "Max Payload",
                  "Encryption?", "Version", ]
        panel_sizer = wx.FlexGridSizer(rows=len(labels), cols=2, vgap=2,
                                       hgap=5)
        panel_sizer.SetFlexibleDirection(wx.HORIZONTAL)
        self.vals = []
        for lbl in labels:
            txt = wx.StaticText(self, label=lbl, style=wx.ALIGN_RIGHT)
            val = wx.TextCtrl(self)
            val.SetMinSize((175, -1))
            self.vals.append(val)
            panel_sizer.Add(txt)
            panel_sizer.Add(val)
        self.SetSizer(panel_sizer)

    @property
    def xbee(self):
        """XBee object which provides data to fill controls."""
        return self.xb

    @xbee.setter
    def set_xbee(self, xbee):
        self.xb = xbee

    def set_value(self, field, value):
        """
        Sets the value of a given field.
        field: integer index to vals array.
        value: value to display.
        """
        self.vals[field].SetValue(str(value))

    def populate(self):
        self.xb.at(command="ID")
        resp = self.xb.wait_read_frame()
        print(hex_str(resp['parameter']))
        self.set_value(0, hex_str(resp['parameter']))
        self.xb.at(command="MY")
        resp = self.xb.wait_read_frame()
        print(hex_str(resp['parameter']))
        self.xb.at(command="%V")
        resp = self.xb.wait_read_frame()
        print(hex_str(resp['parameter']))


class DevWidgetsPanel(wx.Panel):

    def __init__(self, parent, *args, **kwargs):
        super(DevWidgetsPanel, self).__init__(parent, *args, **kwargs)
        self.SetBackgroundColour((216, 216, 191))
        self.list_radio_label = wx.StaticText(self, -1,
                                       "Detected Devices",
                                       style=wx.ALIGN_CENTRE)
        self.list_radio_label.SetBackgroundColour(wx.Colour(216, 216, 191))
        self.list_box_1 = wx.ListBox(self, choices=[],
                                     style=wx.LB_SINGLE | wx.LB_NEEDED_SB)
        self.list_box_1.SetMinSize((145, 166))
        self.list_box_szr = wx.BoxSizer(wx.VERTICAL)
        self.list_box_szr.Add(self.list_radio_label, 0, wx.ALL, border=10)
        self.list_box_szr.Add(self.list_box_1,
                              flag=wx.RIGHT | wx.LEFT | wx.BOTTOM,
                              border=5)
        self.vals = []
        """list of data value display controls"""
        self.build_data_panel()
        self.top_widgets_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.top_widgets_sizer.Add(self.list_box_szr)
        self.top_widgets_sizer.Add(self.DataPanel, wx.EXPAND)
        self.SetSizer(self.top_widgets_sizer)

    def build_data_panel(self):
        #data_panel = Panel {
        #  BoxSizer VERTICAL
        #  StaticText "Device Info"
        #  NoteBook {
        #    page {
        #      NotebookPage1Panel
        #}}}
        self.DataPanel = wx.Panel(self, wx.ID_ANY)
        self.DataPanel.SetMinSize((-1, 250))

        data_panel_sizer = wx.BoxSizer(wx.VERTICAL)
        lbl = wx.StaticText(self.DataPanel, wx.ID_ANY, "Device Info")
        data_panel_sizer.Add(lbl, 0, wx.EXPAND | wx.ALL, border=10)

        self.notebook = wx.Notebook(self.DataPanel)
        self.page1_panel = NotebookPage1Panel(self.notebook)
        self.notebook.AddPage(self.page1_panel, "Basics")
        data_panel_sizer.Add(self.notebook,
                                  flag=wx.EXPAND | wx.ALL, border=5)
        self.DataPanel.SetSizer(data_panel_sizer)

    def on_select_page1(self, event):
        self.page1_panel.populate_from(self.xb)

    def fill_ports(self, port_list):
        for port in port_list:
            self.list_box_1.AppendAndEnsureVisible(port)

    def set_value(self, index, data):

        self.vals[index].SetValue(data)


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

        self.verified_ports = []
        self.check_ports()

        #menu bar
        self.frame_1_menubar = wx.MenuBar()
        self.SetMenuBar(self.frame_1_menubar)

        #status bar
        self.frame_1_statusbar = self.CreateStatusBar(1, 0)
        self.frame_1_statusbar.SetStatusWidths([-1])
        frame_1_statusbar_fields = ["frame_1_statusbar"]
        for i in range(len(frame_1_statusbar_fields)):
            self.frame_1_statusbar.SetStatusText(frame_1_statusbar_fields[i],
                                                 i)

        #main panels
        self.SetSize((500, 600))
        self.widgets_panel = DevWidgetsPanel(self)
        if self.verified_ports:
            self.widgets_panel.fill_ports(self.verified_ports)
        self.build_sep_panel()
        self.build_comm_panel()
        self.build_button_panel()
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_1.Add(self.widgets_panel, 0, wx.EXPAND, 0)
        sizer_1.Add(self.SepPanel, 0, wx.ALL | wx.EXPAND, 0)
        sizer_1.Add(self.CommPanel, 1, wx.EXPAND, 0)
        sizer_1.Add(self.ButtonsPanel, 0, wx.EXPAND, 0)
        self.SetSizer(sizer_1)
        self.Layout()

        #TODO: mutex to lock this while it's being filled.
        self.incoming_frame = None

        self.ser = None
        self.xb = None

    def check_ports(self):
        """
        for each serial port found, ask "are you an xbee". (How do I do that
        safely? Preferably I would want to not send any data to port. Return
        ports for which answer is yes.
        """
        for port in self.ports:
            self.verified_ports.append(port[0])

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
                                    addto=sizer_2, bind_to=self.close_app)
        self.ButtonsPanel.SetSizer(sizer_2)

    def close_app(self, event):
        if self.xb:
            self.xb.halt()
        try:
            self.ser.close()
        except:
            pass
        self.Close()
        print("close_app")
        event.Skip()

    def read_data(self, device):
        try:
            self.ser = serial.Serial(device,
                                     bytesize=serial.EIGHTBITS,
                                     parity=serial.PARITY_NONE,
                                     stopbits=serial.STOPBITS_ONE,
                                     #timeout=3,
                                     xonxoff=False,
                                     rtscts=False,
                                     baudrate=9600)
            self.xb = ZigBee(self.ser, escaped=True)
            self.xb.at(command="ID")
            resp = self.xb.wait_read_frame()
            print(self.hex_str(resp['parameter']))
            self.widgets_panel.set_value(0, self.hex_str(resp['parameter']))
            self.xb.at(command="MY")
            resp = self.xb.wait_read_frame()
            print(self.hex_str(resp['parameter']))
            self.xb.at(command="%V")
            resp = self.xb.wait_read_frame()
            print(self.hex_str(resp['parameter']))
        except Exception, e:
            self.show_exception(e)
            raise

    def Test(self, event):
        self.ser = serial.Serial('/dev/ttyUSB0',
                                 bytesize=serial.EIGHTBITS,
                                 parity=serial.PARITY_NONE,
                                 stopbits=serial.STOPBITS_ONE,
                                 #timeout=3,
                                 xonxoff=False,
                                 rtscts=False,
                                 baudrate=9600)
        self.xb = ZigBee(self.ser, escaped=True)
        self.widgets_panel.page1_panel.xb = self.xb
        self.widgets_panel.page1_panel.populate()

    def read_frame(self):
        """
        Parse the most recent incoming frame's data into a hex string.
        """
        result = ''
        if self.incoming_frame:
            for bytein in self.incoming_frame['parameter']:
                result += '{:02X}'.format(ord(bytein))
        return result

    def get_frame(self, frame):
        #TODO: lock this to prevent partial data
        self.incoming_frame = frame
        self.text_ctl.AppendText("\n" + self.read_frame())
        assert self.text_ctl.IsMultiLine()
        #print("get_frame() got frame")

    def show_exception(self, e):
        self.text_ctl.AppendText("\n" + str(sys.exc_info()[1]))

if __name__ == '__main__':
    import app
    import os
    assert wx.version().startswith('2.9')
    os.environ['PYUSB_DEBUG_LEVEL'] = 'debug'
    app.doApp()
