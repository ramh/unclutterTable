import wx
from TableInfo import *

class DetailsPanel(wx.Panel):
    """ class MyPanel creates a panel to draw on, inherits wx.Panel """
    def __init__(self, parent, id, pos):
        # create a panel
        self.tableinfo = parent.tableinfo
        wx.Panel.__init__(self, parent, id, size=(800, 200), pos=pos)
        self.SetBackgroundColour("white")
        self.Bind(wx.EVT_PAINT, self.OnPaint)

    def OnPaint(self, evt):
        """set up the device context (DC) for painting"""
        self.dc = wx.PaintDC(self)
        self.dc.BeginDrawing()
        self.dc.DrawText("TABLE STATE", 150, 0)
        self.dc.DrawText("___________", 150, 5)
        self.dc.DrawText("Num Objects: %s" % self.tableinfo.numobjects, 150, 30)
        if True:
            b = self.tableinfo.get_current_belief(self.tableinfo.get_visible_objects())
            for j in range(len(b))[::6]:
                cur_b = b[j:j+6]
                self.dc.DrawText("Belief: [ " + ", ".join([ "Obj %d %1.3f" % (i+j, b_i) for i, b_i in enumerate(cur_b)]) + " ]", 100, 60 + j * 3)

        self.dc.EndDrawing()


