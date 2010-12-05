import wx
import os

from tablefrontpanel import *
from tabletoppanel import *
from manipulator import *

class MainWindow(wx.Frame):
    def __init__(self, parent, title):
        self.dirname=''

        # A "-1" in the size parameter instructs wxWidgets to use the default size.
        # In this case, we select 200px width and the default height.
        wx.Frame.__init__(self, parent, title=title, size=(800,600))
        self.control = wx.TextCtrl(self, style=wx.TE_MULTILINE)
        self.CreateStatusBar() # A Statusbar in the bottom of the window

        # Setting up the menu.
        filemenu= wx.Menu()
        #menuOpen = filemenu.Append(wx.ID_OPEN, "&Open"," Open a file to edit")
        menuAbout= filemenu.Append(wx.ID_ABOUT, "&About"," Information about this simulator")
        menuExit = filemenu.Append(wx.ID_EXIT,"E&xit"," Terminate the simulator")

        # Creating the menubar.
        menuBar = wx.MenuBar()
        menuBar.Append(filemenu,"&File") # Adding the "filemenu" to the MenuBar
        self.SetMenuBar(menuBar)  # Adding the MenuBar to the Frame content.

        # Events.
        #self.Bind(wx.EVT_MENU, self.OnOpen, menuOpen)
        self.Bind(wx.EVT_MENU, self.OnExit, menuExit)
        self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)

        # Use some sizers to see layout options
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.control, 1, wx.EXPAND)

        # Table image
        self.drawTable()

        # Toolbox
        self.drawToolBox()

        #Layout sizers
        self.SetSizer(self.sizer)
        self.SetAutoLayout(1)
        #self.sizer.Fit(self)
        self.Show()

    def drawTable(self):
        TableFrontPanel(self, 1, pos=(0,100))
        TableTopPanel(self, 2, pos=(400, 100))

    def drawToolBox(self):
        self.buttons = []
        self.toolbox = wx.BoxSizer(wx.HORIZONTAL)
        for i in range(0, tableinfo.numobjects):
            buttonRemove = wx.Button(self, i, "Remove Object %d(%s)" % (i , tableinfo.colors[i]))
            self.Bind(wx.EVT_BUTTON, self.OnRemove, buttonRemove)
            self.buttons.append(buttonRemove)
            self.toolbox.Add(buttonRemove, 1, wx.EXPAND)
        self.sizer.Add(self.toolbox, 0, wx.EXPAND)

    # All Event Handling here
    def OnAbout(self,e):
        # Create a message dialog box
        credits = "\n\n\n\tRam Kumar Hariharan\n\tKaushik Subramanian\n\tKelsey Hawkins\n"
        dlg = wx.MessageDialog(self, " A simulator for table manipulation \n in wxPython %s" % credits, "Table manipulation 2D simulator", wx.OK)
        dlg.ShowModal() # Shows it
        dlg.Destroy() # finally destroy it when finished.

    def OnExit(self,e):
        self.Close(True)  # Close the frame.

    def OnOpen(self,e):
        """ Open a file"""
        dlg = wx.FileDialog(self, "Choose a file", self.dirname, "", "*.*", wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            self.filename = dlg.GetFilename()
            self.dirname = dlg.GetDirectory()
            f = open(os.path.join(self.dirname, self.filename), 'r')
            self.control.SetValue(f.read())
            f.close()
        dlg.Destroy()

    def OnRemove(self, e):
        objId = e.GetEventObject().GetId()
        index = tableinfo.ids.index(objId)
        Manipulator.removeObject(index)
        self.buttons[objId].Hide()
        self.drawTable()

app = wx.App(False)
frame = MainWindow(None, "Table 2D simulator - clutter table manipulation")
app.MainLoop()

