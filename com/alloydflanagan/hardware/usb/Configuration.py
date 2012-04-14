# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals
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
        self.config = cfg
        self.interfaces = [USBInterface(n) for n in cfg]

    def __iter__(self):
        return self.interfaces.__iter__()

    def __getattr__(self, aname):
        """
        If we don't have an attribute, check for attribute on underlying
        L{usb.core.Configuration} object.
        """
        return getattr(self.config, aname)

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
        return 'conf[{}]'.format(self.config.bConfigurationValue)

    def dump(self):
        d = "config: #interfaces: {}".format(self.config.bNumInterfaces)
        for intfc in self:
            d += "\n{}".format(intfc.dump())
        return d

if __name__ == '__main__':
    from com.alloydflanagan.hardware.usb.Devices import USBDevices
    print('USBConfiguration tests started.')
    ds = USBDevices()
    print("Found {} devices.".format(len(ds)))
    for d in ds:
        for c in d:
            print('{}: {}'.format('bNumInterfaces', c.bNumInterfaces))
