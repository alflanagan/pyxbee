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
    sys.path.remove(fakegir_path)
    
from gi.repository import Gtk, Gdk, GObject
from serial.tools import list_ports
from serial.serialutil import SerialException
import serial
#TODO: need a common top-level package name (and not pyxbee, it's sort-of taken)
from ui.gtk3.SettingsNotebook import BasicSettingContents, Network1SettingContents, Network2SettingContents
from hardware.xbee.Settings import ReadException


class PyxbMainWin(object):

    def __init__(self, *args, **kwargs):
        self.selected_port = ''
        self.builder = Gtk.Builder()
        my_dir = os.path.dirname(__file__)
        self.builder.add_from_file(os.path.join(my_dir, "PyxbMainWin.glade"))

        self.win = self.builder.get_object("PyxbMainWin")
        #top-level widget for whole window
        self.close_btn = self.builder.get_object("btnClose")
        self.ports_list = self.builder.get_object("liststore1")
        self.ports_view = self.builder.get_object("dev_list_tview")
        #isinstance(self.ports_view, Gtk.TreeView) # hint for editor
        #self.ports_view
        #pprint(dir(self.ports_view))
        self.page1_child = self.builder.get_object("stg_pg1_child")
        self.stg_notebook = self.builder.get_object("settings_notebook")
        self.page1_child.set_property("row-homogeneous", False)

        isinstance(self.page1_child, Gtk.Grid)
        self.page2_child = self.copy_widget(self.page1_child)
        assert isinstance(self.page2_child, Gtk.Grid)
        #self.page2_child = Gtk.Grid(orientation=Gtk.Orientation.VERTICAL)
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
        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn(None, renderer, text=0)
        #the following is REQUIRED to display ports
        column.set_sizing(Gtk.TreeViewColumnSizing.FIXED)
        column.set_widget(None)  # no header
        self.ports_view.append_column(column)

        self.win.connect("delete-event", Gtk.main_quit)
        #TODO: Bind to an action, which is bound to button
        self.close_btn.connect("clicked", self.close_btn_clicked)

        select = self.ports_view.get_selection()
        select.connect("changed", self.setup_notebook_pages)

        self.populate_devices()
        self.win.show_all()

    #TODO: speed up copying by implementing class-specific copy that copies known attributes
    def copy_widget(self, widget):
        """
        Returns a widget with same type and properties as other_widget.
        
        Turns out this isn't trivial in Gtk/GObject. Go figure.
        """
        #from stack overflow answer
        widget2=widget.__class__()
        print("cloning widget class {}".format(widget.__class__.__name__))
        for prop in [p for p in dir(widget) if p.startswith("set_") and p not in ("set_buffer", "set_parent")]:
            print("   property {}".format(prop))
            prop_value=None
            #attempt to get attribute value, complicated by not having consistent names
            try:
                prop_value=getattr(widget, prop.replace("set_","get_") )()
            except:
                try:
                    prop_value=getattr(widget, prop.replace("set_","") )
                except:
                    continue
            if prop_value == None:
                continue
            try:
                getattr(widget2, prop)( prop_value ) 
            except:
                pass
        return widget2        

    def populate_devices(self):
        try:
            self.ports = list_ports.comports()
            #print(self.ports)
        except TypeError as te:
            print(te)
        self.ports.sort()
        for p in self.ports:
            try:
                #s = serial.Serial(p[0])
                #s.open()
                #s.close()
                if p[2] == 'n/a':
                    self.ports_list.append((p[0],))
                else:
                    self.ports_list.append((p[0] + ": " + p[2],))
            except SerialException:
                pass  # don't exist, don't add it

    def setup_notebook_pages(self, tree_selection):
        model, treeiter = tree_selection.get_selected()
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
                                                         self.page1_child)
                    for child in self.page2_child.get_children():
                        self.page2_child.remove(child)
                    self.p2_panel = Network1SettingContents(self.selected_port,
                                                            self.page2_child)
                    for child in self.page3_child.get_children():
                        self.page3_child.remove(child)
                    self.p3_panel = Network2SettingContents(self.selected_port,
                                                            self.page3_child)
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

    def close_btn_clicked(self, event):
        Gtk.main_quit()


if __name__ == '__main__':
    win = PyxbMainWin()
    Gtk.main()
