import wx
from TableInfo import *

class DetailsPanel(wx.Panel):
    """ class MyPanel creates a panel to draw on, inherits wx.Panel """
    def __init__(self, parent, id, pos):
        # create a panel
        self.tableinfo = parent.tableinfo
        self.parent = parent
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
            n = len(self.tableinfo.vis_ids)
            n2 = len(self.tableinfo.rem_vis_ids)
            cur_b = b
            ids = self.tableinfo.vis_ids + self.tableinfo.rem_vis_ids
            self.dc.DrawText("Belief: [ " + ", ".join([ "Obj %d %1.3f" % (ids[i], b_i) for i, b_i in enumerate(cur_b[0:n+n2])]) + " ]", 100, 60)
            self.dc.DrawText("Belief: [ " + ", ".join([ "Beh %d %1.3f" % (ids[i], b_i) for i, b_i in enumerate(cur_b[n+n2:-1])]) + " ]", 100, 60 + 18)
            self.dc.DrawText("Belief: [ " + ", ".join([ "Off %1.3f" % (b_i) for i, b_i in enumerate([cur_b[-1]])]) + " ]", 100, 60 + 2 * 18)

        self.dc.EndDrawing()


