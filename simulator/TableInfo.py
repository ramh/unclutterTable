""" Configuration of the table state from FRONT VIEW """
import random
import sys
from qmdp.state_rep import TableObject

class TableInfo:
    def __init__(self, configId=0):
        self.configId = configId
        self.manualConf(configId)
        self.printConf()

#TODO: Attempt to do Random Configuration is not that easy (commented for now)
#    def randomConf(self):
#        maxobjects = 5
#        maxX = 300
#        maxY = 300
#        maxZ = 300
#        colorlist = ["green", "red", "yellow", "gray", "black"]
#
#        self.numobjects = random.randint(1, maxobjects-1)
#        self.ids = range(0, self.numobjects)
#        self.positions  = []
#        self.dimensions = []
#        self.colors = []
#        for i in range(0, self.numobjects):
#            # Random Position
#            rand_position = [random.randint(0, maxX), random.randint(0, maxY), random.randint(0, maxZ)]
#            self.positions.append(rand_position)
#            # Random Dimension
#            maxX_dimension = maxX - rand_position[0]
#            maxY_dimension = maxY - rand_position[1]
#            maxZ_dimension = maxZ - rand_position[2]
#            rand_dimension = [random.randint(0, maxX_dimension), random.randint(0, maxY_dimension), random.randint(0, maxZ_dimension)]
#            self.dimensions.append(rand_dimension)
#            # Random Colour
#            self.colors.append(colorlist[random.randint(0, len(colorlist)-1)])

    def manualConf(self, configId):
        self.goalid = 1
        if configId == 1: # Some random config to test views
            self.numobjects = 3
            self.ids = range(0, self.numobjects)
            self.positions  = [ [110, 0, 0], [130, 60, 30], [120, 50, 0] ]
            self.dimensions = [ [40, 40, 40], [20, 20, 20], [40, 40, 30] ]
            self.colors = ["green", "yellow", "red"]
            self.full_occ_list = [ [], [], [] ]
            self.part_occ_list = [ [], [], [1] ]
            self.c_grasps = [0.7, 0.8, 0.2 ]
            self.f_grasps = [0.7, 0.8, 0.7 ]
            self.
            self.latticeids = range(1, self.numobjects+1)
        elif configId == 2: # Simple Vertical Stacking
            self.goalid = 0
            self.numobjects = 5
            self.ids = range(0, self.numobjects)
            self.positions  = [ [120, 20, 0], [115, 30, 20], [110, 10, 30], [190, 30, 0], [180, 10, 10] ]
            self.dimensions = [ [20, 20, 20], [30, 10, 10], [40, 40, 40], [30, 10, 10], [40, 40, 40] ]
            self.colors = ["yellow", "blue", "green", "yellow", "blue"]
            self.full_occ_list = [ [1, 2], [2], [], [4], [] ]
            self.part_occ_list = [ [1, 2], [2], [], [4], [] ]
            self.c_grasps = [ 0.9, 0.8, 0.7, 0.9, 0.8]
            self.f_grasps = [ 0.9, 0.8, 0.7, 0.9, 0.8]
            self.latticeids = range(1, self.numobjects+1)
        elif configId == 3: # Simple Horizontal Stacking
            self.goalid = 4
            self.numobjects = 5
            self.ids = range(0, self.numobjects)
            self.positions  = [ [120, 80, 0], [115, 50, 0], [110, 10, 0], [190, 50, 0], [180, 10, 0] ]
            self.dimensions = [ [20, 20, 20], [10, 30, 10], [40, 40, 40], [10, 30, 10], [40, 40, 40] ]
            self.colors = ["yellow", "blue", "green", "yellow", "blue"]
            self.full_occ_list = [ [], [], [], [], [] ]
            self.part_occ_list = [ [], [], [], [], [] ]
            self.c_grasps = [ 0.9, 0.9, 0.7, 0.9, 0.7]
            self.f_grasps = [  0.9, 0.9, 0.7, 0.9, 0.7]
            self.latticeids = range(1, self.numobjects+1)
        elif configId == 4: # Complex Vertical Stacking
            self.goalid = 1
            self.numobjects = 8
            self.ids = range(0, self.numobjects)
            self.positions  = [ [120, 20, 0], [150, 20, 0], [110, 20, 20], [130, 20, 40], [110, 30, 70], [140, 20, 90],  # Stack 1
                                [200, 30, 0], [220, 40, 0] ]
            self.dimensions = [ [20, 20, 20], [20, 20, 20], [70, 20, 20], [40, 30, 30], [70, 20, 20], [20, 20, 20],  # Stack 2
                                [20, 20, 20], [20, 20, 30] ]
            self.colors = ["yellow", "blue", "green", "yellow", "gray", "black",
                           "black", "blue" ]
            self.full_occ_list = [ [], [], [], [], [], [], [], [] ]
            self.part_occ_list = [ [], [], [], [], [], [], [], [] ]
            self.c_grasps = [ 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0 ]
            self.f_grasps = [ 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0 ]
            self.latticeids = range(1, self.numobjects+1)

    def get_current_belief(self):
        

    def get_visible_objects(self):
        tbl_objs = []
        tbl_inds = []
        for i in range(self.numobjects):
            if len(self.full_occ_list[i]) != 0:
                continue
            new_tbl_obj = TableObject(self.latticeids[i], self.part_occ_list[i], False, False, self.c_grasps[i], self.f_grasps[i])

            tbl_objs.append(new_tbl_obj)
            tbl_inds.append(i)

        for n_obj in tbl_objs:
            n_obsts = []
            for o_obst in n_obj.obstructors:
                n_obsts.append(tbl_objs[tbl_inds.index(o_obst)])
            n_obj.obstructors = n_obsts
        return tbl_objs

    def sortonY(self):
        print "Sorting on Y"
        for i in range(0, self.numobjects-1):
            for j in range(i+1, self.numobjects):
                if(self.positions[i][1] < self.positions[j][1]):
                    tmp = self.positions[i]; self.positions[i] = self.positions[j]; self.positions[j] = tmp
                    tmp = self.dimensions[i]; self.dimensions[i] = self.dimensions[j]; self.dimensions[j] = tmp
                    tmp = self.colors[i]; self.colors[i] = self.colors[j]; self.colors[j] = tmp
                    tmp = self.ids[i]; self.ids[i] = self.ids[j]; self.ids[j] = tmp
                    tmp = self.full_occ_list[i]; self.full_occ_list[i] = self.full_occ_list[j]; self.full_occ_list[j] = tmp
                    tmp = self.part_occ_list[i]; self.part_occ_list[i] = self.part_occ_list[j]; self.part_occ_list[j] = tmp
                    tmp = self.c_grasps[i]; self.c_grasps[i] = self.c_grasps[j]; self.c_grasps[j] = tmp
                    tmp = self.f_grasps[i]; self.f_grasps[i] = self.f_grasps[j]; self.f_grasps[j] = tmp
                    tmp = self.latticeids[i]; self.latticeids[i] = self.latticeids[j]; self.latticeids[j] = tmp

    def sortonZ(self):
        print "Sorting on Z"
        for i in range(0, self.numobjects-1):
            for j in range(i+1, self.numobjects):
                if(self.positions[i][2] > self.positions[j][2]):
                    tmp = self.positions[i]; self.positions[i] = self.positions[j]; self.positions[j] = tmp
                    tmp = self.dimensions[i]; self.dimensions[i] = self.dimensions[j]; self.dimensions[j] = tmp
                    tmp = self.colors[i]; self.colors[i] = self.colors[j]; self.colors[j] = tmp
                    tmp = self.ids[i]; self.ids[i] = self.ids[j]; self.ids[j] = tmp
                    tmp = self.full_occ_list[i]; self.full_occ_list[i] = self.full_occ_list[j]; self.full_occ_list[j] = tmp
                    tmp = self.part_occ_list[i]; self.part_occ_list[i] = self.part_occ_list[j]; self.part_occ_list[j] = tmp
                    tmp = self.c_grasps[i]; self.c_grasps[i] = self.c_grasps[j]; self.c_grasps[j] = tmp
                    tmp = self.f_grasps[i]; self.f_grasps[i] = self.f_grasps[j]; self.f_grasps[j] = tmp
                    tmp = self.latticeids[i]; self.latticeids[i] = self.latticeids[j]; self.latticeids[j] = tmp

    def printConf(self):
        print "Numobjects : %s" % self.numobjects
        print "Ids : %s" % self.ids
        print "Positions : %s" % self.positions
        print "Dimensions : %s" % self.dimensions
        print "Colors: %s" % self.colors

    def printVisibleConf(self):
        visible_objects = self.get_visible_objects()
        if len(visible_objects) == 0:
            print "No Objects present"
        else:
            print "Objects are:"
            for config in visible_objects:
                print config

# Instantiate TableInfo
tableinfo = TableInfo(configId=int(sys.argv[1]))
#tableinfo = TableInfo()
