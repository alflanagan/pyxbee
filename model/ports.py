# vim: fileencoding=utf-8
"""
A module of class(es) to interact with a machine's input/output ports.

Adds functionality not already present in the serial module.

"""
import serial
from serial.tools import list_ports

__all__ = ['PortsList']


class PortsList(object):
    """
    A list of available USB and/or serial ports on the machine.

    """
    TIMEOUT_DEFAULT = 2
    """Timeout (in seconds) for attempting to connect to a serial port."""

    def __init__(self, list_store, timeout=TIMEOUT_DEFAULT):
        """Create a ports list.

        Parameters
        ----------
        list_store : list-like object (has "append")
            Model object which will contain the list of ports. Passing it in
            allows caller to link to UI objects, such as GtkListView.

        """
        assert hasattr(list_store, "append")
        self.ports_list = list_store
        self.timeout = timeout
        self.ports = []


    def populate_devices(self, list_serials, list_usbs):
        """Populates device list.

        Parameters
        ----------
        list_serials : Boolean
            If true, non-USB serial ports will be listed.
        list_usbs : Boolean
            If true, USB ports emulating serial ports will be listed.

        Throws SerialException if attempt to get list of ports fails. However,
        if attempt to open port raises SerialException, just skips that port.
        list_ports will list ports that don't actually exist, so SerialException
        is normal behavior.
        """
        self.ports = list_ports.comports()
        self.ports.sort()
        self.ports_list.clear()
        for port in self.ports:
            try:
                serial.Serial(port[0], timeout=self.timeout)
                if (list_usbs and 'USB' in port[0]) or list_serials:
                    if port[2] == 'n/a':
                        self.ports_list.append((port[0],))
                    else:
                        self.ports_list.append((port[0] + ": " + port[2],))
            except serial.SerialException:
                #Serial() tried to configure port, and failed; probably doesn't
                #actually exist on the machine. Debian linuxes appear to create files for
                #ports that don't exist -- not sure why.
                pass
