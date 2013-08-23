'''
Created on Jun 23, 2012

@author: A. Lloyd Flanagan

A simple (?) user interface to serve some of the functions of the XTCU program
but in a platform-independent way.
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
from ui.gtk3.SettingsNotebook import BasicSettingContents, Network1SettingContents, Network2SettingContents
from hardware.xbee.Settings import ReadException


class PyxbMainWin(object):

    TIMEOUT=2  #seconds
    "Timeout for serial reads"
    
    def __init__(self, baud_rate, *args, **kwargs):
        self.selected_port = ''
        self.baud_rate = baud_rate
        self.builder = Gtk.Builder()
        my_dir = os.path.dirname(__file__)
        self.builder.add_from_file(os.path.join(my_dir, "PyxbMainWin.glade"))

        self.win = self.builder.get_object("PyxbMainWin")
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
        self.stg_notebook = self.builder.get_object("settings_notebook")
        self.page1_child.set_property("row-homogeneous", False)

        self.page2_child = Gtk.Grid(orientation=Gtk.Orientation.VERTICAL)
        page2_pos = self.stg_notebook.append_page(self.page2_child,
                                                  Gtk.Label("Network1"))
        assert page2_pos == 1
        self.page2_child.set_property("row-homogeneous", False)

        self.page3_child = Gtk.Grid(orientation=Gtk.Orientation.VERTICAL)
        page3_pos = self.stg_notebook.append_page(self.page3_child,
                                                  Gtk.Label("Network2"))
        assert page3_pos == 2
        self.page3_child.set_property("row-homogeneous", False)

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
            "onSelectDevice": self.setup_notebook_pages,
        }
        self.builder.connect_signals(handlers)
        
        self.populate_devices()
        isinstance(self.text_view, Gtk.TextView)
        buff = self.text_view.get_buffer()
        buff.insert_at_cursor("{}.{}.{}".format(Gtk.get_major_version(), Gtk.get_minor_version(), Gtk.get_micro_version()))
        
        self.win.show_all()

    def populate_devices(self, event=None):
        "Populates device list. May be called as event handler."
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
                if not self.chkSerial.get_active() and not 'USB' in p[0]:
                    continue
                if not self.chkUSB.get_active() and 'USB' in p[0]:
                    continue
                if p[2] == 'n/a':
                    self.ports_list.append((p[0],))
                else:
                    self.ports_list.append((p[0] + ": " + p[2],))
            except SerialException:
                #Serial() tried to configure port, and failed; probably doesn't
                #actually exist on the machine. Debian linuxes appear to create files for
                #ports that don't exist -- not sure why.
                pass

    def setup_notebook_pages(self, tree_view, *args):
        isinstance(tree_view, Gtk.TreeView)
        try:
            selection = Gtk.TreeView.get_selection(tree_view)
        except TypeError:
            #no selection found
            return
        isinstance(selection, Gtk.TreeSelection)
        #boy are the docs for this function wrong:
        model, treeiter = selection.get_selected()
        if not treeiter:
            #this method may be invoked when there is no selection
            self.selected_port = None
            for child in self.page1_child.get_children():
                self.page1_child.remove(child)
            for child in self.page2_child.get_children():
                self.page2_child.remove(child)
            for child in self.page3_child.get_children():
                self.page3_child.remove(child)
        else:
            #treeiter is an object but is accepted as index to model, returns a TreeModelRow
            if model[treeiter][0] != self.selected_port:
                self.selected_port = model[treeiter][0]
                if ':' in self.selected_port:
                    self.selected_port = self.selected_port[:self.selected_port.find(':')]
    
                def ui_work(self):
                    """
                    Local procedure to actually do the work of updating the user interface.
                    We make this a procedure and use GObject.idle_add() to allow the window to
                    set the cursor to a "watch" while the work is done.
                    """
                    try:
                        for child in self.page1_child.get_children():
                            self.page1_child.remove(child)
                        self.p1_panel = BasicSettingContents(self.selected_port,
                                                             self.page1_child,
                                                             self.baud_rate
                                                             )
                        for child in self.page2_child.get_children():
                            self.page2_child.remove(child)
                        self.p2_panel = Network1SettingContents(self.selected_port,
                                                                self.page2_child,
                                                                self.baud_rate)
                        for child in self.page3_child.get_children():
                            self.page3_child.remove(child)
                        self.p3_panel = Network2SettingContents(self.selected_port,
                                                                self.page3_child,
                                                                self.baud_rate)
                    except (SerialException, ReadException) as err:
                        buff = self.text_view.get_buffer()
                        buff.insert_at_cursor("{}: {}\n".format(self.selected_port,
                                                                str(err)))
                    finally:
                        self.win.show_all()
                        self.win.get_window().set_cursor(None)
    
            top_gdk_window = self.win.get_window()
            watch = Gdk.Cursor(Gdk.CursorType.WATCH)
            top_gdk_window.set_cursor(watch)

            GObject.idle_add(ui_work, self)


if __name__ == '__main__':
    win = PyxbMainWin(115200)
    Gtk.main()
