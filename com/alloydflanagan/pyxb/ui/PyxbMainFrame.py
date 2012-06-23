# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals
import wx
from serial.tools import list_ports
from xbee import ZigBee
import serial
import sys
from SettingsNotebook import SettingsNotebook

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

    @param parent: The parent window.
    @type parent: L{wx.Window}
    @param id: An identifier for the panel. wxID_ANY is taken to mean a default
    @type id: int
    @param pos: The panel position. The value wxDefaultPosition indicates a
                default position, chosen by either the windowing system or
                wxWidgets, depending on platform.
    @type pos: wx.Position, or a two-tuple.
    @param size: The panel size. The value wxDefaultSize indicates a default
                 size, chosen by either the windowing system or wxWidgets,
                 depending on platform.
    @type size: wx.Size, or a two-tuple.
    @param style: The window style. See wxPanel.
    @type style: wx.Style, or int
    @param name: Window name.
    @type name: string
    @keyword addto: If present, button will be added to the sizer
    @type addto: L{wx.Sizer}
    @keyword bindto: If present, button event will be bound to this value.
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


class DataPanel(wx.Panel):
    def __init__(self, *args, **kwargs):
        super(DataPanel, self).__init__(*args, **kwargs)
        #self.SetMinSize((-1, 250))

        sizer = wx.BoxSizer(wx.VERTICAL)
        lbl = wx.StaticText(self, wx.ID_ANY, "Device Info")
        sizer.Add(lbl, 0, wx.EXPAND | wx.ALL, border=10)

        self.notebook = SettingsNotebook(self)
        sizer.Add(self.notebook, 1)
        self.SetSizer(sizer)


class ListBoxPanel(wx.Panel):
    def __init__(self, *args, **kwargs):
        super(ListBoxPanel, self).__init__(*args, **kwargs)
        self.list_radio_label = wx.StaticText(self, -1,
                                       "Detected Devices",
                                       style=wx.ALIGN_CENTRE)
        self.list_radio_label.SetBackgroundColour(wx.Colour(216, 216, 191))
        self.list_box_1 = wx.ListBox(self, choices=[],
                                     style=wx.LB_SINGLE | wx.LB_NEEDED_SB)
        self.list_box_szr = wx.BoxSizer(wx.VERTICAL)
        self.list_box_szr.Add(self.list_radio_label, 0, wx.ALL, border=10)
        self.list_box_szr.Add(self.list_box_1, 1,
                              flag=wx.EXPAND,
                              border=5)
        self.SetSizer(self.list_box_szr)


class DevWidgetsPanel(wx.Panel):

    def __init__(self, parent, *args, **kwargs):
        super(DevWidgetsPanel, self).__init__(parent, *args, **kwargs)
        self.SetBackgroundColour((216, 216, 191))
        self.list_panel = ListBoxPanel(self, wx.ID_ANY)
        self.data_panel = DataPanel(self, wx.ID_ANY)
        #self.data_panel.SetMinSize((self.HEIGHT * 0.7, self.WIDTH))
        self.top_widgets_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.top_widgets_sizer.Add(self.list_panel)
        self.top_widgets_sizer.Add(self.data_panel, 1)
        self.SetSizer(self.top_widgets_sizer)
        self.top_widgets_sizer.Fit(self)

    def on_select_page1(self, event):
        #self.page1_panel.populate_from(self.xb)
        pass

    def fill_ports(self, port_list):
        pass
        #for port in port_list:
        #    self.list_box_1.AppendAndEnsureVisible(port)

    def populate(self, xbee_dev=None):
        if xbee_dev:
            self.xb = xbee_dev
        self.data_panel.notebook.page1.xbee = self.xb
        self.data_panel.notebook.page1.populate()


class CommPanel(wx.Panel):
    def __init__(self, *args, **kwargs):
        """
        Window parent
        int id=-1
        Point pos=DefaultPosition
        Size size=DefaultSize
        long style=wxTAB_TRAVERSAL|wxNO_BORDER
        String name=PanelNameStr
        """
        try:
            kwargs["style"] |= wx.SUNKEN_BORDER | wx.TAB_TRAVERSAL
        except KeyError:
            kwargs["style"] = wx.SUNKEN_BORDER | wx.TAB_TRAVERSAL
        super(CommPanel, self).__init__(*args, **kwargs)

        self.SetBackgroundColour(wx.Colour(0, 216, 191))
        self.SetForegroundColour(wx.Colour(0, 0, 0))
        self.SetSize((200, 200))
        self.text_ctl = wx.TextCtrl(self, wx.ID_ANY, "",
                                    style=wx.TE_READONLY | wx.TE_MULTILINE)
        self.szr = wx.BoxSizer(wx.VERTICAL)
        self.szr.Add(self.text_ctl, 1, wx.EXPAND)
        self.SetSizer(self.szr)


class PyxbMainFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        """
        Application window for pyxb UI.

        Parameters can be supplied positionally or as keywords
        @param parent: The window parent. This may be NULL. If it is non-NULL,
            the frame will always be displayed on top of the parent window on
            Windows.
        @type parent: window
        @param id: The window identifier. It may take a value of -1 to indicate
            a default value.
        @type id: int
        @param title: The caption to be displayed on the frame's title bar.
        @type title: string
        @param pos: The window position. The value wxDefaultPosition indicates
            a default position, chosen by either the windowing system or
            wxWidgets, depending on platform.
        @type pos: wx.Point, or tuple of two ints
        @param size: The window size. The value wxDefaultSize indicates a
            default size, chosen by either the windowing system or wxWidgets,
            depending on platform.
        @type size: wx.Size, or tuple of two ints
        @param style: The window style. See wxFrame class description.
        @type style: int
        @param name: The name of the window. This parameter is used to
            associate a name with the item, allowing the application
            user to set Motif resource values for individual windows.
        @type name: string

        """

        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        super(PyxbMainFrame, self).__init__(*args, **kwds)

        self.HEIGHT = 500
        self.WIDTH = 600
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
        self.SetMinSize((self.WIDTH, self.HEIGHT))
        self.widgets_panel = DevWidgetsPanel(self)
        if self.verified_ports:
            self.widgets_panel.fill_ports(self.verified_ports)
        self.widgets_panel.SetMinSize((self.WIDTH, self.HEIGHT * 0.6))
        self.build_sep_panel()
        self.comm_panel = CommPanel(self, wx.ID_ANY)
        self.build_button_panel()

        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_1.Add(self.widgets_panel, 1, wx.EXPAND)
        sizer_1.Add(self.SepPanel, 0)
        sizer_1.Add(self.comm_panel, 1, wx.EXPAND)
        sizer_1.Add(self.ButtonsPanel, 0, wx.EXPAND)
        self.SetSizer(sizer_1)
        sizer_1.Fit(self)
        self.Layout()

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
        self.widgets_panel.populate(self.xb)

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
