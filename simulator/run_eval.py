#! /usr/bin/python

import random
import sys
from qmdp.state_rep import TableObject

configs = range(1, 5)
num_goals = 25
num_runs = 10

def sample_dist(dist):
    cdf = np.zeros(len(dist) - 1)
    for i in range(len(dist) - 1):
        for j in range(0, i+1):
            cdf[i] += dist[j]
    r = random.random()
    for i in range(len(dist) - 1):
        if r < cdf[i]:
            return i
    return len(dist) - 1

trial_data = []
for config_id in configs:
    for g_trial in range(num_goals):
        t_info = TableInfo(config_id)
        b_init = t_info.get_current_belief(t_info.get_visible_objects())
        goal_ind = sample_dist(b_init)

        for g_r_trial in range(num_runs):
            num_steps, is_success, succ_grasp_steps = run_simulation(config_id, goal_ind, planner_type)

