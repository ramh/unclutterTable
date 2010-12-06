#! /usr/bin/python

import numpy as np
from math import fabs
import copy
from state_rep import *

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
        for i in range(N+1):
            V = self.value_iteration(i)
            if i == self.goal_ind:
                r = self.goal_reward
            else:
                r = self.grasp_cost
            cur_q = np.array([r + sum(V * self.succ_probs(ind, a_i)) for a_i in self.succ_acts(ind)])
            q_list.append(cur_q * b[i])

        return self.succ_acts(ind)[np.argmax(sum(q_list))], zip(*[self.succ_acts(ind), sum(q_list).tolist()])

    def obs_func(self, obs, tbl_st, goal_ind, tpr = 0.9, fpr = 0.2):
        num_uncov = 
        goal_uncov = True
        if not goal_uncov:
            if 
        if obs != -1:
           if goal_ind != -1:
               if goal_uncov:

               else:


               prob = tpr * (1. - fpr) ** (num_uncov - 1)
           else:

        else:
           if goal_ind != -1:
               
           else:

        return prob
        
        

    def bayes_update(self, b, act_ind, z, recog_prob = 0.9):
        ret_b = b.copy()
        for j, b_j in enumerate(b):
            recog_joint = 1.0
            for z_val in z:
                if z_val:
                    recog_joint *= recog_prob
                else:
                    recog_joint *= 1. - recog_prob
            act = self.world.table_actions[act_ind]
            trans_prob = act.state_final_list[0][0]
            ret_b *= recog_joint * trans_prob
            ret_b[j]
            c_sum = 0.
            for ps in act.state_final_list:
                c_sum += ps[0] * b[ps[1].state_id]

    def expected_info_gain(self):
            act = self.world.table_actions[act_ind]
            trans_prob = act.state_final_list[0][0]
            inds_moved = act.state_init.objs_not_moved - act.state_final_list[0][1].objs_not_moved
            rem_obj_ind = inds_moved[0]
            num_z = len(rem_obj_ind.obstructing)


#   def print_Q(self, Q, b):
#       for i in range(len(b)):
#           print i, "belief:", "%1.2f" % (b[i])
#       for i, q in enumerate(Q):
#           print i, "%3.2f" % q, [(mdp.world.table_actions[act_ind].state_final_list[0][1].state_id, "%1.2f" % (mdp.world.table_actions[act_ind].state_final_list[0][0]), "%3.1f" % (self.Q_policy(Q, mdp.world.table_actions[act_ind].state_final_list[0][1].state_id, b))) for act_ind in mdp.succ_acts(i)]
