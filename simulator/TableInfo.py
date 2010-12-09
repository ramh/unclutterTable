""" Configuration of the table state from FRONT VIEW """
import random
import sys
import copy
from qmdp.state_rep import TableObject
from utils import half_gauss, part_gauss
import numpy as np

class TableInfo:
    def __init__(self, configId=0, goalInd=-1): # goalInd=-1 to not overwrite the goal index
        self.configId = configId
        self.manualConf(configId)
        # Overwrite the default goal index with what's passed
        if goalInd!= -1:
            self.goalid = goalInd
        self.goal_vol = self.get_goal_vol()
        self.printConf()
        self.init_rem_objs()

    def init_rem_objs(self):
        self.rem_numobjects = 0
        self.rem_ids = []
        self.rem_positions  = []
        self.rem_dimensions = []
        self.rem_colors = []
        self.rem_full_occ_list = []
        self.rem_part_occ_list = []
        self.rem_c_grasps = []
        self.rem_f_grasps = []
        self.rem_open_b = []
        self.rem_part_b = []
        self.rem_latticeids = []

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
        # Configs that can be used for QMDP are: 1, 2, 9
        # TODO: rest other than ones above
        if configId == 1: # Simple vertical & horizontal stacking (just for testing the Panels' drawing)
            self.goalid = 1 # the yellow object
            self.numobjects = 3
            self.ids = range(0, self.numobjects)
            self.positions  = [ [110, 0, 0], [130, 60, 30], [120, 50, 0] ]
            self.dimensions = [ [40, 40, 40], [20, 20, 20], [40, 40, 30] ]
            self.colors = ["green", "yellow", "red"]
            self.full_occ_list = [ [], [], [] ]
            self.part_occ_list = [ [], [], [1] ]
            self.c_grasps = [0.7, 0.8, 0.2 ] # current grasps
            self.f_grasps = [0.7, 0.8, 0.7 ] # full grasps
            self.open_b = [ 0.3, 0.9, 0.2 ]  # belief probability that object is goal when the object is fully visible
            self.part_b = [ 0.3, 0.9, 0.3 ]  # belief probability that object is goal when the obejct is partially visible
            # self.focc_b = [ ]
            self.latticeids = range(1, self.numobjects+1)
        elif configId == 2: # Simple Vertical Stacking
            # Complete for QMDP
            self.goalid = 0 # the yellow object on the left
            self.numobjects = 5
            self.ids = range(0, self.numobjects)
            self.positions  = [ [120, 20, 0], [115, 30, 20], [110, 10, 30], [190, 30, 0], [180, 10, 10] ]
            self.dimensions = [ [20, 20, 20], [30, 10, 10], [40, 40, 40], [30, 10, 10], [40, 40, 40] ]
            self.colors = ["yellow", "blue", "green", "yellow", "blue"]
            self.full_occ_list = [ [2], [2], [], [4], [] ]
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
            self.open_b = [ 0.8, 0.2, 0.1, 0.2, 0.1 ]
            self.part_b = [ 0.8, 0.2, 0.1, 0.2, 0.1 ]
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
            self.open_b = [ 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0 ]
            self.part_b = [ 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0 ]
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
            self.open_b = [ 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0 ]
            self.part_b = [ 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0 ]
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
        elif configId == 8: # Complex Vertical Stacking
            # Complete for QMDP
            self.goalid = 1
            self.numobjects = 9
            self.ids = range(0, self.numobjects)
            self.positions  = [ [110, 10, 0],  #obj before stack 1
                                [120, 50, 0], [150, 50, 0], [110, 50, 20], [130, 50, 40], [110, 60, 70], [140, 50, 90],  # Stack 1
                                [200, 30, 0], [220, 40, 0] ] # stack 2
            self.dimensions = [ [60, 30, 30],
                                [20, 20, 20], [20, 20, 20], [70, 20, 20], [40, 30, 30], [70, 20, 20], [20, 20, 20],
                                [20, 20, 20], [20, 20, 30] ]
            self.colors = [ "black",
                            "yellow", "blue", "green", "red", "gray", "black",
                            "black", "blue" ]
            # TODO: fix all below for the first object in the above list
            self.full_occ_list = [ [], [2,3,4,5], [2,3,4,5], [],      [],    [],  [], [], [] ]
            self.part_occ_list = [ [], [2,3,4,5], [2,3,4,5], [3,4,5], [4,5], [5], [], [], [] ]
            self.c_grasps = [ 0.6, 0.9, 0.9, 0.2, 0.2, 0.3, 0.9, 0.7, 0.7 ]
            self.f_grasps = [ 0.6, 0.9, 0.9, 0.8, 0.7, 0.8, 0.9, 0.7, 0.7 ]
            self.open_b = [ 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0 ]
            self.part_b = [ 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0 ]
            self.latticeids = range(1, self.numobjects+1)

    def set_vision(self, open_b, part_b):
        self.open_b = copy.copy(open_b)
        self.part_b = copy.copy(part_b)

    def get_goal_vol(self):
        goal_ind = self.ids.index(self.goalid)
        dims = self.dimensions[goal_ind]
        return float(dims[0]) * dims[1] * dims[2]

    def get_occ_vol(self, ind):
        dims = self.dimensions[ind]
        pos = self.positions[ind]
        return float(dims[0]) * dims[1] * (dims[2] + pos[2])

    def get_full_occ_bel(self, ind):
        CLUTTER_CONST = 1.0 / 180000.
        BUFFER = 5000.
        occ_vol = self.get_occ_vol(ind)
        print "occ_vol", ind, occ_vol
        print "goal_vol", ind, self.goal_vol
        return CLUTTER_CONST * occ_vol * max((1. - self.goal_vol / (occ_vol + BUFFER)), 0.)

    def joint_belief(self, obj_bel):
        ret_b = [1.] * (len(obj_bel) + 1)
        tbl_b = 1.
        # print "obj_bel", obj_bel
        for i, b_i in enumerate(obj_bel):
                ret_b[i] *= b_i
                for j, b_j in enumerate(obj_bel):
                        if i == j:
                                continue
                        ret_b[i] *= 1. - b_j
                tbl_b *= 1. - b_i
        # for not on table
        # print "ret_b bef", ret_b
        # print "tbl_bel", tbl_b
        #ret_b = np.array(ret_b.tolist + [tbl_bel])
        ret_b[-1] = tbl_b
        # print "ret_b aft", ret_b
        sum_arr = 0.
        for i, b_i in enumerate(ret_b):
            sum_arr += b_i
        out_b = [0.] * len(ret_b)
        for i, b_i in enumerate(ret_b):
            out_b[i] = b_i / sum_arr
        return out_b

    def get_current_belief(self, vis_objs):
        #print "visible objs", ", ".join([vis_obj.__str__() for vis_obj in vis_objs])
        #self.printConf()
        obj_bel = [0.] * (len(vis_objs) * 2)
        for i, obj in enumerate(vis_objs):
            if not obj.has_moved:
                ind = self.latticeids.index(obj.obj_id)
                if len(obj.obstructors) == 0:
                    # do fully open
                    cur_bel = self.open_b[ind]
                else:
                    # do partial
                    cur_bel = self.part_b[ind]
            else:
                ind = self.rem_latticeids.index(obj.obj_id)
                # do fully open, its always open
                cur_bel = self.rem_open_b[ind]

            obj_bel[i] = cur_bel
            # print "Current Belief : ", cur_bel, " Obj_bel[i] : ", obj_bel[i]
            if not obj.has_moved:
                # do full occ
                full_occ_bel = self.get_full_occ_bel(ind)
            else:
                # We placed the object in an open location with nothing behind it
                full_occ_bel = 0.
            obj_bel[i + len(vis_objs)] = full_occ_bel

        print "Object recog probs:\n\t", "\n\t".join(["%2d %1.3f" % (i, o_i) for i, o_i in enumerate(obj_bel)])
        joint_bel = self.joint_belief(obj_bel)
        print "Joint belief:\n\t", "\n\t".join(["%2d %1.3f" % (i, o_i) for i, o_i in enumerate(joint_bel)])
        return joint_bel

    def get_visible_objects(self):
        tbl_objs = []
        tbl_inds = []
        for i in range(self.numobjects):
            # print "get_vis", i, self.full_occ_list[i]
            if len(self.full_occ_list[i]) != 0:
                continue
            new_tbl_obj = TableObject(self.latticeids[i], self.part_occ_list[i], False, False, self.c_grasps[i], self.f_grasps[i])
            tbl_objs.append(new_tbl_obj)
            tbl_inds.append(i)

        for n_obj in tbl_objs:
            n_obsts = []
            for o_obst in n_obj.obstructors:
                n_obsts.append(tbl_objs[tbl_inds.index(self.latticeids.index(o_obst))])
            n_obj.obstructors = n_obsts
        tbl_objs.extend(self.get_moved_objects())
        return tbl_objs

    def get_moved_objects(self):
        tbl_objs = []
        print self.rem_numobjects
        print self.rem_latticeids
        print self.rem_c_grasps
        print self.rem_f_grasps
        print self.printConf()
        for i in range(self.rem_numobjects):
            new_tbl_obj = TableObject(self.rem_latticeids[i], [], False, True, self.rem_c_grasps[i], self.rem_f_grasps[i])
            tbl_objs.append(new_tbl_obj)
        return tbl_objs

    def sortonY(self):
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

    def removeObject(self, index):
        self.numobjects -= 1
        self.rem_numobjects += 1
        objId = self.ids.pop(index)
        self.rem_ids.append(objId)
        x, y, z = self.positions.pop(index)
        x_offset = 50 * (self.rem_numobjects-1)
        self.rem_positions.append([10+x_offset, y+180, 0])
        self.rem_dimensions.append(copy.copy(self.dimensions.pop(index)))
        self.rem_colors.append(self.colors.pop(index))
        self.rem_full_occ_list.append(copy.copy(self.full_occ_list.pop(index)))
        self.rem_part_occ_list.append(copy.copy(self.part_occ_list.pop(index)))
        self.rem_latticeids.append(self.latticeids.pop(index))
        self.rem_c_grasps.append(self.c_grasps.pop(index))
        self.rem_f_grasps.append(self.f_grasps.pop(index))
        self.rem_open_b.append(self.open_b.pop(index))
        self.rem_part_b.append(self.part_b.pop(index))

        for pol in self.part_occ_list:
            if pol.count(objId) > 0:
                pol.remove(objId)
        for fol in self.full_occ_list:
            if fol.count(objId) > 0:
                fol.remove(objId)

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
