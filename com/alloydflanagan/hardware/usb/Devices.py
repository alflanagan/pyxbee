# -*- coding: utf-8 -*-
from __future__ import division, print_function

'''
Created on Mar 18, 2012

@author: lloyd
'''
import usb.core
from com.alloydflanagan.hardware.usb.Device import USBDevice

class USBDevices(object):
    '''
    A container for a list of USBDevice objects, with the ability to fill itself by traversing the list of USB devices.
    
    '''


    def __init__(self, traverse=True):
        '''
        Create a USBDevices collection. When traverse is true, will traverse USB buses on the 
        machine and fill itself.
        '''
        self._devices = []
        if traverse:
            devices = usb.core.find(find_all=True)
            for x in devices:
                dev = USBDevice(x)
                self._devices.append(dev)
                
    def dump(self):
        for dev in self._devices:
            print(dev.dump())
    
    def __iter__(self):
        return self._devices.__iter__()
    
            
if __name__ == '__main__':
    d = USBDevices(True)
    d.dump()
    for f in d:
        print(unicode(f))
        print(f.as_compact_str())
    
