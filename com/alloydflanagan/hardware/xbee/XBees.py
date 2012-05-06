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


import usb.core
from com.alloydflanagan.hardware.usb.Device import USBDevice


class XBees(object):
    """
    Collection of all connected XBee radios
    """

    def __init__(self):
        """
        Search all usb ports to find XBees
        """
        dev = usb.core.find(find_all=True)
        for x in dev:
            print('--------------------------------------')
            dev = USBDevice(x)
            print(dev.dump())
