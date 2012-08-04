'''
Created on Jun 7, 2012

@author: lloyd
'''
from gi.repository import Gtk  # @UnresolvedImport
from xbee import ZigBee
from serial import Serial
from com.alloydflanagan.hardware.xbee.Settings import Settings


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
        #print(names)
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


class NotebookPageSettingContents(SettingContents):

    ATCMDS = ()
    SETTINGS_COUNT = 9 #max settings/page

    def __init__(self, device_name, grid_sizer_to_populate, *args, **kwargs):
        self.stg_lbls = {}
        self.stg_entries = {}
        for lbl in self.ATCMDS:
            self.stg_lbls[lbl] = Gtk.Label(lbl)
            self.stg_entries[lbl] = Gtk.Entry()
            grid_sizer_to_populate.add(self.stg_lbls[lbl])
            grid_sizer_to_populate.attach_next_to(self.stg_entries[lbl],
                                                  self.stg_lbls[lbl],
                                                  Gtk.PositionType.RIGHT, 1, 1)
        for unused in range(self.SETTINGS_COUNT - len(self.ATCMDS)):
            pad1 = Gtk.Label("")
            grid_sizer_to_populate.add(pad1)
            grid_sizer_to_populate.attach_next_to(Gtk.Label(""),
                                                  pad1,
                                                  Gtk.PositionType.RIGHT, 1, 1)

        super(NotebookPageSettingContents, self).__init__(self.ATCMDS, self.stg_lbls,
                                                   self.stg_entries, *args, **kwargs)
        self._set_device(device_name)
        self.populate()
        for cmd in self.ATCMDS:
            self.stg_lbls[cmd].set_tooltip_text(self.settings[cmd].tooltip)


class BasicSettingContents(NotebookPageSettingContents):
    """Class to "own" contents of GridSizer set up to display basic settings of
    the XBee device"""

    ATCMDS = ("Version", "Serial", "Destination", "Address", "Children Avail",
              "Max Payload", "Node ID", "Device Type", "HW Version",)


class Network1SettingContents(NotebookPageSettingContents):
    """
    Class to "own" some settings related to network
    """
    ATCMDS = ("PAN ID", "Oper Channel", "Oper PAN ID", "Max Uni Hops", "Bcast Hops",
              "Disc T/O", "Disc Opt", "Scan Channels", "Scan Duration",)


class Network2SettingContents(NotebookPageSettingContents):

    ATCMDS = ("Stack Prof", "Join Time", "Chan Ver", "Net WD TO", "Join Notif", "Aggr Rtg Not")
