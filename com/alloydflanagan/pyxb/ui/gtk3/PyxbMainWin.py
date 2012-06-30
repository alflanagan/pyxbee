'''
Created on Jun 23, 2012

@author: lloyd
'''

from gi.repository import Gtk #@UnresolvedImport #uses a dynamic importer.
#problem with dynamic importer is that aptana can't get completion info. hmmm...
from serial.tools import list_ports
from com.alloydflanagan.pyxb.ui.SettingsNotebook import BasicSettingContents

class PyxbMainWin(object):

    def __init__(self, *args, **kwargs):
        self.builder = Gtk.Builder()
        self.builder.add_from_file("PyxbMainWin.glade")  

        self.win = self.builder.get_object("PyxbMainWin")
        self.close_btn = self.builder.get_object("btnClose")
        self.ports_list = self.builder.get_object("liststore1")
        self.ports_view = self.builder.get_object("dev_list_tview")
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
        page1_child= self.builder.get_object("stg_pg1_child")
        assert page1_child
        if treeiter != None:
            print ("You selected", model[treeiter][0])
            self.p1_panel = BasicSettingContents(model[treeiter][0], page1_child)
            self.stg_notebook.set_current_page(1)
    
    def close_btn_clicked(self, event):
        Gtk.main_quit()


if __name__ == '__main__':
    win = PyxbMainWin()
    Gtk.main()