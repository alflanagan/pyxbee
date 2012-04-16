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
Created on Mar 18, 2012

@author: A. Lloyd Flanagan
"""
import usb.core
from com.alloydflanagan.hardware.usb.Device import USBDevice


class USBDevices(object):
    """
    A container for a list of USBDevice objects, with the ability to fill
    itself by traversing the list of USB devices.

    """

    def __init__(self, traverse=True):
        """
        Create a USBDevices collection. When traverse is true, will traverse
        USB buses on the machine and fill itself.
        """
        self._devices = []
        if traverse:
            #print('Devices()')
            devices = usb.core.find(find_all=True)
            #print('found {}'.format(len(devices)))
            for x in devices:
                dev = USBDevice(x)
                self._devices.append(dev)

    def __len__(self):
        return len(self._devices)

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
