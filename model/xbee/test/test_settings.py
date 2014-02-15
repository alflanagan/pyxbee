'''
Unit tests for the Settings module.

@author: A. Lloyd Flanagan

'''

import unittest
import serial

from xbee.base import ReadTimeoutException
from xbee import ZigBee

from hardware.xbee.config import ReadableSetting, ReadException, WritableSetting, Settings, at_cmds


class TestSettings(unittest.TestCase):
    """Unit tests for hardware.xbee.Settings object."""

    @classmethod
    def setUpClass(cls):
        cls.settings = Settings(at_cmds.keys())

    def test_readall(self):
        port = serial.Serial('/dev/ttyUSB0', 38400)
        xbee_device = ZigBee(port)
        self.settings.bind(xbee_device)
        read_settings = self.settings.read_all()
        #TODO: clearly we need to allow for other versions, etc.
        self.assertEqual(read_settings['Version'], '21A7 Coord(API)')
        #TODO: and this needs to be configurable
        self.assertEqual(read_settings['PAN ID'], '000000000BADFACE')
        xbee_device.halt()
        port.close()

    def test_read_timeout(self):
        port = serial.Serial('/dev/ttyUSB0', 9600)
        xbee_device = ZigBee(port)
        self.settings.bind(xbee_device)
        self.assertRaises(ReadException,
                          self.settings.read_all)
        xbee_device.halt()
        port.close()


if __name__ == '__main__':
    unittest.main()
