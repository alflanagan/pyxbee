'''
Created on Jun 7, 2012

@author: lloyd
'''
from gi.repository import Gtk, GObject #@UnresolvedImport
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


class BasicSettingContents(object):
    """Class to "own" contents of GridSizer set up to display basic settings of the XBee device"""

    def __init__(self, device_name, grid_sizer_to_populate):
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
        self.stg_lbls = {}
        self.stg_values = {}
        
        for lbl in self.settings:
            self.stg_lbls[lbl] = Gtk.Label(lbl)
            self.stg_values[lbl] = Gtk.Entry()
            grid_sizer_to_populate.add(self.stg_lbls[lbl])
            grid_sizer_to_populate.add(self.stg_values[lbl])
            
        
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
    def xbee(self, xbee):
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
