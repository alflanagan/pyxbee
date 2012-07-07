'''
Created on Jun 23, 2012

@author: lloyd
'''

from gi.repository import Gtk #@UnresolvedImport #uses a dynamic importer.
#problem with dynamic importer is that aptana can't get completion info. hmmm...
from serial.tools import list_ports
from serial.serialutil import SerialException
from com.alloydflanagan.pyxb.ui.gtk3.SettingsNotebook import BasicSettingContents

class PyxbMainWin(object):

    def __init__(self, *args, **kwargs):
        self.selected_port = ''
        self.builder = Gtk.Builder()
        self.builder.add_from_file("PyxbMainWin.glade")  

        self.win = self.builder.get_object("PyxbMainWin")
        self.close_btn = self.builder.get_object("btnClose")
        self.ports_list = self.builder.get_object("liststore1")
        self.ports_view = self.builder.get_object("dev_list_tview")
        self.page1_child= self.builder.get_object("stg_pg1_child")
        self.text_view = self.builder.get_object("textview1")
        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn(None, renderer, text=0)
        column.set_widget(None) #no header
        self.ports_view.append_column(column)

        self.stg_notebook = self.builder.get_object("settings_notebook")

        self.win.connect("delete-event", Gtk.main_quit)
        self.close_btn.connect("clicked", self.close_btn_clicked)

        select = self.ports_view.get_selection()
        select.connect("changed", self.setup_notebook_pages)


        self.populate_devices()
        self.win.show_all()
        
    def populate_devices(self):
        self.ports = list_ports.comports()
        self.ports.sort()
        for p in self.ports:
            self.ports_list.append((p[0], ))

    def setup_notebook_pages(self, tree_selection):
        model, treeiter = tree_selection.get_selected()
        if model[treeiter][0] != self.selected_port:
            self.selected_port = model[treeiter][0]
            if treeiter != None:
                print ("You selected", self.selected_port)
                for child in self.page1_child.get_children():
                    self.page1_child.remove(child)
                try:
                    self.p1_panel = BasicSettingContents(self.selected_port, self.page1_child)
                except SerialException as err:
                    buff = self.text_view.get_buffer()
                    buff.insert_at_cursor("{}: {}\n".format(self.selected_port, str(err) ))
                #self.stg_notebook.set_current_page(0)
            self.win.show_all()
    
    def close_btn_clicked(self, event):
        Gtk.main_quit()


if __name__ == '__main__':
    win = PyxbMainWin()
    Gtk.main()