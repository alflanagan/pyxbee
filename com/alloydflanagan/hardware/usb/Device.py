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
Created on Mar 5, 2012

@author: A. Lloyd Flanagan
"""
from com.alloydflanagan.hardware.errors import InvalidArgumentType
from collections import defaultdict
from com.alloydflanagan.hardware.usb.Configuration import USBConfiguration


#can we inherit from usb.core.Device? A: Nope. We can forward attribute
#accesses to the enclosed object, however.
class USBDevice(object):
    """
    A device on the USB bus. Corresponds to a USB device descriptor.
    http://www.beyondlogic.org/usbnutshell/usb5.shtml


    """

    std_device_class_codes = defaultdict(lambda: 'Unknown Class',
        {0x00: 'Unspecified', #stores class info in interface descriptors
         0x01: 'Audio',
         0x02: 'Communications and CDC Control',
         0x03: 'HID (Human Interface Device)',
         0x05: 'Physical',
         0x06: 'Image',
         0x07: 'Printer',
         0x08: 'Mass Storage',
         0x09: 'Hub',
         0x0A: 'CDC-Data',
         0x0B: 'Smart Card',
         0x0D: 'Content Security',
         0x0E: 'Video',
         0x0F: 'Personal Healthcare',
         0x10: 'Audio/Video Devices',
         0xDC: 'Diagnostic Device',
         0xE0: 'Wireless Controller',
         #subclass protocol Meaning
         #01h      01h      Bluetooth Programming Interface.  Get specific
         #                  information from www.bluetooth.com.
         #         02h      UWB Radio Control Interface.  Definition for this
         #                  is found in the Wireless USB Specification in
         #                  Chapter 8.
         #         03h      Remote NDIS.  Information can be found at:
         #http://www.microsoft.com/windowsmobile/mobileoperators/default.mspx
         #         04h      Bluetooth AMP Controller. Get specific information
         #                  from www.bluetooth.com.
         #02h      01h      Host Wire Adapter Control/Data interface.
         #                  Definition can be found in the Wireless USB
         #                  Specification in Chapter 8.
         #         02h      Device Wire Adapter Control/Data interface.
         #                  Definition can be found in the Wireless USB
         #                  Specification in Chapter 8.
         #         03h      Device Wire Adapter Isochronous interface.
         #                  Definition can be found in the Wireless USB
         #                  Specification in Chapter 8.

         0xEF: 'Miscellaneous',
         0xFE: 'Application Specific',
         0xFF: 'Vendor Specific',
         })

    def __init__(self, dev):
        """
        Creates a USBDevice object based on the device descriptor. A USBDevice
        has some information about the overall device, and a collection of
        L{USBDescriptors}.
        
        @param dev: U{usb.core.Device} object returned by usb.core.find()
                    <http://pyusb.sourceforge.net/docs/1.0/tutorial.html> 
        """
        try:
            if dev.bDescriptorType != 1:
                raise InvalidArgumentType(
                    'Not a device descriptor (descriptor type %d, need 1).'
                    % dev.bDescriptorType)
        except AttributeError:
            raise InvalidArgumentType(
                            'Not a descriptor: expecting usb.core.Device.')

        self.device = dev
        """
        The original L{usb.core.Device} object. 
        
        attributes: address bDescriptorType bDeviceClass bDeviceProtocol
        bDeviceSubClass bLength bMaxPacketSize0 bNumConfigurations bcdDevice
        bcdUSB bus default_timeout iManufacturer iProduct iSerialNumber
        idProduct idVendor
                    
        methods: attach_kernel_driver ctrl_transfer detach_kernel_driver
        get_active_configuration is_kernel_driver_active read reset
        set_configuration set_interface_altsetting write
                 
        """
        #print('got device {}'.format(dev))
        #print(dev.bcdUSB)
        #print('%04x' % dev.bcdUSB)
        #print(self.device)
        self.spec = '%04x' % dev.bcdUSB

        #print('bcdUSB {}, spec {}'.format(dev.bcdUSB, self.spec))
        self.usb_version = (int(self.spec[:2]),
                            int(self.spec[2]),
                            int(self.spec[3]))
        """USB Version as a tuple of ints (major, minor, really minor)."""
        #print(self.usb_version)
        self.version_string = '.'.join([str(i) for i in self.usb_version])
        """Convenient dotted representation of version (e.g. 2.0.0)"""
        #print('version_string: {}'.format(self.version_string))
        self.configs = []
        for cfg in self.device:
            self.configs.append(USBConfiguration(cfg))

    def __iter__(self):
        return self.configs.__iter__()

    def __getattr__(self, aname):
        """
        Exposes the attributes of the underlying L{usb.core.Device} object.
        Poor man's inheritance since we can't inherit from usb.core.Device.
        """
        #if we don't have an attribute, try the underlying device
        try:
            return getattr(self.device, aname)
        except AttributeError:
            #replace name of class in Device's error message.
            raise AttributeError("'{}' object has no attribute '{}'".format(
                                            self.__class__.__name__, aname))

    def __unicode__(self):
        fmt = (U'Device: version:{} class:{} ({}), subclass: {}, vendor: {}, '
               'product: {}')
        return fmt.format(
            self.usb_version, self.device.bDeviceClass,
            USBDevice.std_device_class_codes[self.device.bDeviceClass],
            self.device.bDeviceSubClass, self.device.idVendor,
            self.device.iProduct)

    def as_compact_str(self):
        return U'%s: %s (%s -- %s)' % (
            USBDevice.std_device_class_codes[self.device.bDeviceClass],
            self.device.bDeviceSubClass, self.device.idVendor,
            self.device.iProduct)

    def dump(self):
        fmt = (U'Device: version:{} class:{} ({}), subclass: {}, '
               U'vendor: {}, product: {}')
        val = fmt.format(
            self.usb_version, self.device.bDeviceClass,
            USBDevice.std_device_class_codes[self.device.bDeviceClass],
            self.device.bDeviceSubClass, self.device.idVendor,
            self.device.iProduct)
        for cfg in self.configs:
            val += '\n   config: {}'.format(cfg.dump())
        return val

#Subclass Code (Assigned by USB Org)
#6     bDeviceProtocol     1     Protocol     
#
#Protocol Code (Assigned by USB Org)
#7     bMaxPacketSize     1     Number     
#
#Maximum Packet Size for Zero Endpoint. Valid Sizes are 8, 16, 32, 64
#8     idVendor     2     ID     
#
#Vendor ID (Assigned by USB Org)
#10     idProduct     2     ID     
#
#Product ID (Assigned by Manufacturer)
#12     bcdDevice     2     BCD     
#
#Device Release Number
#14     iManufacturer     1     Index     
#
#Index of Manufacturer String Descriptor
#15     iProduct     1     Index     
#
#Index of Product String Descriptor
#16     iSerialNumber     1     Index     
#
#Index of Serial Number String Descriptor
#17     bNumConfigurations     1     Integer     
#
#Number of Possible Configurations

if __name__ == '__main__':
    from com.alloydflanagan.hardware.usb.Devices import USBDevices
    print('started.')
    ds = USBDevices()
    print("Found {} devices.".format(len(ds)))
    for d in ds:
        print('==========================================================')
        dev = d.device
        skip_types = ('method-wrapper', 'instancemethod',
                      'builtin_function_or_method', 'type',
                      '_ResourceManager')
        attrs = [a for a in dir(dev) if a not in
                 ('__dict__', '__doc__', '__module__')]
        attrs = [a for a in attrs if
               type(getattr(dev, a)).__name__  not in skip_types]
        for a in attrs:
            print('{}: {}'.format(a, getattr(d, a)))
