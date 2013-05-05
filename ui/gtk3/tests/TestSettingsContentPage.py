'''
Created on Jul 1, 2012

@author: lloyd
'''
from gi.repository import Gtk #@UnresolvedImport
from com.alloydflanagan.pyxb.ui.gtk3.SettingsNotebook import BasicSettingContents


class TestSettingsContentPageGlade(object):

    def __init__(self):
        #Gtk.Window.__init__(self, title="TestSettingsContentPage")
        self.builder = Gtk.Builder()
        self.builder.add_from_file("TestSettingsContents.glade")  

        self.win = self.builder.get_object("window1")
        self.grid = self.builder.get_object("test_setting_grid")
        #grid = Gtk.Grid(orientation=Gtk.Orientation.VERTICAL)
        #self.add(grid)
        self.win.connect("delete-event", Gtk.main_quit)
        self.win.show_all()
        try:
            content_page = BasicSettingContents('/dev/ttyS0', self.grid)
        except Exception as e:
            print(e)
        self.win.show_all()

        #grid.add(content_page)


win = TestSettingsContentPageGlade()

Gtk.main()
