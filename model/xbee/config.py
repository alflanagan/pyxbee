'''
Created on Jul 8, 2012

@author: lloyd
'''
from collections import MutableMapping  # help Settings emulate dictionary
from serial import SerialTimeoutException
from xbee import ZigBee


class WriteException(Exception):
    """
    Raised by a Setting type when an attempted write fails (is setting
    read-only?)
    """
    pass


class ReadException(Exception):
    pass


class UnboundSetting(object):
    def __init__(self, name, setting_cmds, encoding="hex", tooltip=''):
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
        self.setting_cmds = setting_cmds
        self.encoding = encoding
        self.tooltip = tooltip

    def value(self):
        """Reads value from device, returns bytes() of response"""
        return b""


def disp_version(firmware_version):
    # TODO: We need a whole data structure with device model, firmware version, etc.
# 20xx - Coordinator - AT/Transparent Operation
# - 21xx - Coordinator - API Operation
# - 22xx - Router - AT/Transparent Operation
# - 23xx - Router - API Operation
# - 28xx - End Device - AT/Transparent Operation
# - 29xx - End Device - API Operation
    prefix = int.from_bytes(firmware_version[:1], 'big')
    verint = int.from_bytes(firmware_version, 'big')
    vstr = "{:X}".format(verint)
    vers_strs = {0x20: "{} Coord(AT)",
                 0x21: "{} Coord(API)",
                 0x22: "{} Routr(AT)",
                 0x23: "{} Routr(API)",
                 0x28: "{} End(AT)",
                 0x29: "{} End(API)",
                 }
    try:
        return vers_strs[prefix].format(vstr)
    except KeyError:
        return "{} unknown".format(vstr)


class ReadableSetting(UnboundSetting):
    def __init__(self, xbee, timeout=5, *args, **kwargs):
        super(ReadableSetting, self).__init__(*args, **kwargs)
        self.device = xbee
        assert isinstance(self.device, ZigBee)
        self.timeout = timeout

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
            self.device
        except AttributeError:
            raise ReadException("no xbee device found")

        # send each AT cmd, accumulate result
        for cmd in self.setting_cmds:
            self.device.at(command=cmd)
            try:
                resp = self.device.wait_read_frame(self.timeout)
            except SerialTimeoutException as e:
                raise ReadException("Timeout on command '{}'".format(cmd)) from e

            try:
                returned_val = resp["parameter"]
                if self.encoding == "hex":
                    result += self.hex_str(returned_val)
                elif self.encoding == "enabled":
                    if returned_val == 0:
                        result += "disabled"
                    else:
                        result += "enabled"
                elif self.encoding == "version":
                    result += disp_version(returned_val)
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


class Settings(MutableMapping):
    """
    A class to hold a collection of settings. Basically a dictionary of Setting objects, with
    additional methods for binding them to a device, reading all of them from the device, etc.
    """
    def __init__(self, names, *args, **kwargs):
        """
        Create Settings objects containing the settings specified in the names argument. Elements
        in names become the keys to the Settings dictionary.

        For now at least, each item in names should be a key to the at_cmds global structure.

        @param names: List of settings stored in this group
        @type names: iterable of immutable objects (usually strings)
        """
        super(Settings, self).__init__(*args, **kwargs)
        self.names = list(names)  # make our own copy!!
        self.stgs = {}

    def bind(self, xbee_device):
        for name in self.names:
            data = list(at_cmds[name])
            # fill in default values depending on current length
            if len(data) == 1:
                data.append("")  # no tooltip
            if len(data) == 2:
                data.append(False)  # setting not writable
            if len(data) == 3:
                data.append("hex")  # returns hex number
            if data[2]:
                new_bound = ReadableSetting(xbee_device, name=name, at_cmds=data[0],
                                             encoding=data[3], tooltip=data[1])
            else:
                new_bound = WritableSetting(xbee_device, name=name, at_cmds=data[0],
                                            encoding=data[3], tooltip=data[1])
            self.stgs[name] = new_bound

    def read_all(self):
        """Reads all settings in collection from the bound device.

        """
        values = {}

        for cmd in self.names:
            values[cmd] = self.stgs[cmd].value

        return values

    def __iter__(self):
        """
        Returns iterator for keys.
        """
        return self.stgs.__iter__()

    def keys(self):
        return self.stgs.keys()

    # define dictionary interface so client never has to refer to stgs directly
    def __getitem__(self, key):
        return self.stgs[key]

    def __setitem__(self, key, new_val):
        """
        Adds / replaces item with key 'key'.

        If new_val is an UnboundSetting object (or subclass thereof), the value gets set directly.
        otherwise new_val should be a key of the at_cmds dictionary.
        """
        # don't see a way around type-checking here that doesn't allow 'bad' things to happen
        if isinstance(new_val, UnboundSetting):
            self.stgs[key] = new_val
        else:
            self.stgs[key] = at_cmds[new_val]

    def __delitem__(self, key):
        """
        Deletes item at key, if any.
        """
        self.stgs.__delitem__(key)

    def __len__(self):
        return self.stgs.__len__()

#Structure defining available AT commands for an XBee
#key is a user-friendly label for the function
#Structure of values:
#1. Tuple of length 1 or 2 2-char byte strings defining commands (if 2, first is for high part of
# result, 2nd is for low part.)
#2. Longer description of command/returned result.
#3. Boolean: True if ...
#4. Encoding: This is a string telling UI how to display/interpret the returned value:
#    hex: display result as hex string (this is default, if not specified)
#    ascii: result is ASCII text
#    enabled: UI should display "enabled" if true, "disabled" if not
at_cmds = {
    "PAN ID": ((b"ID",), "Network ID for this node"),
    "Serial": ((b"SH", b"SL"), "Serial number for the device", True),
    "Destination": ((b"DH", b"DL"),
                    ("The 64-bit destination address. Special values include "
                     "0x000000000000FFFF (broadcast) and 0x0000000000000000 "
                     "(coordinator).")),
    "Address": ((b"MY",), "Current network address for this node", True),
    "Children Avail": ((b"NC",), "", True),
    "Max Payload": ((b"NP",), "", True),
    "Node ID": ((b"NI",), "", True, "ascii"),
    "Parent Addr": ((b"MP",), "16-bit Parent Network Address. 0xFFFE means the module does not have a parent.", True),
    "Remaining Kids": ((b"NC",), "Reads the number of end device children that can join the device.", True),
    "Source Endpt": ((b"SE",), "Sets/reads the ZigBee application layer source endpoint value. This value will be used as the source endpoint for all data transmissions. SE is only supported in AT firmware. The default value (0xE8) is the Digi data endpoint."),

    "Oper Channel": ((b"CH",), "", True),
    "Oper PAN ID": ((b"OI",), "", True),
    "Max Uni Hops": ((b"NH",), ""),
    "Bcast Hops": ((b"BH",), ""),
    "Disc T/O": ((b"NT",), ""),
    "Disc Opt": ((b"NO",), ""),
    # TODO: custom display for SC
    "Scan Channels": ((b"SC",), ""),
    "Scan Duration": ((b"SD",), ""),
    "Stack Prof": ((b"ZS",), ""),
    "Join Time": ((b"NJ",), ""),
    "Chan Ver": ((b"JV",), ""),
    "Net WD TO": ((b"NW",), ""),
    "Join Notif": ((b"JN",), ""),
    "Aggr Rtg Not": ((b"AR",), ""),
    "Device Type": ((b"DD",), ""),
    "Power Level": ((b"PL",), "Broadcast power level. Meaning depends on device."),
    "Power Mode": ((b"PM",), "Power Mode Boost On", True, "enabled"),
    "Rcvd Signal": ((b"DB",), "Received signal power, = value * -1dBm"),
    "Module Temp": ((b"TP",), "Module temperature in deg. C, +-7 deg. (PRO S2B only)"),
    "Version": ((b"VR",), "Firmware Version", False, "version"),
    "HW Version": ((b"HV",), "Hardware version. 19xx -> XBee, 1Axx -> XBee Pro"),
}
