#! /usr/bin/python

import numpy as np
from math import fabs
import copy
from state_rep import *

class MDP():
    def __init__(self, t_world, g_cost = -1., goal_rew = 10., disc=0.95):
        self.world = t_world
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
                if i == goal_ind:
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

    def V_policy(self, V, st_ind, goal_ind):
        if i == goal_ind:
            r = self.goal_reward
        else:
            r = self.grasp_cost
        cur_v = np.array([r + sum(V * self.succ_probs(st_ind, a_i)) for a_i in self.succ_acts(st_ind)])
        return self.succ_acts(st_ind)[np.argmax(cur_v)]

    def print_V(self, V, goal_ind):
        for i, v in enumerate(V):
            if i == goal_ind:
                print i, "%3.2f" % v, [(self.world.table_actions[act_ind].state_final_list[0][1].state_id, "%1.2f" % (self.world.table_actions[act_ind].state_final_list[0][0])) for act_ind in self.succ_acts(i)], "**** Goal ****"
            else:
                print i, "%3.2f" % v, [(self.world.table_actions[act_ind].state_final_list[0][1].state_id, "%1.2f" % (self.world.table_actions[act_ind].state_final_list[0][0])) for act_ind in self.succ_acts(i)]

    def q_mdp_policy(self, ind, b, e=1):
        N = len(self.world.table_states[0].table_objects)
        q_list = []
        for i in range(N+1):
            V = self.value_iteration(i)
#           if i == goal_ind:
#               r = self.goal_reward
#           else:
#               r = self.grasp_cost
            r = self.grasp_cost
            cur_q = np.array([r + sum(V * self.succ_probs(ind, a_i)) for a_i in self.succ_acts(ind)])
            q_list.append(cur_q * b[i])

        return self.succ_acts(ind)[np.argmax(sum(q_list))], zip(*[self.succ_acts(ind), sum(q_list).tolist()])

    def obs_func(self, obs, tbl_st, goal_ind, tpr = 0.9, fpr = 0.2):
        # observation function p(z|x)
        # obs recognized object (obs) as the goal object
        # goal_ind index of the goal object
        num_uncov = sum([len(obj.obstructors) == 0 for obj in tbl_st.table_objects])
        if goal_ind != -1: 
            goal_uncov = len(tbl_st.table_objects[goal_ind].obstructors) == 0
            if not goal_uncov:
                if obs == -1:
                    return 1.
                else:
                    return 0.
        # c = (1. - fpr) ** (num_uncov - 1)
        c = 1.
        if obs != -1:
           if goal_ind != -1:
               if obs == goal_ind:
                   return tpr * c
               else:
                   return (1. - tpr) * c
           else:
               return fpr * c
        else:
           if goal_ind != -1:
               return (1. - tpr) * c
           else:
               return (1. - fpr) * c

    def bayes_filter(self, b, act_ind, obs, recog_prob = 0.9):
        # only for successful action
        ret_b = b.copy()
        act = self.world.table_actions[act_ind]
        new_st = act.state_final_list[0][1]
        for j, b_j in enumerate(b[0:-1]):
#           recog_joint = 1.0
#           for z_val in z:
#               if z_val:
#                   recog_joint *= recog_prob
#               else:
#                   recog_joint *= 1. - recog_prob
#           trans_prob = act.state_final_list[0][0]
#           ret_b *= recog_joint * trans_prob

            obs_prob = self.obs_func(obs, new_st, j)

            ret_b[j] *= obs_prob
#           c_sum = 0.
#           for ps in act.state_final_list:
#               c_sum += ps[0] * b[ps[1].state_id]
        ret_b[-1] *= self.obs_func(obs, new_st, -1)
        return normalize(ret_b)

    def conditional_entropy(self, b, act_ind, obs, new_b=None):
        if new_b is None:
            new_b = self.bayes_filter(b, act_ind, obs)
        temp = new_b * np.log(new_b)
        temp2 = [0. if np.isnan(t) else t for t in temp]
        return -sum(temp2)

    def expected_info_gain(self, ind, b, alpha = 0.8):
        tbl_st = self.world.table_states[ind]

        act_values = []
        for act in tbl_st.from_actions:
            # reward = np.ones(len(b)) * self.grasp_cost
            pos_obs = range(len(b)-1) + [-1]
            # this is hacked only to work with grasp action-failure world
            trans_prob = act.state_final_list[0][0]
            new_st = act.state_final_list[0][1]
            inner = 0.
            for obs in pos_obs:
                # print "previous entropy:", obs, self.conditional_entropy(b, act.action_id, obs, new_b=b)
                # print "current entropy:", obs, self.conditional_entropy(b, act.action_id, obs)
                for goal_ind in pos_obs:
                    grasp_succ = self.conditional_entropy(b, act.action_id, obs) * self.obs_func(obs, new_st, goal_ind) * trans_prob
                    grasp_fail = self.conditional_entropy(b, act.action_id, obs, new_b=b) * self.obs_func(obs, tbl_st, goal_ind) * (1. - trans_prob)
                    inner += grasp_succ + grasp_fail
            act_values.append(sum((self.grasp_cost - alpha * inner) * np.array(b)))
        return tbl_st.from_actions[np.argmax(act_values)].action_id, act_values

def simulation_no_find(mdp, b_init, method):
    import random
    cur_ind = 0
    if method == mdp.q_mdp_policy:
        print "-" * 26, "QMDP", "-" * 26
    else:
        print "-" * 20, "Expected Entropy", "-" * 20
    b = b_init.copy()
    last_b = b.copy()
    print "Initial belief:", "[", ", ".join(["%1.2f" % (np.log(b_i)) for b_i in b]), "]"
    while cur_ind != (len(mdp.world.table_states) - 1):
        act_id, vals = method(cur_ind, b)
        act = mdp.world.table_actions[act_id]
        print "Action %d taken.  <%s>" % (act_id, act)
        # we will always succeed
        prob = act.state_final_list[0][0]
        print "\tProbability of success: %1.2f" % (prob)
        new_st = act.state_final_list[0][1]
        print "\tNow in state %d" % (new_st.state_id)
        cur_ind = new_st.state_id
        last_b = b.copy()
        b = mdp.bayes_filter(b, act_id, -1) # no goal object seen
        print "\tNew belief:", "[", ", ".join(["%1.2f" % (np.log(b_i)) for b_i in b]), "]"
        print "\tEntropy Difference: %1.4f" % (entropy_difference(last_b, b))

def entropy_difference(b_init, b_final):
    temp = b_init * np.log(b_init)
    temp2 = [0. if np.isnan(t) else t for t in temp]
    entropy1 = -sum(temp2)
    temp = b_final * np.log(b_final)
    temp2 = [0. if np.isnan(t) else t for t in temp]
    entropy2 = -sum(temp2)
    return entropy1 - entropy2

