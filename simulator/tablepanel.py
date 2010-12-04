import wx
from tableinfo import *

class TablePanel(wx.Panel):
    """ class MyPanel creates a panel to draw on, inherits wx.Panel """
    def __init__(self, parent, id):
        # create a panel
        wx.Panel.__init__(self, parent, id, size=(400,400))
        self.CentreOnParent()
        self.SetBackgroundColour("white")
        self.Bind(wx.EVT_PAINT, self.OnPaint)

    def OnPaint(self, evt):
        """set up the device context (DC) for painting"""
        self.dc = wx.PaintDC(self)
        self.dc.BeginDrawing()
        self.dc.SetPen(wx.Pen(wx.Colour(133, 94, 66),style=wx.TRANSPARENT))
        self.dc.SetBrush(wx.Brush(wx.Colour(133, 94, 66), wx.SOLID))
        # set x, y, w, h for rectangle
        self.dc.DrawRectangle(0, 0, 400, 400)

        # Draw Table Objects
        tableinfo = TableInfo()
        for i in range(0, tableinfo.numobjects):
            self.dc.SetBrush(wx.Brush(tableinfo.colors[i], wx.SOLID))
            self.dc.DrawRectangle(tableinfo.positions[i][0], tableinfo.positions[i][1], tableinfo.dimensions[i][0], tableinfo.dimensions[i][1])

        self.dc.EndDrawing()

