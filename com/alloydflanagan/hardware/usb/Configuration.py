# -*- coding: utf-8 -*-
from __future__ import division, print_function
'''
Created on Mar 6, 2012

@author: lloyd
'''
from com.alloydflanagan.hardware.errors import InvalidArgumentType
from com.alloydflanagan.hardware.usb.Interface import USBInterface

class USBConfiguration(object):
    '''
    A USB configuration descriptor. "A USB device can have several different
    configurations although the majority of devices are simple and only have
    one. The configuration descriptor specifies how the device is powered, what
    the maximum power consumption is, the number of interfaces it has." See
    U{http://www.beyondlogic.org/usbnutshell/usb5.shtml}.
    '''


    def __init__(self, cfg):
        '''
        Create a USBConfiguration from usb.core.
        '''
        if cfg.bDescriptorType != 2:
            raise InvalidArgumentType('Expected descriptor type 2, got {}'.format(cfg.bDescriptorType))
        self._total_len = cfg.wTotalLength
        self._num_intfcs = cfg.bNumInterfaces
        self._value = cfg.bConfigurationValue
        self._attrs = cfg.bmAttributes
        self.interfaces = [USBInterface(n) for n in cfg]
#        0     bLength     1     Number     
#
#Size of Descriptor in Bytes
#1     bDescriptorType     1     Constant     
#
#Configuration Descriptor (0x02)
#2     wTotalLength     2     Number     
#
#Total length in bytes of data returned
#4     bNumInterfaces     1     Number     
#
#Number of Interfaces
#5     bConfigurationValue     1     Number     
#
#Value to use as an argument to select this configuration
#6     iConfiguration     1     Index     
#
#Index of String Descriptor describing this configuration
#7     bmAttributes     1     Bitmap     
#
#D7 Reserved, set to 1. (USB 1.0 Bus Powered)
#
#D6 Self Powered
#
#D5 Remote Wakeup
#
#D4..0 Reserved, set to 0.
#8     bMaxPower     1     mA     
#
#Maximum Power Consumption in 2mA units 
#        

    def __unicode__(self):
        return u'conf[{}]'.format(self._value)
    
    def dump(self):
        d = "config: #interfaces: {}".format(self._num_intfcs)
        for intfc in self.interfaces:
            d += "\n{}".format(intfc.dump())
        return d