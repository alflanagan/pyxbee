'''
Created on Jun 17, 2012

@author: lloyd
'''
import wx
from com.alloydflanagan.pyxb.ui.SettingsNotebook import SettingsNotebook


class ThisApp(wx.App):

    def OnInit(self):
        self.top_frame = wx.Frame(None, wx.ID_ANY, "")
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        lbl = wx.StaticText(self.top_frame, wx.ID_ANY, "Device Info")
        self.nb = SettingsNotebook(self.top_frame)
        self.sizer.Add(lbl)
        self.sizer.Add(self.nb, 1)
        self.top_frame.SetSizer(self.sizer)
        self.SetTopWindow(self.top_frame)
        return True

    def Show(self):
        self.top_frame.Show()


app = ThisApp(0)
app.Show()
app.MainLoop()
