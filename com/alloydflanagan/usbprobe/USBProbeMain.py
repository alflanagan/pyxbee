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
from wx._core import Size
from com.alloydflanagan.hardware.usb.Devices import USBDevices
from wx import html


class USBTopFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.top_panel = wx.Panel(self, -1)
        self.top_frame_statusbar = self.CreateStatusBar(1, wx.ST_SIZEGRIP)

        #child windows
        self.build_selection_panel()
        self.build_display_panel()

        self.__set_properties()
        self.__do_layout()

        self.initial_size = Size(440, 600)
        self.SetSize(self.initial_size)

        self.bind_controls()

        #set up initial data items
        self.populate_usb_list()
        self.selected_dev = None
        '''currently selected device entry, if any'''

    def bind_controls(self):
        self.Bind(wx.EVT_LISTBOX, self.OnClick, self.device_list_box)
        self.Bind(wx.EVT_BUTTON, self.closeOnClick, self.button_close)
        self.Bind(wx.EVT_TREE_SEL_CHANGED, self.onTreeSelectChange,
                  self.tree_usb_probe)

    def build_display_panel(self):
        """
        Sets up UI elements for bottom half of UI, which displays various
        attributes of the selected item.

        """
        self.display_panel = wx.Panel(self.top_panel, -1)
        self.display_html = html.HtmlWindow(self.display_panel, -1)
        self.show_display_html('''<h2>Display Window</h2>
        <p>Hello, world</p>''')
        self.button_close = wx.Button(self.display_panel, -1, "Close")

    def show_display_html(self, html_text):
        """
        Display html_text in the lower half of the frame.

        """
        self.display_html.SetPage(html_text)
        #must reset background color after each SetPage()
        #if you set background to wx.NullColor, previous HTML text shows
        #up underneath new. This must be a bug.
        self.display_html.SetBackgroundColour(self.GetBackgroundColour())

    def show_device_info(self, dev):
        """
        Builds display of info about USB device in bottom panel. Called
        whenever a device entry is selected by user.

        """
        attrs = dev.get_non_methods()

        html_text = '<h3>USB Device (v. {})</h3><ul>'.format(
                                            dev.version_string)
        for attr in attrs:
            html_text = '{}<li>{}: {}</li>'.format(
                        html_text, attr, str(eval('dev.device.' + attr)))
        html_text += '</ul>'
        self.show_display_html(html_text)

    def show_interface_info(self, intfc):
        """
        Builds display of info about USB interface in bottom panel. Called
        whenever an interface entry is selected by user.

        """
        attrs = USBTopFrame.get_non_methods(intfc)
        html_text = '<h3>USB Interface</h3><ul>'
        for attr in attrs:
            html_text = '{}<li>{}: {}</li>'.format(html_text, attr,
                                                   str(eval('intfc.' + attr)))
        html_text += '</ul>'
        self.show_display_html(html_text)

    def show_endpoint_info(self):
        """
        Builds display of info about USB endpoint in bottom panel. Called
        whenever an endpoint entry is selected by user.

        """
        pass

    def build_selection_panel(self):
        """
        Sets up UI elements for top half of UI, where the user selects an item
        in the USB heirarchy.

        selection_panel
          selection_splitter
            selection_panel_pane_L
              device_lbl
              device_list_box
            selection_panel_pane_R
              interfaces_lbl
              tree_usb_probe

        """
        self.selection_panel = wx.Panel(self.top_panel, -1)
        self.selection_splitter = wx.SplitterWindow(self.selection_panel, -1,
                                            style=wx.SP_3D | wx.SP_BORDER)
        self.selection_panel_pane_R = wx.Panel(self.selection_splitter, -1)
        self.selection_panel_pane_L = wx.Panel(self.selection_splitter, -1)
        self.device_lbl = wx.StaticText(self.selection_panel_pane_L,
                                        - 1, "Devices")
        self.interfaces_lbl = wx.StaticText(self.selection_panel_pane_R,
                                            - 1, "Interfaces")
        self.device_list_box = wx.ListBox(self.selection_panel_pane_L, -1,
                            choices=[], style=wx.LB_SINGLE | wx.LB_NEEDED_SB)
        self.tree_usb_probe = wx.TreeCtrl(self.selection_panel_pane_R, -1,
                    style=wx.TR_HAS_BUTTONS | wx.TR_NO_LINES |
                            wx.TR_DEFAULT_STYLE | wx.SUNKEN_BORDER)

    def populate_usb_list(self):
        """
        Probes USB devices and adds an entry to list box for each device.
        """
        self._devs = USBDevices(traverse=True)
        for d in self._devs:
            self.device_list_box.Insert(d.as_compact_str(),
                                        self.device_list_box.Count, d)

    def __set_properties(self):
        self.SetTitle("USBProbe")
        self.SetSize((525, 533))
        self.top_frame_statusbar.SetStatusWidths([-1])
        # statusbar fields
        top_frame_statusbar_fields = ["top_frame_statusbar"]
        for i in range(len(top_frame_statusbar_fields)):
            self.top_frame_statusbar.SetStatusText(
                                            top_frame_statusbar_fields[i], i)

    def layout_selection_panel(self):
        """
        Layout for panel to display items user can select.

        selection_panel
          sizer_selection_panel
            selection_sizer
              selection_splitter
                selection_panel_pane_L
                  sizer_left
                    device_lbl
                    device_list_box
                selection_panel_pane_R
                  sizer_right
                    interfaces_lbl
                    tree_usb_probe
        """

        sizer_left = wx.BoxSizer(wx.VERTICAL)
        sizer_left.Add(self.device_lbl, 0, wx.ALL, 10)
        sizer_left.Add(self.device_list_box, 1,
                       wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 10)
        self.selection_panel_pane_L.SetSizer(sizer_left)

        sizer_right = wx.BoxSizer(wx.VERTICAL)
        sizer_right.Add(self.interfaces_lbl, 0, wx.ALL, 10)
        sizer_right.Add(self.tree_usb_probe, 1,
                        wx.EXPAND | wx.RIGHT | wx.BOTTOM, 10)
        self.selection_panel_pane_R.SetSizer(sizer_right)

        self.selection_splitter.SplitVertically(self.selection_panel_pane_L,
                                                self.selection_panel_pane_R)

        selection_sizer = wx.BoxSizer(wx.HORIZONTAL)
        selection_sizer.Add(self.selection_splitter, 1, wx.EXPAND, 0)
        self.selection_panel.SetSizer(selection_sizer)

    def layout_display_panel(self):
        """
        Layout for panel to display info about selected item.

        display_panel
          display_sizer
          button_sizer
            button_close
        """
        display_sizer = wx.BoxSizer(wx.VERTICAL)
        button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        button_sizer.AddStretchSpacer()
        button_sizer.Add(self.button_close, proportion=0, flag=wx.ALL,
                         border=10)
        display_sizer.Add(self.display_html, proportion=1,
                          flag=wx.EXPAND | wx.TOP | wx.RIGHT | wx.LEFT,
                          border=10)
        display_sizer.Add(button_sizer, flag=wx.EXPAND)
        self.display_panel.SetSizer(display_sizer)

    def __do_layout(self):
        top_sizer = wx.BoxSizer(wx.VERTICAL)
        panel_sizer = wx.BoxSizer(wx.VERTICAL)
        self.layout_selection_panel()
        self.layout_display_panel()
        panel_sizer.Add(self.selection_panel, 1, wx.EXPAND, 0)
        panel_sizer.Add(self.display_panel, 1, wx.EXPAND, 0)
        self.top_panel.SetSizer(panel_sizer)
        top_sizer.Add(self.top_panel, 1, wx.EXPAND, 0)
        self.SetSizer(top_sizer)
        self.Layout()

    def closeOnClick(self, event):
        self.Close(True)
        event.Skip()  # probably not necessary :)

    def OnClick(self, event):
        """
        Respond to click in list box by populating the tree control,
        and displaying the device information in the info pane.

        """
        selected_id = self.device_list_box.GetSelection()
        tree_root_txt = self.device_list_box.GetString(selected_id)
        self.selected_dev = self.device_list_box.GetClientData(selected_id)
        self.tree_usb_probe.DeleteAllItems()
        self.tree_root = self.tree_usb_probe.AddRoot(tree_root_txt)
        self.show_device_info(self.selected_dev)
        #for each device configuration:
        #  add to device
        #  for each configuration interface:
        #    add to config
        #    for each interface endpoint
        #      add to interface
        for conf in self.selected_dev.configs:
            new_config = self.tree_usb_probe.AppendItem(self.tree_root,
                                        unicode(conf), wx.ID_ANY, wx.ID_ANY)
            #have to have item selected for
            self.tree_usb_probe.SelectItem(new_config)
            for intfc in conf.interfaces:
                new_intfc = self.tree_usb_probe.AppendItem(
                    new_config, unicode(intfc), wx.ID_ANY, wx.ID_ANY, None)
                for endp in intfc.endpoints:
                    self.tree_usb_probe.AppendItem(new_intfc, unicode(endp),
                                                   wx.ID_ANY, wx.ID_ANY, None)
        event.Skip()

    def onTreeSelectChange(self, evt):
        """
        Change display whenever a tree item is selected.

        """
        print("onTreeSelectChange")
        evt.Skip()

# end of class USBTopFrame


class USBProbeMain(wx.App):
    def OnInit(self):
        wx.InitAllImageHandlers()
        top_frame = USBTopFrame(None, -1, "")
        self.SetTopWindow(top_frame)
        top_frame.Show()
        return 1

# end of class USBProbeMain

if __name__ == "__main__":
    USBProbe = USBProbeMain(0)
    USBProbe.MainLoop()
