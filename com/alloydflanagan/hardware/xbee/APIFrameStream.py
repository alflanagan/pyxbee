# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals
#com.alloydflanagan.hardware.xbee.APIFrameStream
"""
Created on Apr 28, 2012

@author: A. Lloyd Flanagan

"""

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
import serial
import io
import threading
from com.alloydflanagan.hardware.xbee.APIFrame import APIFrame
import sys
import os


class APIFrameStream(object):
    """
    Class to buffer and return API Frames from a stream object.

    parameters:
    @param serial_device: serial device to connect to ('/dev/ttyUSB0', 'COM1:'
                          , etc.)
    @type serial_device: string
    @keyword listeners: callbacks to be called when frame is read
    @type listeners: sequence of functions accepting L{APIFrame} argument

    additional arguments: Any accepted by serial.Serial()
    """

    def __init__(self, serial_device, *args, **kwargs):
        """
        Constructor
        """
        try:
            self.listeners = kwargs['listeners']
            """List of registered callbacks. Will be called with an APIFrame as
            parameter whenever a frame is completely received."""
            del kwargs['listeners']
        except KeyError:
            self.listeners = []
        self.conn = serial.Serial(serial_device, *args, **kwargs)
        self.conn.baudrate = 9600
        self.conn.bytesize = 8
        self.conn.parity = serial.PARITY_NONE
        self.conn.stopbits = 1
        self.conn.timeout = 5
        self.read_buff = io.BufferedReader(self.conn)
        self._reader_alive = True
        """Flag to signal child thread to terminate."""
        self._start_reader()
        self.write_buff = io.BufferedWriter(self.conn)

    def register_listener(self, listener):
        """Add a callback to the list of listeners. Param listener must be a
        callable that accepts one parameter, which will be a constructed
        APIFrame object."""
        self.listeners = self.listeners + listener

    def unregister_listener(self, listener):
        """Removes listener from registered list, so that it will no longer
        be called. Has no effect if listener is not a registered callback."""
        new_list = []
        for x in self.listeners:
            if not x is listener:
                new_list.append(x)
        self.listeners = tuple(new_list)

    def _start_reader(self):
        """Start reader thread"""
        self._reader_alive = True
        self.receiver_thread = threading.Thread(target=self.reader)
        self.receiver_thread.setDaemon(True)
        self.receiver_thread.start()

    def _stop_reader(self):
        """Stop reader thread only, wait for clean exit of thread"""
        self._reader_alive = False
        self.receiver_thread.join()

    def reader(self):
        """Procedure to run in child thread. Receives bytes from serial device,
        builds APIFrames, and calls registered callbacks when each frame is
        complete."""
        #read from read_buff until we've data for an entire frame
        #build frame, call registered listeners
        #io.BufferedReader *should* be handling synchronization of serial reads
        #for us
        current_frame = ''
        while self._reader_alive:
            b = self.read_buff.read(1)
            sys.stdout.write('.')
            #TODO: Really should be completing frame when complete length
            #is read, not when next frame starts. Will require this function
            #to know about length bytes, and check against current length of
            #current_frame
            if b == APIFrame.START_BYTE:
                if current_frame:
                    new_frame = APIFrame(current_frame)
                    #list() makes a local copy of list, so it doesn't change
                    #if we register/unregister a listener mid-loop
                    for x in list(self.listeners):
                        x(new_frame)
                    current_frame = ''
                    del new_frame
            else:
                current_frame += b

    def send(self, a_frame):
        self.write_buff.write(str(a_frame))
        self.write_buff.flush()

    def close(self):
        self._stop_reader()


if __name__ == "__main__":
    gotframe = False

    def test_listener(a_frame):
        print("got frame of {} bytes".format(len(a_frame)))
        global gotframe
        gotframe = True

    import time
    try:
        test1 = APIFrameStream('/dev/ttyUSB0', listeners=[test_listener])
        atid = APIFrame('ATID')
        test1.send(atid)
        time.sleep(1)
        test1.send(atid)
        while not gotframe:
            time.sleep(1)
    finally:
        test1.close()
