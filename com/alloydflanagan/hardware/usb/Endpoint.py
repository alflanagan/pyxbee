# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals

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
Created on Mar 6, 2012

@author: A. Lloyd Flanagan
"""
from com.alloydflanagan.hardware.errors import InvalidArgumentType
import usb

class USBEndpoint(object):
    """
    A USB endpoint descriptor.
    """

    def __init__(self, endp):
        """
        Creates a wrapper for pyusb Endpoint object.
        
        """
        if endp.bDescriptorType != 5:
            raise InvalidArgumentType('Was expecting descriptor type 5, got {}'.format(endp.bDescriptorType))
        self.endp = endp

    def __getattr__(self, x):
        try:
            return getattr(self.endp, x)
        except AttributeError:
            raise AttributeError("'{}' object has no attribute '{}'".format(self.__class__.__name__, x))

#Bits 0..3b Endpoint Number.
#Bits 4..6b Reserved. Set to Zero
#Bits 7 Direction 0 = Out, 1 = In (Ignored for Control Endpoints)
        #TODO: define a class for accessing bitmaps. damn.
#    00 = Control
#    01 = Isochronous
#    10 = Bulk
#    11 = Interrupt
#
#Bits 2..7 are reserved. If Isochronous endpoint,
#Bits 3..2 = Synchronisation Type (Iso Mode)
#
#    00 = No Synchonisation
#    01 = Asynchronous
#    10 = Adaptive
#    11 = Synchronous
#
#Bits 5..4 = Usage Type (Iso Mode)
#
#    00 = Data Endpoint
#    01 = Feedback Endpoint
#    10 = Explicit Feedback Data Endpoint
#    11 = Reserved

    def dump(self):
        val = '\nEndpoint: {}, attribs: {}, interval: {}'.format(
                            self.bEndpointAddress, self.bmAttributes, self.bInterval)
        return val

    def __unicode__(self):
        return "Endpoint: {}, attribs: {}".format(self.bEndpointAddress, self.bmAttributes)

    def get_ui(self):
        """Return a dictionary whose keys are UI elements, and values are string representations
        of the matching object attributes. This allows controller to populate a view automatically.
        (work in progress)
        """
        pass

