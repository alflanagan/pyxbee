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

'''
Created on Mar 6, 2012

@author: A. Lloyd Flanagan
'''
from com.alloydflanagan.hardware.errors import InvalidArgumentType
from com.alloydflanagan.hardware.usb.Endpoint import USBEndpoint
import usb

#can't inherit from usb.core.Interface, darn it. Essentially this is a proxy
#class that exposes attributes from Interface, and adds a few.
class USBInterface(object):
    '''
    USB Interface descriptor.
    
    Intended to support and extend the interface of pyusb's
    L{usb.core.Interface} object, even though we can't inherit from it.
    '''


    def __init__(self, intfc):
        self.intfc = intfc
        if self.intfc.bDescriptorType != 4:
            raise InvalidArgumentType('Was expecting descriptor type 4, got {}'.format(self.bDescriptorType))
        self.endpoints = [USBEndpoint(x) for x in intfc]
        #TODO: find the string descriptor and get a description of this interface

    def __getattr__(self, x):
        try:
            return getattr(self.intfc, x)
        except AttributeError:
            raise AttributeError("'{}' object has no attribute '{}'".format(self.__class__.__name__, x))

    def __iter__(self):
        return self.endpoints.__iter__()

    def dump(self):
        val = "Interface: #{}, class {}, subclass {}, protocol {}, #endpoints: {}".format(
            self.bInterfaceNumber, self.bInterfaceClass, self.bInterfaceSubClass,
            self.bInterfaceProtocol, self.bNumEndpoints)

        for e in self:
            val += e.dump()
        return val
#0     bLength     1     Number     
#
#Size of Descriptor in Bytes (9 Bytes)
#1     bDescriptorType     1     Constant     
#
#Interface Descriptor (0x04)
#2     bInterfaceNumber     1     Number     
#
#Number of Interface
#3     bAlternateSetting     1     Number     
#
#Value used to select alternative setting
#4     bNumEndpoints     1     Number     
#
#Number of Endpoints used for this interface
#5     bInterfaceClass     1     Class     
#
#Class Code (Assigned by USB Org)
#6     bInterfaceSubClass     1     SubClass     
#
#Subclass Code (Assigned by USB Org)
#7     bInterfaceProtocol     1     Protocol     
#
#Protocol Code (Assigned by USB Org)
#8     iInterface     1     Index     
#
#Index of String Descriptor Describing this interface

    def __unicode__(self):
        return u'intf[{}]: {}({})'.format(self.bInterfaceNumber, self.bInterfaceClass, self.bInterfaceSubClass)

if __name__ == '__main__':
    from com.alloydflanagan.hardware.usb.Devices import USBDevices
    devs = USBDevices(traverse=True)
    for d in devs:
        for c in d:
            for i in c:
                #verify that USBInterface objects expose attributes of Interface
                for attr in ['alternate_index', 'bAlternateSetting', 'bDescriptorType',
                             'bInterfaceClass', 'bInterfaceNumber', 'bInterfaceProtocol',
                             'bInterfaceSubClass', 'bLength', 'bNumEndpoints', 'configuration',
                             'iInterface', 'index']:
                    print("{}: {}".format(attr, getattr(i, attr)))
