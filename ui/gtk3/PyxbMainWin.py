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
from ui.gtk3.ports_chooser import GtkPortChooser


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
        assert isinstance(self.close_btn, Gtk.Button)
        self.ports_list = self.builder.get_object("liststore1")
        "model for device list"
        assert isinstance(self.ports_list, Gtk.TreeModel)
        self.ports_view = self._init_ports_view()
        "view for device list"
        assert isinstance(self.ports_view, Gtk.TreeView)
        
        self.chkSerial = self.builder.get_object("chkSerial")
        assert isinstance(self.chkSerial, Gtk.ToggleButton)
        self.chkUSB = self.builder.get_object("chkUSB")
        assert isinstance(self.chkUSB, Gtk.ToggleButton)
        self.chooser = GtkPortChooser(self.ports_list, self.ports_view, 
                                      self.chkSerial, 
                                      self.chkUSB, 
                                      self)
        
        self.stg_notebook = self.builder.get_object("settings_notebook")
        assert isinstance(self.stg_notebook, Gtk.Notebook)
        self.page1_child = self.builder.get_object("stg_pg1_child")
        assert isinstance(self.page1_child, Gtk.Grid)

        self.page2_child = self._add_new_notebook_page("Network1")
        self.page3_child = self._add_new_notebook_page("Network2")

        self.text_view = self.builder.get_object("textview1")
        "Text output box"
        assert isinstance(self.text_view, Gtk.TextView)

        #make the standard close box for window work
        #for some reason bad things happen if we try do this with handlers dict below
        self.win.connect("delete-event", Gtk.main_quit)

        #connect action handlers to code objects
        handlers = {
            #close button
            "onCloseAction": Gtk.main_quit,
            #toggle checkbox on device listing
            "onSerialToggled": self.chooser.onSerialToggled,
            "onUSBToggled": self.chooser.onUSBToggled,
            #pick a specific device
            "onSelectDevice": self.chooser.onPortChosen,
        }
        self.builder.connect_signals(handlers)
        
        self.chooser.updateList()
        buff = self.text_view.get_buffer()
        buff.insert_at_cursor("{}.{}.{}".format(Gtk.get_major_version(), Gtk.get_minor_version(), Gtk.get_micro_version()))
        
        self.win.show_all()

    def _init_ports_view(self):
        """Sets up columns, etc. for Treeview to list ports.
        
        Returns
        -------
        Gtk.TreeView object with appropriate column, renderer, etc.
        
        """
        ports_view = self.builder.get_object("dev_list_tview")
        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn(None, renderer, text=0)
        #the following is REQUIRED to display ports
        column.set_sizing(Gtk.TreeViewColumnSizing.FIXED)
        
        column.set_widget(None)  # no header
        ports_view.append_column(column)
        return ports_view
        
        
    def _add_new_notebook_page(self, page_label):
        """Add an additional page to the settings notebook, with label `page_label`.
        
        Parameters
        ----------
        pae_label : string to set label for tab
        
        Returns
        -------
        Gtk.Widget which is first child of new page.
            
        """
        notebook_page = Gtk.Grid(orientation=Gtk.Orientation.VERTICAL)
        self.stg_notebook.append_page(notebook_page, Gtk.Label(page_label))
        notebook_page.set_property("row-homogeneous", False)
        return notebook_page
        
    def onPortSelected(self, port):
        self.setup_notebook_pages()
        
    def setup_notebook_pages(self):
        self.selected_port = self.chooser.selectedPort
        print("setup_notebook_pages(): selected port is " + self.selected_port)
        if not self.selected_port:
            for page in (self.page1_child, self.page2_child, self.page3_child):
                for child in page.get_children():
                    page.remove(child)
        else:
            def ui_work(self):
                """Local procedure to actually do the work of updating the user interface.
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
            #Not working??
            watch = Gdk.Cursor(Gdk.CursorType.WATCH)
            top_gdk_window.set_cursor(watch)

            GObject.idle_add(ui_work, self)


if __name__ == '__main__':
    win = PyxbMainWin(115200)
    Gtk.main()
