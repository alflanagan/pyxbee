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
import argparse
import time
from xbee import ZigBee

#we use fakegir to generate package info for editor autocomplete. If it's present in PATH, remove it
fakegir_path = os.path.join(os.path.expanduser('~'), '.cache', 'fakegir')
if fakegir_path in sys.path:
    #print("fakegir found; ignoring it")
    sys.path.remove(fakegir_path)
    
import inspect
from gi.repository import Gtk, Gdk, GObject
from serial.tools import list_ports
from serial.serialutil import SerialException
import serial
#TODO: need a common top-level package name (and not pyxbee, it's sort-of taken)
from hardware.xbee.Settings import ReadException
from ports_chooser import GtkPortChooser
from tools.annotations import print_call
from threading import Thread


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
        self.ports_chooser = GtkPortChooser(self.ports_list, 
                                            self.ports_view, 
                                            self.chkSerial,
                                            self.chkUSB,
                                            self
                                           )

        self.ports_chooser.updateList()
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
            "onCloseAction": self.onCloseAction,
            "on_chkUSB_toggled": self.ports_chooser.onUSBToggled,
            "on_chkSerial_toggled": self.ports_chooser.onSerialToggled,
            "onSelectDevice": self.ports_chooser.onPortChosen,
            "b_entry_bkspc": self.b_entry_bkspc,
            "a_entry_bkspc": self.a_entry_bkspc,
            "b_entry_paste": self.b_entry_paste,
            "a_entry_paste": self.a_entry_paste,
            "b_key_press": self.b_key_press,
            "a_key_press": self.a_key_press,
            "on_btnClose_pressed": self.on_btnClose_press,
        }
        self.builder.connect_signals(handlers)
        
        #isinstance(self.text_view, Gtk.TextView)
        #buff = self.text_view.get_buffer()
        #buff.insert_at_cursor("{}.{}.{}".format(Gtk.get_major_version(), Gtk.get_minor_version(), Gtk.get_micro_version()))
        class RefreshTask(Thread):
            def __init__(self, main_win, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.parent_win = main_win
                assert isinstance(self.parent_win, TestSendMainWin)
            
            def run(self):
                while True:
                    time.sleep(3)
                    print("refreshing list", flush=True)
                    GObject.idle_add(self.parent_win.ports_chooser.updateList)
                    port = self.parent_win.ports_chooser.selectedPort
                    #if port:
                    
        self.refresh_task = RefreshTask(self)
        
        self.refresh_task.start()
        assert self.refresh_task.is_alive()
        self.win.show_all()
        
    def _set_device(self, device_name):
        # args to serial
        #         port = None,           # number of device, numbering starts at
        #                                # zero. if everything fails, the user
        #                                # can specify a device string, note
        #                                # that this isn't portable anymore
        #                                # port will be opened if one is specified
        #         baudrate=9600,         # baud rate
        #         bytesize=EIGHTBITS,    # number of data bits
        #         parity=PARITY_NONE,    # enable parity checking
        #         stopbits=STOPBITS_ONE, # number of stop bits
        #         timeout=None,          # set a timeout value, None to wait forever
        #         xonxoff=False,         # enable software flow control
        #         rtscts=False,          # enable RTS/CTS flow control
        #         writeTimeout=None,     # set a timeout for writes
        #         dsrdtr=False,          # None: use rtscts setting, dsrdtr
        #                                #override if True or False
        #         interCharTimeout=None  # Inter-character timeout, None to disable
        self.current_port = Serial(port=device_name, baudrate=self.baud_rate, timeout=self.TIMEOUT)
        self.xb = ZigBee(self.current_port, shorthand=True, escaped=False)
        assert self.xb

    def cancel_threads(self):
        self.refresh_task.join()
        
    def onChkUSB(self, button):
        self.ports_chooser.onUSBToggled(button)
        
    def onChkSerial(self, button):
        self.ports_chooser.onUSBToggled(button)
        
    def onPortSelected(self, port):
        print("selected {}".format(port))
        self.ports_chooser.updateList()

    def onCloseAction(self):
        Gtk.main_quit()

    def a_entry_bkspc(self, event):
        print("a_entry_bkspc(self, {})".format(str(event)))
        
    def b_entry_bkspc(self, event):
        print("b_entry_bkspc(self, {})".format(str(event)))
        
    def a_entry_paste(self, event):
        print("a_entry_paste(self, {})".format(str(event)))
        
    def b_entry_paste(self, event):
        print("b_entry_paste(self, {})".format(str(dir(event))))
        
    def a_key_press(self, text_view, event_key):
        print("a_key_press: {}".format(event_key.string))
        
    def b_key_press(self, text_view, event_key):
        #isinstance(event_key, Gdk.EventKey)
        print("b_key_press: {}".format(event_key.string))
        
    def on_btnClose_press(self, event):
        Gtk.main_quit()


if __name__ == '__main__':
    desc = """
    A small application to test communication between two XBee radio units.
    """
    DEFAULT_BAUD=38400
    a = argparse.ArgumentParser(description=desc)
    a.add_argument('--baud', '-b', type=int, dest="baud_rate", default=DEFAULT_BAUD,
                   help="""
                   The baud rate for serial i/o (default: %(default)s). This must match the setting
                   for the XBee radios. NOTE: all radios must have same rate setting.""")
    parsed = a.parse_args()
    win = TestSendMainWin(parsed.baud_rate)
    try:
        Gtk.main()
    finally:
        win.cancel_threads()
