import wx
from tableinfo import *

class TableTopPanel(wx.Panel):
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
        self.dc.DrawText("TOP VIEW", 150, 0)
        self.dc.SetPen(wx.Pen(wx.Colour(133, 94, 66),style=wx.TRANSPARENT))
        self.dc.SetBrush(wx.Brush(wx.Colour(133, 94, 66), wx.SOLID))
        # set x, y, w, h for rectangle
        tableX = 50
        tableY = 50
        tableLength = 300
        tableWidth = 300
        self.dc.DrawRectangle(tableX, tableY, tableLength, tableWidth)

        # sort on Z for top view
        tableinfo.sortonZ()

        # Draw Table Objects
        for i in range(0, tableinfo.numobjects):
            self.dc.SetBrush(wx.Brush(tableinfo.colors[i], wx.SOLID))
            objectX = tableX + tableinfo.positions[i][0]
            objectY = tableY + tableWidth - tableinfo.positions[i][1] - tableinfo.dimensions[i][1]
            self.dc.DrawRectangle(objectX, objectY, tableinfo.dimensions[i][0], tableinfo.dimensions[i][1])

        self.dc.EndDrawing()

