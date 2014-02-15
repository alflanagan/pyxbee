"""
Created on Aug 25, 2013

@author: A. Lloyd Flanagan

A module to allow the user to select a serial port from a list of serial ports.

Required UI elements: a GtkTreeView, GtkListStore, and two GtkCheckButtons (to 
toggle display of true serial and USB ports).

"""


from gi.repository import Gtk
from serial.tools import list_ports
from serial.serialutil import SerialException
import serial

from model.ports import PortsList


class GtkPortChooser(object):
    def __init__(self, ports_gtk_list_store, gtk_tree_view, serial_gtk_button, 
                 usb_gtk_button, port_selected_listener = []):
        """Creates port chooser and links to UI elements.
        
        The assumption is made that UI elements are defined externally, probably
        by a layout program such as Glade, and required objects are provided for
        this class to operate upon.
        
        Parameters
        ----------
        ports_gtk_list_store : Gtk.ListStore
            A `ListStore` used to hold data for the TreeView.
        gtk_tree_view : Gtk.TreeView
            A `TreeView` which displays a list of serial ports.
        serial_gtk_button : Gtk.ToggleButton
            A `ToggleButton` which causes display of serial (non-USB) ports
            when selected.
        usb_gtk_button : Gtk.ToggleButton
            A `ToggleButton` which causes display of USB (emulated) serial
            ports when selected.
        port_selected_listener : listener object or iterable of listeners, optional
            One or more objects whose `onPortSelected` method will be called when
            the user selects a specific port.
        """
        #TODO: implement friendlier checks than assert (should be ValueError)
        assert isinstance(ports_gtk_list_store, Gtk.TreeModel)
        assert isinstance(gtk_tree_view, Gtk.TreeView)
        assert isinstance(serial_gtk_button, Gtk.ToggleButton)
        assert isinstance(usb_gtk_button, Gtk.ToggleButton)
        self.store = ports_gtk_list_store
        self.tview = gtk_tree_view
        self.btnSerial = serial_gtk_button
        self.btnUSB = usb_gtk_button
        self.listeners = []
        try:
            for listener in port_selected_listener:
                assert hasattr(listener, "onPortSelected")
                self.listeners.append(listener) #make our own list to prevent mischief
        except TypeError:
            #OK, not iterable
            assert hasattr(port_selected_listener, "onPortSelected")
            self.listeners.append(port_selected_listener)
        self.lister = PortsList(self.store)
        self.show_usb = self.btnUSB.get_active()
        self.show_serial = self.btnSerial.get_active()
        
    def onSerialToggled(self, btn):
        self.show_serial = not self.show_serial
        self.lister.populate_devices(self.show_serial, self.show_usb)
    
    def onUSBToggled(self, btn):
        self.show_usb = not self.show_usb
        self.lister.populate_devices(self.show_serial, self.show_usb)
    
    def onPortChosen(self, tview_object):
        """Handler to be called when a new port is selected in TreeView."""
        the_port = self.selectedPort
        if the_port: #sometimes we get triggered when there is no port
            for listener in self.listeners:
                listener.onPortSelected(the_port)
        
    def updateList(self):
        #TODO: get serial and usb toggled state from treeview
        print("updating list")
        self.lister.populate_devices(True, True)
        
    @property
    def selectedPort(self):
        """
        The currently selected port (as a string, e.g. "/dev/ttyS1")
        or None if no port is selected.
        
        """
        try:
            selection = Gtk.TreeView.get_selection(self.tview)
        except TypeError:
            #no selection found
            return None
        if selection == None:
            return None
        isinstance(selection, Gtk.TreeSelection)
        #boy are the docs for this function wrong:
        model, treeiter = selection.get_selected()
        if not treeiter:
            #this method may be invoked when there is no selection
            return None
        else:
            #treeiter is an object but is accepted as index to model, returns a TreeModelRow
            selected_port = model[treeiter][0]
            if ':' in selected_port:
                selected_port = selected_port[:selected_port.find(':')]
            return selected_port
