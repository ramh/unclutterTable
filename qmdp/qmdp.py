#! /usr/bin/python

import numpy as np
from math import fabs
import copy

class TableObject():
    def __init__(self, o_id, obs, is_p, has_m, graspab):
        self.obj_id = o_id
        self.obstructors = obs
        self.is_potential = is_p
        self.has_moved = has_m
        self.graspability = graspab
    def __str__(self):
        return ("Obj ID: " + str(self.obj_id) + "\n\t" +
                "Has moved: " + str(self.has_moved) + "\n\t" + 
                "Graspability: " + str(self.graspability) + "\n\t" +
                "Is Potential: " + str(self.is_potential) + "\n\t" +
                "Obstructors: " + ", ".join([str(obs.obj_id) for obs in self.obstructors]) + "\n")


class TableAction():
    def __init__(self, si, sf_list):
        self.state_init = si
        self.state_final_list = sf_list
        self.reward = -1.0
    def __str__(self):
        return ("Init state: " + str(self.state_init.state_id) + "\n" +
                "Final states: "+ ", ".join([ "[%1.2f %s]" % (pa[0], pa[1].state_id) for pa in self.state_final_list]))

class TableState():
    def __init__(self, ts_id, tbl_objs):
        self.state_id = ts_id
        self.table_objects = tbl_objs
        self.objs_not_moved = set()
        for obj in self.table_objects:
            if not obj.has_moved:
                self.objs_not_moved.add(obj.obj_id)
        self.from_actions = []
        self.to_actions = []

    def has_same_moves(self, ts):
        return ts.objs_not_moved == self.objs_not_moved

    def __str__(self):
        return ("State ID: " + str(self.state_id) + "\n"
                "State objects:\n"+"\n".join([obj.__str__() for obj in self.table_objects]) +"\n"
                "From actions:\n"+"\n\n".join([ act.__str__() for act in self.from_actions]) + "\n\n"
                "To actions:\n"+"\n\n".join([ act.__str__() for act in self.to_actions]))

class TableWorld():
    def __init__(self, num_objs, tbl_sts, tbl_acts):
        self.num_objs = num_objs
        self.table_states = tbl_sts
        for i, st in enumerate(self.table_states):
            st.state_id = i
        self.table_actions = tbl_acts
        for i, act in enumerate(self.table_actions):
            act.action_id = i

    def __str__(self):
        print self.table_actions
        return ("-" * 20 + " Table States " + "-" * 20 + "\n" + ("\n" + "-" * 60 + "\n").join([ts.__str__() for ts in self.table_states]) + 
                "\n" + "-" * 20 + " Table Actions " + "-" * 20 + "\n" + "\n\n".join([ts.__str__() for ts in self.table_actions]))
        

t1 = TableObject(1, [], False, False, 0.8)
t2 = TableObject(2, [], False, False, 0.7)
t3 = TableObject(3, [t1, t2], False, False, 0.3)
t4 = TableObject(4, [t3], False, False, 0.2)
t5 = TableObject(5, [t4], False, False, 0.1)
vis_objs = [t1, t2, t3, t4, t5]

def get_potential_objs(v_objs):
    ret_objs = []
    for obj in v_objs:
        ret_objs.append(TableObject(obj.obj_id + len(v_objs), [obj], True, False, 0.0))
    return ret_objs

init_table_objects = vis_objs + get_potential_objs(vis_objs)

def table_world_generator(tbl_objs):
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
                    sf_acts = [ [ obj.graspability, new_state ], [ 1. - obj.graspability, table_state ] ]
                    act = TableAction(table_state, sf_acts)
                    table_state.from_actions.append(act)
                    table_state.to_actions.append(act)
                    new_state.to_actions.append(act)
                    all_actions.append(act)

        all_levels.append(cur_level)
    all_states = []
    for level in all_levels:
        all_states.extend(level)
    return TableWorld(len(tbl_objs), all_states, all_actions)

table_world = table_world_generator(init_table_objects)

print table_world.__str__()

class MDP():
    def __init__(self, t_world, g_cost = -1., goal_rew = 10., disc=0.9):
        self.world = t_world
        self.goal_ind = goal_ind
        self.grasp_cost = g_cost
        self.goal_reward = goal_rew
        self.discount = disc

    def succ_acts(self, st_ind):
        return [a.action_id for a in self.world.table_states[st_ind].from_actions]

    def succ_probs(self, st_ind, act_ind):
        probs = np.zeros(len(self.world.table_states))
        for sf in self.world.table_actions[act_ind].state_final_list:
            probs[sf[1].state_id] = sf[0]
        return probs

    def value_iteration(self, goal_ind, e=1):
        V = np.ones(len(self.world.table_states)) * self.grasp_cost
        while True:
            _V = V.copy()
            d = 0
            for i in range(len(V)):
                if i == self.goal_ind:
                    r = self.goal_reward
                else:
                    r = self.grasp_cost
                if i == len(V) - 1:
                    V[i] = self.discount * r
                else:
                    V[i] = self.discount * max(
                           [r + sum(V * self.succ_probs(i, a_i)) for a_i in self.succ_acts(i)])
                diff = fabs(V[i] - _V[i])
                if diff > d:
                    d = diff
            if d <= e * (1 - self.discount) / self.discount:
                break
        return V

    def V_policy(self, V, st_ind):
        if i == self.goal_ind:
            r = self.goal_reward
        else:
            r = self.grasp_cost
        cur_v = np.array([r + sum(V * self.succ_probs(st_ind, a_i)) for a_i in self.succ_acts(st_ind)])
        return self.succ_acts(st_ind)[np.argmax(cur_v)]

    def print_V(self, V, goal_ind):
        for i, v in enumerate(V):
            if i == goal_ind:
                print i, "%3.2f" % v, [(mdp.world.table_actions[act_ind].state_final_list[0][1].state_id, "%1.2f" % (mdp.world.table_actions[act_ind].state_final_list[0][0])) for act_ind in mdp.succ_acts(i)], "**** Goal ****"
            else:
                print i, "%3.2f" % v, [(mdp.world.table_actions[act_ind].state_final_list[0][1].state_id, "%1.2f" % (mdp.world.table_actions[act_ind].state_final_list[0][0])) for act_ind in mdp.succ_acts(i)]

    def q_mdp_policy(self, ind, b, e=1):
        N = len(self.world.table_states[0].table_objects)
        q_list = []
        for i in range(N):
            V = self.value_iteration(i)
            if i == self.goal_ind:
                r = self.goal_reward
            else:
                r = self.grasp_cost
            cur_q = np.array([r + sum(V * self.succ_probs(ind, a_i)) for a_i in self.succ_acts(ind)])
            q_list.append(cur_q * b[i])

        return self.succ_acts(ind)[np.argmax(sum(q_list))], zip(*[self.succ_acts(ind), sum(q_list).tolist()])

    def print_Q(self, Q, b):
        for i in range(len(b)):
            print i, "belief:", "%1.2f" % (b[i])
        for i, q in enumerate(Q):
            print i, "%3.2f" % q, [(mdp.world.table_actions[act_ind].state_final_list[0][1].state_id, "%1.2f" % (mdp.world.table_actions[act_ind].state_final_list[0][0]), "%3.1f" % (self.Q_policy(Q, mdp.world.table_actions[act_ind].state_final_list[0][1].state_id, b))) for act_ind in mdp.succ_acts(i)]

def normalize(b):
    return b / np.linalg.norm(b)

goal_ind = 20
mdp = MDP(table_world)
V = mdp.value_iteration(goal_ind, 1)
mdp.print_V(V, goal_ind)
b = normalize(np.ones(len(init_table_objects)))
# Q = mdp.q_mdp(b)
# mdp.print_Q(Q, b)
for i in range(len(V)-1):
    print i, mdp.q_mdp_policy(i, b)

