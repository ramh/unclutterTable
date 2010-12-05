import wx
from tableinfo import *

class TableFrontPanel(wx.Panel):
    """ class MyPanel creates a panel to draw on, inherits wx.Panel """
    def __init__(self, parent, id, pos):
        # create a panel
        wx.Panel.__init__(self, parent, id, size=(400,400), pos=pos)
        self.SetBackgroundColour("white")
        self.Bind(wx.EVT_PAINT, self.OnPaint)

    def OnPaint(self, evt):
        """set up the device context (DC) for painting"""
        self.dc = wx.PaintDC(self)
        self.dc.BeginDrawing()
        self.dc.DrawText("FRONT VIEW", 150, 0)
        self.dc.SetPen(wx.Pen(wx.Colour(133, 94, 66),style=wx.TRANSPARENT))
        self.dc.SetBrush(wx.Brush(wx.Colour(133, 94, 66), wx.SOLID))
        # set x, y, w, h for rectangle
        tableX = 50
        tableZ = 300
        self.dc.DrawRectangle(tableX, tableZ, 300, 20)
        self.dc.DrawRectangle(100, 320, 20, 80)
        self.dc.DrawRectangle(280, 320, 20, 80)

        # Sort on Y for front view
        tableinfo.sortonY()

        # Draw Table Objects
        for i in range(0, tableinfo.numobjects):
            self.dc.SetBrush(wx.Brush(tableinfo.colors[i], wx.SOLID))
            objectX = tableX + tableinfo.positions[i][0]
            objectZ = tableZ - tableinfo.positions[i][2] - tableinfo.dimensions[i][2]
            self.dc.DrawRectangle(objectX, objectZ, tableinfo.dimensions[i][0], tableinfo.dimensions[i][2])

        self.dc.EndDrawing()


