# -*- coding: utf-8 -*-
from __future__ import division, print_function
'''
Created on Mar 5, 2012

@author: lloyd
'''
from com.alloydflanagan.hardware.errors import InvalidArgumentType
from collections import defaultdict
from com.alloydflanagan.hardware.usb.Configuration import USBConfiguration

class USBDevice(object):
    '''
    A device on the USB bus. Corresponds to a USB device descriptor.
    http://www.beyondlogic.org/usbnutshell/usb5.shtml
    
    '''
    std_device_class_codes = defaultdict(lambda: 'Unknown Class', 
                                         {0x00: 'Use class information in the Interface Descriptors',
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
                                          #01h      01h      Bluetooth Programming Interface.  Get specific information from www.bluetooth.com.
                                          #         02h      UWB Radio Control Interface.  Definition for this is found in the Wireless USB Specification in Chapter 8.
                                          #         03h      Remote NDIS.  Information can be found at: http://www.microsoft.com/windowsmobile/mobileoperators/default.mspx
                                          #         04h      Bluetooth AMP Controller. Get specific information from www.bluetooth.com.
                                          #02h      01h      Host Wire Adapter Control/Data interface.  Definition can be found in the Wireless USB Specification in Chapter 8.
                                          #         02h      Device Wire Adapter Control/Data interface.  Definition can be found in the Wireless USB Specification in Chapter 8.
                                          #         03h      Device Wire Adapter Isochronous interface.  Definition can be found in the Wireless USB Specification in Chapter 8.
             
                                          0xEF: 'Miscellaneous',
                                          0xFE: 'Application Specific',
                                          0xFF: 'Vendor Specific',
                                         }) 

    def __init__(self, dev):
        '''
        Creates a USBDevice object based on the device descriptor. A USBDevice has some information
        about the overall device, and a collection of L{USBDescriptors}.
        
        @param dev: U{usb.core.Device<http://pyusb.sourceforge.net/docs/1.0/tutorial.html>}
                    object returned by usb.core.find() 
        '''
        try:
            if dev.bDescriptorType != 1:
                raise InvalidArgumentType('Not a device descriptor (descriptor type %d, need 1).' % dev.bDescriptorType)     
        except AttributeError:
            raise InvalidArgumentType('Not a descriptor: expecting usb.core.Device.')
        
        self._spec = '%04x' % dev.bcdUSB
        self._usb_version = (int(self._spec[:2]), int(self._spec[2]), int(self._spec[3]))      
        self._dev_class = dev.bDeviceClass
        '''Class Code (Assigned by USB Org). if 0, each interface specifies its own code
           If 0xFF, the class code is vendor specified.'''
        self._sub_class = dev.bDeviceSubClass
        self._vendor = dev.idVendor
        self._product = dev.idProduct
        self.configs = [USBConfiguration(cfg) for cfg in dev]
            

    def __unicode__(self):
        return U'Device: version:{} class:{} ({}), subclass: {}, vendor: {}, product: {}'.format(self._usb_version, self._dev_class,
                                                                        USBDevice.std_device_class_codes[self._dev_class],
                                                                        self._sub_class, self._vendor, self._product)

    def as_compact_str(self):
        return U'%s: %s (%s -- %s)' % (USBDevice.std_device_class_codes[self._dev_class],
                                self._sub_class, self._vendor, self._product)
    def dump(self):
        val = U'Device: version:{} class:{} ({}), subclass: {}, vendor: {}, product: {}'.format(self._usb_version, self._dev_class,
                                                                        USBDevice.std_device_class_codes[self._dev_class],
                                                                        self._sub_class, self._vendor, self._product)
        for cfg in self._configs:
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