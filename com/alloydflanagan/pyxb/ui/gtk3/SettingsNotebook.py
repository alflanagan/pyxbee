'''
Created on Jun 7, 2012

@author: lloyd
'''
from gi.repository import Gtk  # @UnresolvedImport
from xbee import ZigBee
from serial import Serial
from com.alloydflanagan.hardware.xbee.Settings import Setting


class SettingContents(object):
    """
    Defines common functionality of classes to "own" contents of
    GridSizer set up to display basic settings of the XBee device.
    """
    def __init__(self):
        super(SettingContents, self).__init__()
        self.settings = {}
        """
        dict of labels for settings field --> AT command used to get/set
        that value. if two commands given, they set/return high and low parts
        of a 64-bit value.
        """
        self.stg_lbls = {}
        """Gtk.Label objects for page, indexed by label's text."""
        self.stg_values = {}
        """Gtk.Entry objects for page, indexed by label's text."""

    def _set_device(self, device_name):
#args to serial
#         port = None,           # number of device, numbering starts at
#                                # zero. if everything fails, the user
#                                # can specify a device string, note
#                                # that this isn't portable anymore
#                                # port will be opened if one is specified
#         baudrate=9600,         # baud rate
#         bytesize=EIGHTBITS,    # number of data bits
#         parity=PARITY_NONE,    # enable parity checking
#         stopbits=STOPBITS_ONE, # number of stop bits
#         timeout=None,          # set a timeout value, None to wait forever
#         xonxoff=False,         # enable software flow control
#         rtscts=False,          # enable RTS/CTS flow control
#         writeTimeout=None,     # set a timeout for writes
#         dsrdtr=False,          # None: use rtscts setting, dsrdtr
#                                #override if True or False
#         interCharTimeout=None  # Inter-character timeout, None to disable
        self.current_port = Serial(port=device_name)
        self.xb = ZigBee(self.current_port, shorthand=True, escaped=False)
        for stg in self.settings:
            self.settings[stg].set_device(self.xb)

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
        self.stg_values[field].set_text(str(value))

    def populate(self):
        for stg in self.settings:
            val = self.settings[stg].read_value()
            self.stg_values[stg].set_text(val)


class BasicSettingContents(SettingContents):
    """Class to "own" contents of GridSizer set up to display basic settings of
    the XBee device"""
    def __init__(self, device_name, grid_sizer_to_populate):
        super(BasicSettingContents, self).__init__()

        self.settings = {
            "PAN ID": Setting("pan_id", ("ID",)),
            "Serial": Setting("serial", ("SH", "SL")),
            "Destination": Setting("dest", ("DH", "DL")),
            "Address": Setting("addr", ("MY",)),
            "Children Avail": Setting("kids", ("NC",), writable=False),
            "Max Payload": Setting("max", ("NP",), writable=False),
            "Node ID": Setting("nodeid", ("NI",), writable=False,
                               encoding="ascii"),
            "Version": Setting("ver", ("",), writable=False),
            }

        for lbl in self.settings:
            self.stg_lbls[lbl] = Gtk.Label(lbl)
            self.stg_values[lbl] = Gtk.Entry()
            grid_sizer_to_populate.add(self.stg_lbls[lbl])
            grid_sizer_to_populate.attach_next_to(self.stg_values[lbl],
                                                  self.stg_lbls[lbl],
                                                  Gtk.PositionType.RIGHT, 1, 1)
        self._set_device(device_name)
        self.populate()


class Network1SettingContents(SettingContents):
    """
    Class to "own" some settings related to network
    """
    def __init__(self, device_name, grid_sizer_to_populate, *args, **kwargs):
        super(Network1SettingContents, self).__init__(*args, **kwargs)
        self.settings = {"Oper Channel": Setting("op_chnl", ("CH",),
                                                      writable=False),
                         "Oper PAN ID": Setting("op_pan_id", ("OI",),
                                                     writable=False),
                         "Max Uni Hops": Setting("max_uhops", ("NH",)),
                         "Bcast Hops": Setting("bcast_hops", ("BH",)),
                         "Disc T/O": Setting("node_dto", ("NT",)),
                         "Disc Opt": Setting("ntwk_dopts", ("NO",)),
                         #TODO: custom display for SC
                         "Scan Channels": Setting("scan_chan", ("SC",)),
                         "Scan Duration": Setting("scan_dur", ("SD",)),
                         #"Stack Prof": Setting("stk_prof", ("ZS",)),
                         }

        for lbl in self.settings:
            self.stg_lbls[lbl] = Gtk.Label(lbl)
            self.stg_values[lbl] = Gtk.Entry()
            grid_sizer_to_populate.add(self.stg_lbls[lbl])
            grid_sizer_to_populate.attach_next_to(self.stg_values[lbl],
                                                  self.stg_lbls[lbl],
                                                  Gtk.PositionType.RIGHT, 1, 1)
        self._set_device(device_name)
        self.populate()


class Network2SettingContents(SettingContents):
    """
    Class to "own" some settings related to network
    """
    def __init__(self, device_name, grid_sizer_to_populate, *args, **kwargs):
        super(Network2SettingContents, self).__init__(*args, **kwargs)
        self.settings = {"Stack Prof": Setting("stk_prof", ("ZS",)),
                         "Join Time": Setting("join_tm", ("NJ",)),
                         "Chan Ver": Setting("ch_verif", ("JV",)),
                         "Net WD TO": Setting("ntwk_watch", ("NW",)),
                         "Join Notif": Setting("join_notif", ("JN",)),
                         "Aggr Rtg Not": Setting("aggr_rtg", ("AR",)),
                         }

        for lbl in self.settings:
            self.stg_lbls[lbl] = Gtk.Label(lbl)
            self.stg_values[lbl] = Gtk.Entry()
            grid_sizer_to_populate.add(self.stg_lbls[lbl])
            grid_sizer_to_populate.attach_next_to(self.stg_values[lbl],
                                                  self.stg_lbls[lbl],
                                                  Gtk.PositionType.RIGHT, 1, 1)
        self._set_device(device_name)
        self.populate()