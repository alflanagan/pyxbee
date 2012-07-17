'''
Created on Jun 7, 2012

@author: lloyd
'''
from gi.repository import Gtk  # @UnresolvedImport
from xbee import ZigBee
from serial import Serial
from com.alloydflanagan.hardware.xbee.Settings import WriteException, \
    ReadException, ReadableSetting, WritableSetting, Settings


class SettingContents(object):
    """
    Defines common functionality of classes to "own" contents of
    GridSizer set up to display basic settings of the XBee device.
    """
    def __init__(self, names, labels, entries):
        """
        @param names: Names for the settings displayed (any of the ones defined
        in settings module)
        @type: string iterable
        @param labels: Widgets to display labels for fields
        @type labels: iterable of Gtk.Label or equivalent
        @param entries: Widgets for entry and display of setting value
        @type entries: iterable of Gtk.Entry or equivalent
        """
        self.settings = Settings(names)
        self.stg_lbls = labels
        """Gtk.Label objects for page, indexed by label's text."""
        self.stg_entries = entries
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
        assert self.xb
        self.settings.bind(self.xb)

    def populate(self):
        curr_vals = self.settings.read_all()
        for stg in self.settings:
            val = curr_vals[stg]
            self.stg_entries[stg].set_text(val)


class BasicSettingContents(SettingContents):
    """Class to "own" contents of GridSizer set up to display basic settings of
    the XBee device"""

    ATCMDS = ("PAN ID", "Serial", "Destination", "Address", "Children Avail",
              "Max Payload", "Node ID", "Version",)

    def __init__(self, device_name, grid_sizer_to_populate, *args, **kwargs):
        self.stg_lbls = {}
        self.stg_entries = {}
        for lbl in BasicSettingContents.ATCMDS:
            self.stg_lbls[lbl] = Gtk.Label(lbl)
            self.stg_entries[lbl] = Gtk.Entry()
            grid_sizer_to_populate.add(self.stg_lbls[lbl])
            grid_sizer_to_populate.attach_next_to(self.stg_entries[lbl],
                                                  self.stg_lbls[lbl],
                                                  Gtk.PositionType.RIGHT, 1, 1)
        super(BasicSettingContents, self).__init__(BasicSettingContents.ATCMDS, self.stg_lbls,
                                                   self.stg_entries, *args, **kwargs)
        self._set_device(device_name)
        self.populate()
        for cmd in BasicSettingContents.ATCMDS:
            self.stg_lbls[cmd].set_tooltip_text(self.settings[cmd].tooltip)


class Network1SettingContents(SettingContents):
    """
    Class to "own" some settings related to network
    """
    def __init__(self, device_name, grid_sizer_to_populate, *args, **kwargs):
        pass
#        super(Network1SettingContents, self).__init__(*args, **kwargs)
#        self.settings = {"Oper Channel": Setting("op_chnl", ("CH",),
#                                                      writable=False),
#                         "Oper PAN ID": Setting("op_pan_id", ("OI",),
#                                                     writable=False),
#                         "Max Uni Hops": Setting("max_uhops", ("NH",)),
#                         "Bcast Hops": Setting("bcast_hops", ("BH",)),
#                         "Disc T/O": Setting("node_dto", ("NT",)),
#                         "Disc Opt": Setting("ntwk_dopts", ("NO",)),
#                         #TODO: custom display for SC
#                         "Scan Channels": Setting("scan_chan", ("SC",)),
#                         "Scan Duration": Setting("scan_dur", ("SD",)),
#                         #"Stack Prof": Setting("stk_prof", ("ZS",)),
#                         }
#
#        for lbl in self.settings:
#            self.stg_lbls[lbl] = Gtk.Label(lbl)
#            self.stg_entries[lbl] = Gtk.Entry()
#            grid_sizer_to_populate.add(self.stg_lbls[lbl])
#            grid_sizer_to_populate.attach_next_to(self.stg_entries[lbl],
#                                                  self.stg_lbls[lbl],
#                                                  Gtk.PositionType.RIGHT, 1, 1)
#        self._set_device(device_name)
#        self.populate()


class Network2SettingContents(SettingContents):
    """
    Class to "own" some settings related to network
    """
    def __init__(self, device_name, grid_sizer_to_populate, *args, **kwargs):
        pass
#        super(Network2SettingContents, self).__init__(*args, **kwargs)
#        self.settings = {"Stack Prof": Setting("stk_prof", ("ZS",)),
#                         "Join Time": Setting("join_tm", ("NJ",)),
#                         "Chan Ver": Setting("ch_verif", ("JV",)),
#                         "Net WD TO": Setting("ntwk_watch", ("NW",)),
#                         "Join Notif": Setting("join_notif", ("JN",)),
#                         "Aggr Rtg Not": Setting("aggr_rtg", ("AR",)),
#                         }
#
#        for lbl in self.settings:
#            self.stg_lbls[lbl] = Gtk.Label(lbl)
#            self.stg_entries[lbl] = Gtk.Entry()
#            grid_sizer_to_populate.add(self.stg_lbls[lbl])
#            grid_sizer_to_populate.attach_next_to(self.stg_entries[lbl],
#                                                  self.stg_lbls[lbl],
#                                                  Gtk.PositionType.RIGHT, 1, 1)
#        self._set_device(device_name)
#        self.populate()
