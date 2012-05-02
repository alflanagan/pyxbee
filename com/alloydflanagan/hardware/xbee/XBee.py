# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals
import threading
import time
from com.alloydflanagan.hardware.xbee.APIFrameStream import APIFrameStream

#Copyright 2012 A. Lloyd Flanagan
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

"""
Created on Mar 5, 2012

@author: A. Lloyd Flanagan
"""
import serial

#{"AT command":  ("Name and description", "Node type", (Parameter range),
#                 "writable", "Default"),

AT_CMDS = {"DH": ("""Destination Address High. Special values:
                     0x000000000000FFFF (broadcast) and 0x0000000000000000
                     (coordinator).
                  """, "CRE", (0, 0xFFFFFFFF), True, 0),
           "DL": ("""Destination Address Low. Special values:
                     0x000000000000FFFF (broadcast) and 0x0000000000000000
                     (coordinator).""", "CRE", (0, 0xFFFFFFFF), True, 0xFFFF),
           "MY": ("""16 - bit Network Address. 0xFFFE ==>
                     not in a network.""", "CRE", (0, 0xFFFE), False, 0xFFFE),
           "MP": ("""16 - bit Parent Network Address. 0xFFFE ==> no parent.
                  """, "E", (0, 0xFFFE), False, 0xFFFE),
           "NC": ("""Number of Remaining Children. Number of end devices
                     that can join the device. 0 ==> the device cannot allow
                     any more end devices to join.""", "CR", (0, None), False,
                     None),
           "SH": ("""Serial Number High. Reads the high 32 bits of the
                     module’s unique 64-bit address.""",
                     "CRE", (0, 0xFFFFFFFF), False, None),
           "SL": ("""Serial Number Low. Reads the low 32 bits of the
                      module’s unique 64-bit address.""",
                      "CRE", (0, 0xFFFFFFFF), False, None),
           "NI": ("""Node Identifier. String identifier, max length 20,
                     no commas.""",
                     "CRE", (None, None), True, " "),
           "SE": ("""Source Endpoint. Sets/reads the ZigBee application layer
                     source endpoint value. This value will be used as the
                     source endpoint for all data transmissions. SE is only
                     supported in AT firmware. The default value (0xE8) is
                     the Digi data endpoint.""",
                     "CRE", (0, 0xFF), True, 0xE8),
           "DE": ("""Destination Endpoint. Sets/reads ZigBee application layer
                     destination ID value. This value will be used as the
                     destination endpoint for all data transmissions. DE is
                     only supported in AT firmware. The default value (0xE8)
                     is the Digi data endpoint.""",
                  "CRE", (0, 0xFF), True, 0xE8),
           "CI": ("""Cluster Identifier. Sets/reads ZigBee application layer
                     cluster ID value. This value will be used as the cluster
                     ID for all data transmissions. CI is only supported in AT
                     firmware. The default value (0x11) is the transparent
                     data cluster ID.""", "CRE", (0, 0xFFFF), True, 0x11),
           "NP": ("""Maximum RF Payload Bytes. This value returns the maximum
                     number of RF payload bytes that can be sent in a unicast
                     transmission. If APS encryption is used (API transmit
                     option bit enabled), the maximum payload size is reduced
                     by 9 bytes. If source routing is used (AR < 0xFF), the
                     maximum payload size is reduced further.""",
                  "CRE", (0, 0xFFFF), False, None),
           "DD": ("""Device Type Identifier. Stores a device type value. This
                     value can be used to differentiate different XBee-based
                     devices. Digi reserves the range 0–0xFFFFFF.""",
                  "CRE", (None, None), False, None),
}
#For example, Digi currently uses the following DD values to identify various ZigBee products:
#
#0x30001 - ConnectPort X8 Gateway
#
#0x30002 - ConnectPort X4 Gateway
#
#0x30003 - ConnectPort X2 Gateway
#
#0x30005 - RS-232 Adapter
#
#0x30006 - RS-485 Adapter
#
#0x30007 - XBee Sensor Adapter
#
#0x30008 - Wall Router
#
#0x3000A - Digital I/O Adapter
#
#0x3000B - Analog I/O Adapter
#
#0x3000C - XStick
#
#0x3000F - Smart Plug
#
#0x30011 - XBee Large Display
#
#0x30012 - XBee Small Display


class XBee(object):
    """
    A single connected XBee radio
    """

    def __init__(self, device_name, *args, **kwargs):
        """
        Constructor

        @param args: Positional params which are forwarded to Serial.__init__()
        @param kwarg: Keyword params, also forwarded to Serial.__init__()
        """
        super(XBee, self).__init__(*args, **kwargs)
        self.ID = 0
        self.frame_stream = APIFrameStream(device_name, *args, **kwargs)
        self.get_ID()

    def activate_at_mode(self):
        if not self.conn.isOpen():
            self.conn.open()
        time.sleep(1)
        self.conn.write("+++")
        self.conn.flush()
        time.sleep(1)

    def send(self, data):
        if not self.conn.isOpen():
            self.conn.open()
        self.write_buff.write(data)
        self.write_buff.flush()

    def get_ID(self):
        if not self.ID:
            self.activate_at_mode()
            self.send_line("ATID")
            time.sleep(1)
            newID = self.read_buff.readline()
            cr_find = newID.find('\r')
            if cr_find:
                newID = newID[cr_find + 1:]
            if len(newID):
                self.ID = int(newID, 16)
        return self.ID
