# vim: fileencoding=utf-8
'''
A single XBee radio device. This will connect to an XBee radio and set itself to be
called back when data is received. Any number of client objects can register as
listeners to get the data passed to them.

'''
from xbee import Zigbee

class XBeeRadio(object):
    def __init__(self, device_port, baudrate, timeout=1):
        self.port_name = device_port
        self.baud = baudrate
        self.timeout = timeout
        self.serial = Serial(port=self.port_name, baudrate=self.baud, timeout=self.timeout)
        #Constructor arguments:
            #ser:    The file-like serial port to use.


            #shorthand: boolean flag which determines whether shorthand command
                       #calls (i.e. xbee.at(...) instead of xbee.send("at",...)
                       #are allowed.

            #callback: function which should be called with frame data
                      #whenever a frame arrives from the serial port.
                      #When this is not None, a background thread to monitor
                      #the port and call the given function is automatically
                      #started.

            #escaped: boolean flag which determines whether the library should
                     #operate in escaped mode. In this mode, certain data bytes
                     #in the output and input streams will be escaped and unescaped
                     #in accordance with the XBee API. This setting must match
                     #the appropriate api_mode setting of an XBee device; see your
                     #XBee device's documentation for more information.
        self.xb = ZigBee(self.serial, shorthand=True, callback=self.xbee_callback, escaped=False)
        self.listeners = []

    @staticmethod
    def hex_str(data):
        result = ''
        for bytein in data:
            result += '{:02X}'.format(bytein)
        return result

    def register_incoming_listener(self, listener):
        """
        listener should be object with data_in(self, data) method, which will be
        called when data is received from radio.
        """
        self.listeners.append(listener)

    def remove_incoming_listener(self, listener):
        self.listeners.remove(listener)

    def xbee_callback(self, data):
        """
        Called by ZigBee when device returns an API frame.
        """
        print("got data from xbee {}".format(self.hex_str(data)))
        for listener in self.listeners:
            listener.data_in(data)
