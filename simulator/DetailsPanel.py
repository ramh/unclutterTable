import wx
from TableInfo import *

class DetailsPanel(wx.Panel):
    """ class MyPanel creates a panel to draw on, inherits wx.Panel """
    def __init__(self, parent, id, pos):
        # create a panel
        wx.Panel.__init__(self, parent, id, size=(400, 100), pos=pos)
        self.SetBackgroundColour("white")
        self.Bind(wx.EVT_PAINT, self.OnPaint)

    def OnPaint(self, evt):
        """set up the device context (DC) for painting"""
        self.dc = wx.PaintDC(self)
        self.dc.BeginDrawing()
        self.dc.DrawText("TABLE STATE", 150, 0)
        self.dc.DrawText("___________", 150, 5)
        self.dc.DrawText("Num Objects: %s" % tableinfo.numobjects, 150, 30)

        self.dc.EndDrawing()


