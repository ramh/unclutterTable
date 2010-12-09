import wx
import os

from TableFrontPanel import *
from TableTopPanel import *
from DetailsPanel import *
from qmdp.state_rep import *
from qmdp.qmdp import *

class MainWindow(wx.Frame):
    def __init__(self, parent, title):
        self.dirname=''
        wx.Frame.__init__(self, parent, title=title, size=(900,700))
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
        DetailsPanel(self, 3, pos=(0, 0))

    def drawToolBox(self):
        # Tools for POMDP
        self.buttons = []
        self.toolbox1 = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "POMDP Solve: Remove => ")
        self.toolbox1.Add(label)
        for i in range(0, tableinfo.numobjects):
            buttonRemove = wx.Button(self, i, "Obj %d(%s)" % (i , tableinfo.colors[i]))
            self.Bind(wx.EVT_BUTTON, self.OnRemove, buttonRemove)
            self.buttons.append(buttonRemove)
            self.toolbox1.Add(buttonRemove, 1, wx.EXPAND)
        # Tools for QMDP & InfoGain
        self.toolbox2 = wx.BoxSizer(wx.HORIZONTAL)
        label1 = wx.StaticText(self, -1, "QMDP Solve: ")
        self.toolbox2.Add(label1)
        buttonQMDP = wx.Button(self, -1, "Execute QMDP Step")
        self.Bind(wx.EVT_BUTTON, self.OnExecQMDP, buttonQMDP)
        self.toolbox2.Add(buttonQMDP, 1, wx.EXPAND)

        label2 = wx.StaticText(self, -1, "Information Gain Solve: ")
        self.toolbox2.Add(label2)
        buttonInfoGain = wx.Button(self, -1, "Execute InfoGain Step")
        self.Bind(wx.EVT_BUTTON, self.OnExecInfoGain, buttonInfoGain)
        self.toolbox2.Add(buttonInfoGain, 2, wx.EXPAND)
        # Add the tools
        self.sizer.Add(self.toolbox1, 0, wx.EXPAND)
        self.sizer.Add(self.toolbox2, 0, wx.EXPAND)

    # All Event Handling from here
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

    def OnExecQMDP(self, e):
        visible_objects = tableinfo.get_visible_objects()
        belief = tableinfo.get_current_belief(visible_objects)
        planner_type = 0 #QMDP
        print "EXECUTE PLANNING Input: ", belief, visible_objects, planner_type
        print ", ".join([vis_obj.__str__() for vis_obj in visible_objects])
        latticeInd = execute_planning_step(belief, visible_objects, planner_type)
        print "EXECUTE PLANNING Output: ", latticeInd

        # somehow got objId and probability
        title = "Result QMDP (doesnt work yet)"
        if latticeInd==0:
            content = "I am no longer going to search for the object"
        elif latticeInd<0:
            if -latticeInd in tableinfo.latticeids:
                index = tableinfo.latticeids.index(-latticeInd)
                content = "Goal Object found: %d" % (tableinfo.ids[index])
            elif -latticeInd in tableinfo.rem_latticeids:
                index = tableinfo.rem_latticeids.index(-latticeInd)
                content = "Goal Object found: %d" % (tableinfo.rem_ids[index])
            else:
                raise Exception("Lost track of index")

        else:
            # Chance of successful removal of object = Full Graspability probability
            index = tableinfo.latticeids.index(latticeInd)
            objId = tableinfo.ids[index]
            prob = tableinfo.f_grasps[index]
            rand = random.random()
            if rand < prob:
                content = "Removed Object: %d" % (objId)
                self.removeObject(index)
            else:
                content = "Failed to remove Object: %d since grasp prob is: %d" % (objId, prob*100)
        msg_box = wx.MessageDialog(self, content, title, wx.OK | wx.CENTRE | wx.ICON_EXCLAMATION)
        msg_box.ShowModal()   #Show the Dialog

    def OnExecInfoGain(self, e):
        title = "Result InfoGain"
        content = "(doesnt work yet)"
        msg_box = wx.MessageDialog(self, content, title, wx.OK | wx.CENTRE | wx.ICON_EXCLAMATION)
        msg_box.ShowModal()   #Show the Dialog

    def OnRemove(self, e):
        objId = e.GetEventObject().GetId()
        index = tableinfo.ids.index(objId)
        tableinfo.removeObject(index)
        self.buttons[objId].Hide()
        self.drawTable()

    def removeObject(self, index):
        objId = tableinfo.ids[index]
        tableinfo.removeObject(index)
        self.buttons[objId].Hide()
        self.drawTable()

app = wx.App(False)
frame = MainWindow(None, "Table 2D simulator - clutter table manipulation")
app.MainLoop()
