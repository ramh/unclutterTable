#! /usr/bin/python

import numpy as np
from math import fabs
import copy

from state_rep import *
from qmdp import *

t1 = TableObject(1, [], False, False, 0.8, 0.8)
t2 = TableObject(2, [], False, False, 0.7, 0.7)
t3 = TableObject(3, [t1, t2], False, False, 0.3, 0.8)
t4 = TableObject(4, [t3], False, False, 0.2, 0.9)
t5 = TableObject(5, [t4], False, False, 0.1, 0.3)
vis_objs = [t1, t2, t3, t4, t5]

table_world = table_world_generator(vis_objs)

# print table_world.__str__()

goal_ind = 6
print table_world.table_states[1]
mdp = MDP(table_world)
V = mdp.value_iteration(goal_ind, 0.001)
print "-" * 20, " V ", "-" * 20
mdp.print_V(V, goal_ind)
b = normalize(np.ones(2 * len(vis_objs)+1))
print "b", b
b[0] = 2.9
mdp.call_planning(b, 1)
simulation_no_find(mdp, b, mdp.q_mdp_policy)
simulation_no_find(mdp, b, mdp.expected_info_gain)

# Q = mdp.q_mdp(b)
# mdp.print_Q(Q, b)
# for i in range(len(V)-1):
#     print i, mdp.q_mdp_policy(i, b)
#     print i, mdp.expected_info_gain(i, b)
#     print "   ", mdp.q_mdp_policy(i, b)

