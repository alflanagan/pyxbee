'''
Created on Aug 22, 2013

@author: A. Lloyd Flanagan

A simple (?) user interface to test communications with XBee radios.
'''
if __name__ == "__main__" and __package__ is None:
    #make relative imports work when run as main script, see PEP 366
    __package__ = ""

import os
import sys 
#we use fakegir to generate package info for editor autocomplete. If it's present in PATH, remove it
fakegir_path = os.path.join(os.path.expanduser('~'), '.cache', 'fakegir')
if fakegir_path in sys.path:
    #print("fakegir found; ignoring it")
    sys.path.remove(fakegir_path)
    
from gi.repository import Gtk, Gdk, GObject
from serial.tools import list_ports
from serial.serialutil import SerialException
import serial
#TODO: need a common top-level package name (and not pyxbee, it's sort-of taken)
from hardware.xbee.Settings import ReadException


class TestSendMainWin(object):

    TIMEOUT=2  #seconds
    "Timeout for serial reads"
    
    def __init__(self, baud_rate, *args, **kwargs):
        self.baud_rate = baud_rate
        self.builder = Gtk.Builder()
        my_dir = os.path.dirname(__file__)
        self.builder.add_from_file(os.path.join(my_dir, "TestSend.glade"))

        self.win = self.builder.get_object("TestSendMainWin")
        "top-level widget for whole window"
        self.close_btn = self.builder.get_object("btnClose")
        self.ports_list = self.builder.get_object("liststore1")
        "model for device list"
        self.ports_view = self.builder.get_object("dev_list_tview")
        "view for device list"
        
        self.chkSerial = self.builder.get_object("chkSerial")
        self.chkUSB = self.builder.get_object("chkUSB")
        isinstance(self.chkSerial, Gtk.CheckButton)
        isinstance(self.chkUSB, Gtk.CheckButton)
        #isinstance(self.ports_view, Gtk.TreeView) # hint for editor
        #self.ports_view
        #pprint(dir(self.ports_view))
        self.page1_child = self.builder.get_object("stg_pg1_child")
        isinstance(self.page1_child, Gtk.Grid)

        self.text_view = self.builder.get_object("textview1")
        "Text output box"
        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn(None, renderer, text=0)
        #the following is REQUIRED to display ports
        column.set_sizing(Gtk.TreeViewColumnSizing.FIXED)
        
        column.set_widget(None)  # no header
        self.ports_view.append_column(column)

        #make the standard close box for window work
        #for some reason bad things happen if we try do this with handlers dict below
        self.win.connect("delete-event", Gtk.main_quit)

        #connect action handlers to code objects
        handlers = {
            #close button
            "onCloseAction": Gtk.main_quit,
            #toggle checkbox on device listing
            "onDeviceCheckbox": self.populate_devices,
            #pick a specific device
            "onSelectDevice": self.onSelectDevice,
        }
        self.builder.connect_signals(handlers)
        
        self.populate_devices()
        isinstance(self.text_view, Gtk.TextView)
        buff = self.text_view.get_buffer()
        buff.insert_at_cursor("{}.{}.{}".format(Gtk.get_major_version(), Gtk.get_minor_version(), Gtk.get_micro_version()))
        
        self.win.show_all()
        
    def onSelectDevice(self, *args, **kwargs):
        print(*args)
        print(**kwargs)

    def populate_devices(self):
        ports = list_ports()


if __name__ == '__main__':
    win = TestSendMainWin(115200)
    Gtk.main()
