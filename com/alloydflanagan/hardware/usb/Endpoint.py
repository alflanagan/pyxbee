# -*- coding: utf-8 -*-
from __future__ import division, print_function
'''
Created on Mar 6, 2012

@author: lloyd
'''
from com.alloydflanagan.hardware.errors import InvalidArgumentType
import usb

class USBEndpoint(object):
    '''
    A USB endpoint descriptor.
    '''


    def __init__(self, endp):
        '''
        Creates a wrapper for pyusb Endpoint object.
        
        '''
        if endp.bDescriptorType != 5:
            raise InvalidArgumentType('Was expecting descriptor type 5, got {}'.format(endp.bDescriptorType))
        self._endp_object = endp
        #'bLength', 'bRefresh', 'bSynchAddress', 'index', 'read', 'write'
        self._address = endp.bEndpointAddress
#Bits 0..3b Endpoint Number.
#Bits 4..6b Reserved. Set to Zero
#Bits 7 Direction 0 = Out, 1 = In (Ignored for Control Endpoints)
        self._synchaddr = endp.bSynchAddress
        #TODO: define a class for accessing bitmaps. damn.
        self._attrs = endp.bmAttributes
#    00 = Control
#    01 = Isochronous
#    10 = Bulk
#    11 = Interrupt
#
#Bits 2..7 are reserved. If Isochronous endpoint,
#Bits 3..2 = Synchronisation Type (Iso Mode)
#
#    00 = No Synchonisation
#    01 = Asynchronous
#    10 = Adaptive
#    11 = Synchronous
#
#Bits 5..4 = Usage Type (Iso Mode)
#
#    00 = Data Endpoint
#    01 = Feedback Endpoint
#    10 = Explicit Feedback Data Endpoint
#    11 = Reserved
        self._packet_size = endp.wMaxPacketSize
        '''Maximum Packet Size this endpoint is capable of sending or receiving'''
        self._interval = endp.bInterval
        '''Interval for polling endpoint data transfers. Value in frame counts. Ignored for Bulk & Control Endpoints.
           Isochronous must equal 1 and field may range from 1 to 255 for interrupt endpoints.'''
        
    def dump(self):
        val = '\nEndpoint: {}, attribs: {}, interval: {}'.format(self._address, self._attrs, self._interval)
        return val
    
    def __unicode__(self):
        return "Endpoint: {}, attribs: {}".format(self._address, self._attrs)
    
    def get_ui(self):
        '''Return a dictionary whose keys are UI elements, and values are string representations
        of the matching object attributes. This allows controller to populate a view automatically.
        (work in progress)
        '''
        pass
    