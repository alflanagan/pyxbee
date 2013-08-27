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


class GtkPortChooser(object):
    def __init__(self, ports_gtk_list_store, gtk_tree_view, serial_gtk_button, usb_gtk_button, port_selected_listener = []):
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
        #TODO: implement friendlier checks than assert
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
        self.lister = PortsListerHelper(self.store)
        
    def onSerialToggled(self, btn):
        pass
    
    def onUSBToggled(self, byn):
        pass
    
    def onPortChosen(self, tview_object):
        """Handler to be called when a new port is selected in TreeView."""
        the_port = self.selectedPort
        for listener in self.listeners:
            listener.onPortSelected(the_port)
        
    def updateList(self):
        #TODO: get serial and usb toggled state from treeview
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
        
#TODO: better class name, move from UI-specific directory
class PortsListerHelper(object):
    TIMEOUT = 2
    """Timeout (in seconds) for attempting to connect to a serial port."""
    
    def __init__(self, gtk_list_store):
        """Create a list helper.
        
        Parameters
        ----------
        gtk_list_store : Gtk.TreeModel
            Model object which will contain the list of ports.
            
        """
        assert isinstance(gtk_list_store, Gtk.TreeModel)
        self.ports_list = gtk_list_store
    
    def populate_devices(self, list_serials, list_usbs):
        """Populates device list.
        
        Parameters
        ----------
        list_serials : Boolean
            If true, non-USB serial ports will be listed.
        list_usbs : Boolean
            If true, USB ports emulating serial ports will be listed.
            
        """
        try:
            self.ports = list_ports.comports()
            #print(self.ports)
        except TypeError as te:
            print(te)
        self.ports.sort()
        #isinstance(self.ports_list, Gtk.ListStore)
        self.ports_list.clear()
        for p in self.ports:
            try:
                s = serial.Serial(p[0], timeout=self.TIMEOUT)
                if ((list_usbs and 'USB' in p[0]) or list_serials):
                    if p[2] == 'n/a':
                        self.ports_list.append((p[0],))
                    else:
                        self.ports_list.append((p[0] + ": " + p[2],))
            except SerialException:
                #Serial() tried to configure port, and failed; probably doesn't
                #actually exist on the machine. Debian linuxes appear to create files for
                #ports that don't exist -- not sure why.
                pass
    