# -*- coding: utf-8 -*-
from __future__ import division, print_function
'''
Created on Mar 6, 2012

@author: lloyd
'''
from com.alloydflanagan.hardware.errors import InvalidArgumentType
from com.alloydflanagan.hardware.usb.Endpoint import USBEndpoint

class USBInterface(object):
    '''
    USB Interface descriptor.
    '''


    def __init__(self, intf):
        '''
        Constructor
        '''
        if intf.bDescriptorType != 4:
            raise InvalidArgumentType('Was expecting descriptor type 4, got {}'.format(intf.bDescriptorType))
        self._num = intf.bInterfaceNumber
        self._alt_setting = intf.bAlternateSetting
        self._num_ends = intf.bNumEndpoints
        self._iclass = intf.bInterfaceClass
        self._isubclass = intf.bInterfaceSubClass
        self._protocol = intf.bInterfaceProtocol
        self._iintfc = intf.iInterface
        self._endpoints = [USBEndpoint(x) for x in intf]
        
    def dump(self):
        val = "Interface: #{}, class {}, subclass {}, protocol {}, #endpoints: {}".format(
                    self._num, self._iclass, self._isubclass, self._protocol, self._num_ends)
        for e in self._endpoints:
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