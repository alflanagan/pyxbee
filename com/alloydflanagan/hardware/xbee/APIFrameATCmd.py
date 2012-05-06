# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals
#com.alloydflanagan.hardware.xbee.APIFrameATCmd
"""
Created on May 3, 2012

@author: A. Lloyd Flanagan

"""
from com.alloydflanagan.hardware.xbee.APIFrameStream import APIFrameStream
from com.alloydflanagan.hardware.xbee.APIFrame import APIFrame

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


class APIFrameATCmd(APIFrame):
    """
    The type of data frame used to read/set AT command registers
    """
    #Fields in this frame (payload)
    #dataFrame type = 0x08
    #Frame ID (byte) ID to be used in subsequent ACK. 0 ==> no ACK sent.
    #AT command  two ASCII characters that identify the AT command.
    #Parameter value  (optional)  value to set reqister (absent ==> query)

    def __init__(self, cmd_str, *args, **kwargs):
        """
        Create a frame.

        params:
        @param cmd_str: The AT command (ASCII)
        @type cmd_str: bytearray, length 2
        @keyword value: New value for the register identified by cmd_str
        @type value: bytearray, MSB first
        """
        payload = str(cmd_str)
        self.new_val = b''
        try:
            self.new_val = str(kwargs['value'])
            del kwargs['value']
        except KeyError:
            pass
        payload += self.new_val
        super(APIFrameATCmd, self).__init__(payload, *args, **kwargs)


def frame_listener(a_frame):
    assert isinstance(a_frame, APIFrame)
    print("got frame")


if __name__ == "__main__":
    atid = APIFrameATCmd(b'ID')
    stream = APIFrameStream('/dev/ttyUSB0', listeners=[frame_listener])
    stream.send(atid)
