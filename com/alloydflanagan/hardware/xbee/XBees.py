# -*- coding: utf-8 -*-
from __future__ import division, print_function
'''
Created on Mar 5, 2012

@author: lloyd
'''


import usb.core
import usb.util
from com.alloydflanagan.hardware.usb.Device import USBDevice

class XBees(object):
    '''
    Collection of all connected XBee radios
    '''


    def __init__(self):
        '''
        Search all usb ports to find XBees
        '''
        dev = usb.core.find(find_all=True)
        for x in dev:
            print('--------------------------------------')
            dev = USBDevice(x)
            print(dev.dump())
