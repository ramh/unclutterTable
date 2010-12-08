#! /usr/bin/python

import numpy as np
from math import fabs
import copy

class TableObject():
    def __init__(self, o_id, obs, is_p, has_m, c_grasp, f_grasp):
        self.obj_id = o_id
        self.obstructors = obs
        self.obstructing = []
        self.is_potential = is_p
        self.has_moved = has_m
        self.cur_grasp = c_grasp
        self.unobs_grasp = f_grasp
    def __str__(self):
        return ("Obj ID: " + str(self.obj_id) + "\n\t" +
                "Has moved: " + str(self.has_moved) + "\n\t" + 
                "Current Graspability: " + str(self.cur_grasp) + "\n\t" +
                "Unobstructed Graspability: " + str(self.unobs_grasp) + "\n\t" +
                "Is Potential: " + str(self.is_potential) + "\n\t" +
                "Obstructors: " + ", ".join([str(obs.obj_id) for obs in self.obstructors]) + "\n")

GRASP_REMOVE = 0
GRASP_GOAL = 1
EXIT_NO_GOAL = 2

class TableAction():
    def __init__(self, obj_rem, si, sf_list, act_type=GRASP_REMOVE):
        self.obj_rem = obj_rem
        self.state_init = si
        self.state_final_list = sf_list
        self.act_type = act_type
    def __str__(self):
        if self.act_type == GRASP_REMOVE:
            return ("Object removed: %d " % (self.obj_rem) + "Init state: " + str(self.state_init.state_id) + " " +
                "Final states: "+ ", ".join([ "[%1.2f %s]" % (pa[0], pa[1].state_id) for pa in self.state_final_list]))
        if self.act_type == GRASP_GOAL:
            return ("Goal returned: %d " % (self.obj_rem) + "Init state: " + str(self.state_init.state_id) + " " +
                "Final states: "+ ", ".join([ "[%1.2f %s]" % (pa[0], pa[1].state_id) for pa in self.state_final_list]))
        if self.act_type == EXIT_NO_GOAL:
            return ("Search ended, no goal: %d " % (self.obj_rem) + "Init state: " + str(self.state_init.state_id) + " " +
                "Final states: "+ ", ".join([ "[%1.2f %s]" % (pa[0], pa[1].state_id) for pa in self.state_final_list]))

class TableState():
    def __init__(self, ts_id, tbl_objs, is_exit=False, obj_ind_exit=-100):
        self.state_id = ts_id
        self.is_exit = is_exit
        if not is_exit:
            self.table_objects = tbl_objs
            self.objs_not_moved = set()
            for obj in self.table_objects:
                obj.obstructing = []
            for obj in self.table_objects:
                if not obj.has_moved:
                    self.objs_not_moved.add(obj.obj_id)
                for obst in obj.obstructors:
                    obst.obstructing.append(obj)
        else:
            self.obj_ind_exit = obj_ind_exit
        self.from_actions = []
        self.to_actions = []

    def has_same_moves(self, ts):
        return ts.objs_not_moved == self.objs_not_moved

    def __str__(self):
        if not self.is_exit:
            return ("State ID: " + str(self.state_id) + "\n"
                    "\tState objects:\n"+"\n".join([obj.__str__() for obj in self.table_objects]) +"\n"
                    "\tFrom actions:\n"+"\n\n".join([ act.__str__() for act in self.from_actions]) + "\n\n"
                    "\tTo actions:\n"+"\n\n".join([ act.__str__() for act in self.to_actions]))
        else:
            return ("State ID: " + str(self.state_id) + "\n"
                    "\tTerminal state\n" +"\n"
                    "\tReturned index: %d\n\n" % (self.obj_ind_exit))

class TableWorld():
    def __init__(self, num_objs, tbl_sts, tbl_acts):
        self.num_objs = num_objs
        self.table_states = tbl_sts
        for i, st in enumerate(self.table_states):
            st.state_id = i
        self.table_actions = tbl_acts
        for i, act in enumerate(self.table_actions):
            act.action_id = i

    def is_terminal_action(self, act_id):
        return self.table_actions[act_id].act_type != GRASP_REMOVE

    def __str__(self):
        return ("-" * 20 + " Table States " + "-" * 20 + "\n" + ("\n" + "-" * 60 + "\n").join([ts.__str__() for ts in self.table_states]) + 
                "\n" + "-" * 20 + " Table Actions " + "-" * 20 + "\n" + "\n\n".join([ts.__str__() for ts in self.table_actions]))
        
def make_potential_objs(v_objs):
    ret_objs = []
    max_id = max([o.obj_id for o in v_objs])
    for obj in v_objs:
        ret_objs.append(TableObject(obj.obj_id + max_id + 1, [obj], True, False, 0.0, 1.0))
    return ret_objs

def table_world_generator(vis_objs):
    tbl_objs = vis_objs + make_potential_objs(vis_objs)

    num_real = 0
    for obj in tbl_objs:
        if obj.is_potential:
            num_real += 1

    state_id = 0

    all_levels = [[TableState(state_id, tbl_objs)]]
    state_id += 1
    all_actions = []
    for i in range(num_real):
        last_level = all_levels[-1]
        cur_level = []
        for table_state in last_level:
            for obj in table_state.table_objects:
                if not obj.is_potential and not obj.has_moved:
                    # create new state
                    new_tbl_objs = copy.deepcopy(table_state.table_objects)
                    rem_i = -1
                    for i, n_obj in enumerate(new_tbl_objs):
                        if obj.obj_id == n_obj.obj_id:
                            rem_i = i
                        else:
                            rem_j = -1
                            for j, o_obj in enumerate(n_obj.obstructors):
                                if o_obj.obj_id == obj.obj_id:
                                    rem_j = j

                            if rem_j != -1:
                                del n_obj.obstructors[rem_j]

                    if rem_i == -1:
                        raise Exception("Bad obj structure")

                    new_tbl_objs[rem_i].has_moved = True
                    new_tbl_objs[rem_i].obstructors = []
                    new_tbl_objs[rem_i].obstructing = []
                    made_state = TableState(state_id, new_tbl_objs)

                    new_state = None
                    for c_state in cur_level:
                        if c_state.has_same_moves(made_state):
                            new_state = c_state
                    if new_state is None:
                        new_state = made_state
                        state_id += 1
                        cur_level.append(new_state)

                    # Create action
                    if len(new_tbl_objs[rem_i].obstructors) == 0:
                        graspability = obj.cur_grasp
                    else:
                        graspability = obj.unobs_grasp

                    sf_acts = [ [ graspability, new_state ], [ 1. - graspability, table_state ] ]
                    act = TableAction(rem_i, table_state, sf_acts)
                    table_state.from_actions.append(act)
                    table_state.to_actions.append(act)
                    new_state.to_actions.append(act)
                    all_actions.append(act)

        all_levels.append(cur_level)
    all_states = []
    for level in all_levels:
        all_states.extend(level)
    end_states = []
    for i, obj in enumerate(tbl_objs):
        # add state
        ret_goal_state = TableState(state_id, None, True, i)
        end_states.append(ret_goal_state)
        state_id += 1
        # make actions
        for st in all_states:
            if len(st.table_objects[i].obstructors) == 0:
                graspability = obj.unobs_grasp
                sf_acts = [ [ graspability, ret_goal_state ], [ 1. - graspability, st ] ]
                act = TableAction(i, st, sf_acts, GRASP_GOAL)
                st.from_actions.append(act)
                st.to_actions.append(act)
                ret_goal_state.to_actions.append(act)
                all_actions.append(act)

    exit_goal_state = TableState(state_id, None, True, -1)
    end_states.append(exit_goal_state)
    for st in all_states:
        sf_acts = [ [ 1., exit_goal_state ] ]
        act = TableAction(-1, st, sf_acts, EXIT_NO_GOAL)
        st.from_actions.append(act)
        st.to_actions.append(act)
        exit_goal_state.to_actions.append(act)
        all_actions.append(act)
                    
    all_states.extend(end_states)
    return TableWorld(len(tbl_objs), all_states, all_actions)

def normalize(b):
    return b / np.linalg.norm(b, 1)

