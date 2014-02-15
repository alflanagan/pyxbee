'''
Created on Jun 7, 2012

@author: lloyd
'''
from gi.repository import Gtk  # @UnresolvedImport
from xbee import ZigBee
from serial import Serial
from model.xbee.config import Settings

class SettingContents(object):
    """
    Defines common functionality of classes to "own" contents of
    GridSizer set up to display basic settings of the XBee device.
    """
    TIMEOUT = 2  # seconds
    "Timeout for serial port reads"

    def __init__(self, names, labels, entries, baud_rate):
        """
        @param names: Names for the settings displayed (any of the ones defined
        in settings module)
        @type: string iterable
        @param labels: Widgets to display labels for fields
        @type labels: iterable of Gtk.Label or equivalent
        @param entries: Widgets for entry and display of setting value
        @type entries: iterable of Gtk.Entry or equivalent
        @param baud_rate: baud rate for Serial port
        @type baud_rate: integer in Serial.BAUDRATES
        """
        # print(names)
        self.settings = Settings(names)
        self.baud_rate = baud_rate
        self.stg_lbls = labels
        """Gtk.Label objects for page, indexed by label's text."""
        self.stg_entries = entries
        """Gtk.Entry objects for page, indexed by label's text."""
        self.current_port = None
        self.xb_radio = None

    def _set_device(self, device_name):
        "Binds this object to device, allowing it to display/edit settings for that device."
# args to serial
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
        self.current_port = Serial(port=device_name, baudrate=self.baud_rate, timeout=self.TIMEOUT)
        self.xb_radio = ZigBee(self.current_port, shorthand=True, escaped=False)
        assert self.xb_radio
        self.settings.bind(self.xb_radio)

    def populate(self):
        "Read settings from device and save them."
        curr_vals = self.settings.read_all()
        for stg in self.settings:
            val = curr_vals[stg]
            self.stg_entries[stg].set_text(val)


class NotebookPageSettingContents(SettingContents):
    "Defines a notebook page which contains a GridSizer set up to display/edit settings."

    ATCMDS = ()
    SETTINGS_COUNT = 9  # max settings/page

    def __init__(self, device_name, grid_sizer_to_populate, baud_rate, *args, **kwargs):
        isinstance(grid_sizer_to_populate, Gtk.Grid)
        grid_sizer_to_populate.set_row_homogeneous(False)
        grid_sizer_to_populate.set_hexpand(False)
        self.baud_rate = baud_rate
        self.stg_lbls = {}
        self.stg_entries = {}
        for lbl in self.ATCMDS:
            self.stg_lbls[lbl] = Gtk.Label(lbl, hexpand=False)
            self.stg_entries[lbl] = Gtk.Entry(hexpand=False)
            grid_sizer_to_populate.add(self.stg_lbls[lbl])
            grid_sizer_to_populate.attach_next_to(self.stg_entries[lbl],
                                                  self.stg_lbls[lbl],
                                                  Gtk.PositionType.RIGHT, 1, 1)
        for _ in range(self.SETTINGS_COUNT - len(self.ATCMDS)):
            pad1 = Gtk.Label("")
            grid_sizer_to_populate.add(pad1)
            grid_sizer_to_populate.attach_next_to(Gtk.Label(""),
                                                  pad1,
                                                  Gtk.PositionType.RIGHT, 1, 1)

        super(NotebookPageSettingContents, self).__init__(self.ATCMDS, self.stg_lbls,
                                                   self.stg_entries, self.baud_rate,
                                                   *args, **kwargs)
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
    "A notebook page which displays settings related to ZigBee networking."
    ATCMDS = ("PAN ID", "Oper Channel", "Oper PAN ID", "Max Uni Hops", "Bcast Hops",
              "Disc T/O", "Disc Opt", "Scan Channels", "Scan Duration",)


class Network2SettingContents(NotebookPageSettingContents):
    "Another notebook page to display settings for networking."
    ATCMDS = ("Stack Prof", "Join Time", "Chan Ver", "Net WD TO", "Join Notif", "Aggr Rtg Not")
