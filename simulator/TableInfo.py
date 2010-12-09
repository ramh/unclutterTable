""" Configuration of the table state from FRONT VIEW """
import random
import sys
from qmdp.state_rep import TableObject
import numpy as np

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
        if configId == 1: # Simple vertical & horizontal stacking (just for testing the Panels' drawing)
            self.goalid = 1 # the yellow object
            self.numobjects = 3
            self.ids = range(0, self.numobjects)
            self.positions  = [ [110, 0, 0], [130, 60, 30], [120, 50, 0] ]
            self.dimensions = [ [40, 40, 40], [20, 20, 20], [40, 40, 30] ]
            self.colors = ["green", "yellow", "red"]
            self.full_occ_list = [ [], [], [] ]
            self.part_occ_list = [ [], [], [1] ]
            self.c_grasps = [0.7, 0.8, 0.2 ]  # current grasps
            self.f_grasps = [0.7, 0.8, 0.7 ]  # full grasps
            self.open_b = [ 0.3, 0.9, 0.2 ]  # belief probability that object is goal when the object is fully visible
            self.part_b = [ 0.3, 0.9, 0.3 ]  # belief probability that object is goal when the obejct is partially visible
            # self.focc_b = [ ]
            self.latticeids = range(1, self.numobjects+1)
        elif configId == 2: # Simple Vertical Stacking
            self.goalid = 0 # the yellow object on the left
            self.numobjects = 5
            self.ids = range(0, self.numobjects)
            self.positions  = [ [120, 20, 0], [115, 30, 20], [110, 10, 30], [190, 30, 0], [180, 10, 10] ]
            self.dimensions = [ [20, 20, 20], [30, 10, 10], [40, 40, 40], [30, 10, 10], [40, 40, 40] ]
            self.colors = ["yellow", "blue", "green", "yellow", "blue"]
            self.full_occ_list = [ [1, 2], [2], [], [4], [] ]
            self.part_occ_list = [ [1, 2], [2], [], [4], [] ]
            self.c_grasps = [ 0.9, 0.8, 0.7, 0.9, 0.8]
            self.f_grasps = [ 0.9, 0.8, 0.7, 0.9, 0.8]
            self.open_b = [ 0.95, 0.2, 0.1, 0.5, 0.1 ]
            self.part_b = [ 0.95, 0.2, 0.1, 0.5, 0.1 ]
            # self.focc_b = [ ]
            self.latticeids = range(1, self.numobjects+1)
        elif configId == 3: # Simple Horizontal Stacking (connected)
            self.goalid = 4
            self.numobjects = 5
            self.ids = range(0, self.numobjects)
            self.positions  = [ [120, 80, 0], [115, 50, 0], [110, 10, 0], [190, 50, 0], [180, 10, 0] ]
            self.dimensions = [ [20, 20, 20], [10, 30, 10], [40, 40, 40], [10, 30, 10], [40, 40, 40] ]
            self.colors = ["yellow", "blue", "green", "yellow", "blue"]
            self.full_occ_list = [ [], [], [], [], [] ]
            self.part_occ_list = [ [], [], [], [], [] ]
            self.c_grasps = [ 0.9, 0.9, 0.7, 0.9, 0.7]
            self.f_grasps = [ 0.9, 0.9, 0.7, 0.9, 0.7]
            self.open_b = [ ]
            self.part_b = [ ]
            # self.focc_b = [ ]
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
            self.full_occ_list = [ [2,3,4,5], [2,3,4,5], [],      [],    [],  [], [], [] ]
            self.part_occ_list = [ [2,3,4,5], [2,3,4,5], [3,4,5], [4,5], [5], [], [], [] ]
            self.c_grasps = [ 0.9, 0.9, 0.2, 0.2, 0.3, 0.9, 0.7, 0.7 ]
            self.f_grasps = [ 0.9, 0.9, 0.8, 0.7, 0.8, 0.9, 0.7, 0.7 ]
            self.latticeids = range(1, self.numobjects+1)
        elif configId == 5: # Complex vertical Stacking 2 (same as configId=4 with kind of just x,y inverted)
            self.goalid = 1
            self.numobjects = 8
            self.ids = range(0, self.numobjects)
            self.positions  = [ [120, 20, 0], [120, 50, 0], [120, 10, 20], [120, 30, 40], [130, 10, 70], [130, 40, 90],  # Stack 1
                                [230, 30, 0], [240, 50, 0] ]
            self.dimensions = [ [20, 20, 20], [20, 20, 20], [20, 70, 20], [30, 40, 30], [20, 70, 20], [20, 20, 20],  # Stack 2
                                [20, 20, 20], [20, 20, 30] ]
            self.colors = ["yellow", "blue", "green", "yellow", "gray", "black",
                           "black", "blue" ]
            self.full_occ_list = [ [2,3,4,5], [2,3,4,5], [],      [],    [],  [], [], [] ]
            self.part_occ_list = [ [2,3,4,5], [2,3,4,5], [3,4,5], [4,5], [5], [], [], [] ]
            self.c_grasps = [ 0.9, 0.9, 0.2, 0.2, 0.3, 0.9, 0.7, 0.7 ]
            self.f_grasps = [ 0.9, 0.9, 0.8, 0.7, 0.8, 0.9, 0.7, 0.7 ]
            self.latticeids = range(1, self.numobjects+1)
        elif configId == 6: # Little compicated Vertical & horizontal Stacking
            self.goalid = 2
            self.numobjects = 5
            self.ids = range(0, self.numobjects)
            self.positions  = [ [110, 0, 0], [130, 60, 30], [120, 50, 0], [190, 40, 0], [250, 40, 0] ]
            self.dimensions = [ [40, 40, 40], [20, 20, 20], [40, 40, 30], [50, 50, 50], [10, 10, 10] ]
            self.colors = ["green", "yellow", "black", "red", "gray"]
            self.full_occ_list = [ [], [], [], [], [] ]
            self.part_occ_list = [ [], [], [1], [], [] ]
            self.c_grasps = [0.7, 0.8, 0.2, 0.6, 0.9 ]
            self.f_grasps = [0.7, 0.8, 0.7, 0.6, 0.9 ]
            self.latticeids = range(1, self.numobjects+1)
        elif configId == 7: # Two objects - one of them is goal
            self.goalid = 0
            self.numobjects = 2
            self.ids = range(0, self.numobjects)
            self.positions  = [ [110, 10, 0], [190, 30, 0] ]
            self.dimensions = [ [40, 40, 40], [20, 20, 20] ]
            self.colors = ["red", "gray"]
            self.full_occ_list = [ [], [] ]
            self.part_occ_list = [ [], [] ]
            self.c_grasps = [0.7, 0.9 ]
            self.f_grasps = [0.7, 0.9 ]
            self.latticeids = range(1, self.numobjects+1)

    def get_goal_vol(self):
        goal_ind = self.ids.index(self.goalid)
        dims = self.dimensions[goal_ind]
        return dims[0] * dims[1] * dims[2]

    def get_occ_vol(self, ind):
        dims = self.dimensions[ind]
        pos = self.positions[ind]
        return dims[0] * dims[1] * (dims[2] + pos[2])

    def get_full_occ_bel(self, ind):
        CLUTTER_CONST = 0.5 / 1800000.
        occ_vol = self.get_occ_vol(ind)
        return CLUTTER_CONST * occ_vol * (1. - self.get_goal_vol() / occ_vol)

    def joint_belief(self, obj_bel):
        ret_b = [1.] * (len(obj_bel) + 1)
        tbl_b = 1.
        for i, b_i in enumerate(obj_bel):
                ret_b[i] *= b_i
                for j, b_j in enumerate(obj_bel):
                        if i == j:
                                continue
                        ret_b[i] *= 1. - b_j
                tbl_b *= 1. - b_i
        # for not on table
        print "ret_b bef", ret_b
        print "tbl_bel", tbl_b
        #ret_b = np.array(ret_b.tolist + [tbl_bel])
        ret_b[-1] = tbl_b
        print "ret_b aft", ret_b
        sum_arr = 0.
        for i, b_i in enumerate(ret_b):
            sum_arr += b_i
        out_b = [0.] * len(ret_b)
        for i, b_i in enumerate(ret_b):
            out_b[i] = b_i / sum_arr
        return out_b

    def get_current_belief(self, vis_objs):
        print "visible objs", ", ".join([vis_obj.__str__() for vis_obj in vis_objs])
        self.printConf()
        obj_bel = [0.] * (len(vis_objs) * 2)
        #obj_bel = np.zeros(len(vis_objs) * 2)
        for i, obj in enumerate(vis_objs):
            ind = self.latticeids.index(obj.obj_id)
            if len(obj.obstructors) == 0:
                # do fully open
                cur_bel = self.open_b[ind]
            else:
                # do partial
                cur_bel = self.part_b[ind]
            obj_bel[i] = cur_bel
            # do full occ
            full_occ_bel = self.get_full_occ_bel(ind)
            obj_bel[i * 2] = full_occ_bel
        print "obj_bel", obj_bel
        return self.joint_belief(obj_bel)

    def get_visible_objects(self):
        tbl_objs = []
        tbl_inds = []
        for i in range(self.numobjects):
            if len(self.full_occ_list[i]) != 0:
                continue
            new_tbl_obj = TableObject(self.latticeids[i], self.part_occ_list[i], False, False, self.c_grasps[i], self.f_grasps[i])
            tbl_objs.append(new_tbl_obj)
            tbl_inds.append(i)

        print tbl_inds
        for n_obj in tbl_objs:
            n_obsts = []
            for o_obst in n_obj.obstructors:
                print "latids", self.latticeids
                print "ob", o_obst
                print self.latticeids.index(o_obst)
                n_obsts.append(tbl_objs[tbl_inds.index(self.latticeids.index(o_obst))])
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
                    tmp = self.open_b[i]; self.open_b[i] = self.open_b[j]; self.open_b[j] = tmp
                    tmp = self.part_b[i]; self.part_b[i] = self.part_b[j]; self.part_b[j] = tmp
                    # tmp = self.focc_b[i]; self.focc_b[i] = self.focc_b[j]; self.focc_b[j] = tmp

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
                    tmp = self.open_b[i]; self.open_b[i] = self.open_b[j]; self.open_b[j] = tmp
                    tmp = self.part_b[i]; self.part_b[i] = self.part_b[j]; self.part_b[j] = tmp
                    # tmp = self.focc_b[i]; self.focc_b[i] = self.focc_b[j]; self.focc_b[j] = tmp

    def printConf(self):
        print "Numobjects : %s" % self.numobjects
        print "Ids : %s" % self.ids
        print "Positions : %s" % self.positions
        print "Dimensions : %s" % self.dimensions
        print "Colors: %s" % self.colors
        print "Lattice Ids %s" % self.latticeids

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
