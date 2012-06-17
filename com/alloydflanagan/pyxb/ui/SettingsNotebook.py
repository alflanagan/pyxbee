'''
Created on Jun 7, 2012

@author: lloyd
'''
import wx
from xbee import ZigBee


def hex_str(data):
    result = ''
    for bytein in data:
            result += '{:02X}'.format(ord(bytein))
    return result


class Setting(object):
    """
    Setting for an xbee device. Name, AT command(s) used to get/set it
    whether it's writable, etc.
    """
    def __init__(self, name, at_cmds, writable=True, readable=True):
        self.name = name
        self.cmds = at_cmds
        self.writeable = writable
        self.readable = readable

    @property
    def output_ctrl(self):
        return self.txt_ctrl

    @output_ctrl.setter
    def output_ctrl(self, txt_ctrl):
        self.txt_ctrl = txt_ctrl


class NotebookPage1Panel(wx.Panel):

    def __init__(self, parent, *args, **kwargs):
        super(NotebookPage1Panel, self).__init__(parent, *args, **kwargs)
        self.settings = {
            "PAN ID": Setting("pan_id", "ID"),
            "Serial": Setting("serial", ("SH", "SL")),
            "Destination": Setting("dest", ("DH", "DL")),
            "Address": Setting("addr", "MY"),
            "Children Avail": Setting("kids", "", writable=False),
            "Max Payload": Setting("max", "", writable=False),
            "Encryption?": Setting("crypt", ""),
            "Version": Setting("ver", "", writable=False),
            }
        """dict of labels for settings field --> AT command used to get/set
        that value. if two commands given, they set/return high and low parts
        of a 64-bit value."""

        panel_sizer = wx.FlexGridSizer(rows=len(self.settings), cols=2, vgap=2,
                                       hgap=5)
        panel_sizer.SetFlexibleDirection(wx.HORIZONTAL)
        for lbl in self.settings:
            txt = wx.StaticText(self, label=lbl, style=wx.ALIGN_RIGHT)
            val = wx.TextCtrl(self)
            val.SetMinSize((175, -1))
            self.settings[lbl].output_ctrl = val
            panel_sizer.Add(txt)
            panel_sizer.Add(val)
        self.SetSizer(panel_sizer)

    def _add_prop(self, prop_name):
        """
        Rather than define a getter and setter for every value displayed, we
        generate them dynamically.
        """
        def new_get(self):
            return self.vals[prop_name]

        def new_set(self, new_val):
            #TODO: clearly this needs to actually write value to the device
            self.vals[prop_name] = new_val

        new_prop = property(new_get, new_set)
        setattr(self, prop_name, new_prop)

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


class SettingsNotebook(wx.Notebook):
    '''
    Notebook object which displays/sets values for xbee device.
    '''

    def __init__(self, parent, *args, **kwargs):
        '''
        Create notebook for device xbee.

        @param xbee: Object of type xbee.Zigbee
        '''
        super(SettingsNotebook, self).__init__(parent, *args, **kwargs)
        self.page1 = NotebookPage1Panel(self)
        self.AddPage(self.page1, "Basic")
        #self.SetBackgroundColour("#FF3300")
        sizer = wx.BoxSizer()
        sizer.Add(self.page1, 1, wx.EXPAND)
        self.SetSizer(sizer)
