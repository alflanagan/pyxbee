# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals
#com.alloydflanagan.hardware.xbee.APIFrame
"""
Created on Apr 27, 2012

@author: A. Lloyd Flanagan

"""

#This file is part of Pyxb.

#Pyxb is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.

#Pyxb is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.

#You should have received a copy of the GNU General Public License
#along with Pyxb.  If not, see <http://www.gnu.org/licenses/>.


class PayloadError(Exception):
    pass


class APIFrame(object):
    '''
    Basic scaffolding for a frame in XBee's API. Handles start byte, length,
    checksum.
    '''
    START_BYTE = 0x7E
    "Common start byte for all communications"

    def __init__(self, payload):
        '''
        Constructor

        payload: byte array (str) containing command for an XBee.
        '''
        self.buff = b'\x7E'
        plength = len(payload)
        if plength > 0xFF * 0xFF - 1:
            raise PayloadError("payload too large")
        lsb = plength & 0xFF
        msb = plength // 256
        print("{:#02x} {:02x}".format(msb, lsb))
        self.buff += chr(msb)
        self.buff += chr(lsb)
        assert len(self.buff) == 3
        chksum = 0
        for x in payload:
            chksum + ord(x)
        chksum = chksum & 0xFF
        self.buff += payload
        self.buff += chr(chksum)
        assert len(self.buff) == 4 + len(payload)

    def get_payload(self):
        return self.buff[3:-1]

if __name__ == '__main__':
    t1 = b'abcdefgtasfsd'
    test = APIFrame(t1)
    t1a = test.get_payload()
    assert t1a == t1
    t2 = t1 * 300
    test2 = APIFrame(t2)
    t2a = test2.get_payload()
    assert t2 == t2a
    t3 = t2 * 300
    try:
        test3 = APIFrame(t3)
        raise Exception("APIFrame failed to raise payload too large exception")
    except PayloadError:
        print("Expected error received -- payload too large")
    del t3
