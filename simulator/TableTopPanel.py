import wx
from TableInfo import *

class TableTopPanel(wx.Panel):
    """ class MyPanel creates a panel to draw on, inherits wx.Panel """
    def __init__(self, parent, id, pos):
        # create a panel
        self.tableinfo = parent.tableinfo
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
        self.tableinfo.sortonZ()

        # First Draw Removed Objects (assumption is they are not going to be stacked)
        for i in range(0, self.tableinfo.rem_numobjects):
            self.dc.SetBrush(wx.Brush(self.tableinfo.rem_colors[i], wx.SOLID))
            objectX = tableX + self.tableinfo.rem_positions[i][0]
            objectY = tableY + tableWidth - self.tableinfo.rem_positions[i][1] - self.tableinfo.rem_dimensions[i][1]
            self.dc.DrawRectangle(objectX, objectY, self.tableinfo.rem_dimensions[i][0], self.tableinfo.rem_dimensions[i][1])

        # Draw Table Objects
        for i in range(0, self.tableinfo.numobjects):
            self.dc.SetBrush(wx.Brush(self.tableinfo.colors[i], wx.SOLID))
            objectX = tableX + self.tableinfo.positions[i][0]
            objectY = tableY + tableWidth - self.tableinfo.positions[i][1] - self.tableinfo.dimensions[i][1]
            self.dc.DrawRectangle(objectX, objectY, self.tableinfo.dimensions[i][0], self.tableinfo.dimensions[i][1])

        self.dc.EndDrawing()

