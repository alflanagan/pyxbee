'''
Created on Jul 8, 2012

@author: lloyd
'''


class WriteException(Exception):
    """
    Raised by a Setting type when an attempted write fails (is setting
    read-only?)
    """
    pass


class ReadException(Exception):
    pass


class UnboundSetting(object):
    def __init__(self, name, at_cmds, encoding="hex", tooltip=''):
        """
        name: short readable name for setting.
        at_cmds: tuple of one or more two-byte strings, used to get/set value.
                 For multi-byte commands, the one to set high bytes comes
                 first.
        encoding: encoding of value, useful for display, etc.
            Acceptable values:
            # any encoding string accepted by str() (usually "ascii")
            # "hex" to display as hex string
            # "enabled" to display 0 as "disabled" and 1 as "enabled"
        """
        self.name = name
        self.at_cmds = at_cmds
        self.encoding = "hex"
        self.tooltip = tooltip

    def value(self):
        """Reads value from device, returns bytes() of response"""
        return b""


class ReadableSetting(UnboundSetting):
    def __init__(self, xbee, *args, **kwargs):
        super(ReadableSetting, self).__init__(*args, **kwargs)
        self.device = xbee

    @staticmethod
    def hex_str(data):
        result = ''
        for bytein in data:
            result += '{:02X}'.format(bytein)
        return result

    @property
    def value(self):
        """
        Reads value from the device. Result format depends on encoding setting.

        @return: The current setting for the device.
        @rtype: str
        """
        result = ""
        try:
            self.xb
        except AttributeError as ae:
            raise ReadException("no xbee device found")
        for cmd in self.at_cmds:
            self.xb.at(command=cmd)
            resp = self.xb.wait_read_frame()
            try:
                returned_val = resp["parameter"]
                if self.encoding == "hex":
                    result += self.hex_str(returned_val)
                elif self.encoding == "enabled":
                    if returned_val == 0:
                        result = "disabled"
                    else:
                        result = "enabled"
                else:
                    result += str(returned_val, self.encoding)
            except KeyError:
                result = "N/A"
        return result

    @value.setter
    def write(self, new_val):
        raise WriteException("This value is read-only.")


class WritableSetting(ReadableSetting):

    def __init__(self, xbee, *args, **kwargs):
        super(WritableSetting, self).__init__(xbee, *args, **kwargs)

    def write(self, new_val):
        pass


class Settings(object):
    """
    A class to hold a collection of settings. Allows us to create a group of
    unbound settings, and then, when we've selected an XBee device, to get a
    group of the settings bound to a given device.
    """
    def __init__(self, cmds, *args, **kwargs):
        """
        @param cmds: commands to keep
        @type cmds: string iterable
        """
        super(Settings, self).__init__(*args, **kwargs)
        self.cmds = cmds
        self.stgs = {}

    def bind(self, xbee_device):
        for cmd in self.cmds:
            data = list(at_cmds[cmd])
            #fill in default values depending on current length
            if len(data) == 1:
                data.append("")
            if len(data) == 2:
                data.append(False)
            if len(data) == 3:
                data.append("hex")
            if data[2]:
                new_bound = ReadableSetting(xbee_device, name=cmd, at_cmds=data[0],
                                             encoding=data[3], tooltip=data[1])
            else:
                new_bound = WritableSetting(xbee_device, name=cmd, at_cmds=data[0],
                                            encoding=data[3], tooltip=data[1])
            self.stgs[cmd] = new_bound

    def read_all(self):
        values = {}
        for cmd in self.cmds:
            values[cmd] = self.stgs[cmd].value
        return values

    def __getitem__(self, name):
        try:
            return self.stgs[name]
        except KeyError:
            if name in self.cmds:
                raise ReadException("Setting object is not bound to xbee device")
            else:
                raise ReadException("I don't know about setting '{}'".format(name))

at_cmds = {
    "PAN ID": ("ID", "Network ID for this node"),
    "Serial": (("SH", "SL"), "Serial number for the device", True),
    "Destination": (("DH", "DL"),
                    ("The 64-bit destination address. Special values include "
                     "0x000000000000FFFF (broadcast) and 0x0000000000000000 "
                     "(coordinator).")),
    "Address": (("MY",), "Current network address for this node", True),
    "Children Avail": (("NC",), "", True),
    "Max Payload": (("NP",), "", True),
    "Node ID": (("NI",), "", True, "ascii"),
    "Version": (("",), "", True),
    "Parent Addr": (("MP",), "16-bit Parent Network Address. 0xFFFE means the module does not have a parent.", True),
    "Remaining Kids": (("NC",), "Reads the number of end device children that can join the device.", True),
    "Source Endpt": (("SE",), "Sets/reads the ZigBee application layer source endpoint value. This value will be used as the source endpoint for all data transmissions. SE is only supported in AT firmware. The default value (0xE8) is the Digi data endpoint."),
    }
