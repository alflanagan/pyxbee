#!/usr/bin/env python
# -*- coding: utf-8 -*-
# generated by wxGlade 0.6.3 on Sun Mar 18 23:09:16 2012

import wx
from wx._core import Size
from com.alloydflanagan.hardware.usb.Devices import USBDevices

# begin wxGlade: extracode
# end wxGlade

class USBTopFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: USBTopFrame.__init__
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.top_panel = wx.Panel(self, -1)
        self.display_panel = wx.Panel(self.top_panel, -1)
        self.notebook_1 = wx.Notebook(self.display_panel, -1, style=0)
        self.notebook_1_pane_1 = wx.Panel(self.notebook_1, -1)
        self.selection_panel = wx.Panel(self.top_panel, -1)
        self.selection_splitter = wx.SplitterWindow(self.selection_panel, -1, style=wx.SP_3D|wx.SP_BORDER)
        self.selection_panel_pane_2 = wx.Panel(self.selection_splitter, -1)
        self.selection_panel_pane_1 = wx.Panel(self.selection_splitter, -1)
        self.top_frame_statusbar = self.CreateStatusBar(1, wx.ST_SIZEGRIP)
        self.device_list_box = wx.ListBox(self.selection_panel_pane_1, -1, choices=[], style=wx.LB_SINGLE|wx.LB_NEEDED_SB)
        self.tree_usb_probe = wx.TreeCtrl(self.selection_panel_pane_2, -1, style=wx.TR_HAS_BUTTONS|wx.TR_NO_LINES|wx.TR_DEFAULT_STYLE|wx.SUNKEN_BORDER)
        self.label_1 = wx.StaticText(self.notebook_1_pane_1, -1, "Spec:")
        self.label_2 = wx.StaticText(self.notebook_1_pane_1, -1, "USB Version")
        self.label_3 = wx.StaticText(self.notebook_1_pane_1, -1, "Class:")
        self.label_4 = wx.StaticText(self.notebook_1_pane_1, -1, "Vendor:")
        self.product_lbl = wx.StaticText(self.notebook_1_pane_1, -1, "Product: ")
        self.button_close = wx.Button(self.display_panel, -1, "&Close")

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_LISTBOX, self.OnClick, self.device_list_box)
        self.Bind(wx.EVT_BUTTON, self.closeOnClick, self.button_close)
        # end wxGlade
        self.initial_size = Size(440, 516)
        self.SetSize(self.initial_size)
        self.populate_usb_list()
        self.selected_dev = None
        '''currently selected device entry, if any'''
        
    def populate_usb_list(self):
        self._devs = USBDevices(traverse=True)
        for d in self._devs:
            #print(dir(self.list_box_1_copy))
            self.device_list_box.Insert(d.as_compact_str(), self.device_list_box.Count, d)
            
    def __set_properties(self):
        # begin wxGlade: USBTopFrame.__set_properties
        self.SetTitle("USBProbe")
        self.SetSize((440, 516))
        self.top_frame_statusbar.SetStatusWidths([-1])
        # statusbar fields
        top_frame_statusbar_fields = ["top_frame_statusbar"]
        for i in range(len(top_frame_statusbar_fields)):
            self.top_frame_statusbar.SetStatusText(top_frame_statusbar_fields[i], i)
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: USBTopFrame.__do_layout
        top_sizer = wx.BoxSizer(wx.VERTICAL)
        panel_sizer = wx.BoxSizer(wx.VERTICAL)
        display_sizer = wx.BoxSizer(wx.VERTICAL)
        button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        grid_sizer_1 = wx.GridSizer(5, 4, 0, 0)
        selection_sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer_6 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_5 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_5.Add(self.device_list_box, 1, wx.EXPAND, 0)
        self.selection_panel_pane_1.SetSizer(sizer_5)
        sizer_6.Add(self.tree_usb_probe, 1, wx.EXPAND, 0)
        self.selection_panel_pane_2.SetSizer(sizer_6)
        self.selection_splitter.SplitVertically(self.selection_panel_pane_1, self.selection_panel_pane_2)
        selection_sizer.Add(self.selection_splitter, 1, wx.EXPAND, 0)
        self.selection_panel.SetSizer(selection_sizer)
        panel_sizer.Add(self.selection_panel, 1, wx.EXPAND, 0)
        grid_sizer_1.Add(self.label_1, 0, 0, 0)
        grid_sizer_1.Add(self.label_2, 0, 0, 0)
        grid_sizer_1.Add(self.label_3, 0, 0, 0)
        grid_sizer_1.Add(self.label_4, 0, 0, 0)
        grid_sizer_1.Add(self.product_lbl, 0, 0, 0)
        self.notebook_1_pane_1.SetSizer(grid_sizer_1)
        self.notebook_1.AddPage(self.notebook_1_pane_1, "Device")
        display_sizer.Add(self.notebook_1, 1, wx.EXPAND, 0)
        button_sizer.Add(self.button_close, 0, 0, 0)
        display_sizer.Add(button_sizer, 0, wx.EXPAND, 0)
        self.display_panel.SetSizer(display_sizer)
        panel_sizer.Add(self.display_panel, 1, wx.EXPAND, 0)
        self.top_panel.SetSizer(panel_sizer)
        top_sizer.Add(self.top_panel, 1, wx.EXPAND, 0)
        self.SetSizer(top_sizer)
        self.Layout()
        # end wxGlade

    def closeOnClick(self, event): # wxGlade: USBTopFrame.<event_handler>
        self.Close(True)
        #print "Event handler `closeOnClick' not implemented"
        #event.Skip()

    #for some reason, wxGlade keeps adding an OnClick event even though
    #this exists. If it does, you'll have to delete the duplicate.
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
        #for each device configuration:
        #  add to device
        #  for each configuration interface:
        #    add to config
        #    for each interface endpoint
        #      add to interface
        for conf in self.selected_dev.configs:
            new_config = self.tree_usb_probe.AppendItem(self.tree_root, unicode(conf), wx.ID_ANY, wx.ID_ANY)
            for intfc in conf.interfaces:
                new_intfc = self.tree_usb_probe.AppendItem(new_config, unicode(intfc), wx.ID_ANY, wx.ID_ANY, None)
                for endp in intfc.endpoints:
                    new_endp = self.tree_usb_probe.AppendItem(new_intfc, unicode(endp), wx.ID_ANY, wx.ID_ANY, None)
                    
        #for 
        

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
