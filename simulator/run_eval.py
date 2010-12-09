#! /usr/bin/python

import random
import sys
from qmdp.state_rep import TableObject

configs = range(1, 5)
num_goals = 25
num_visions = 20
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
config_ids = []
goal_ids = []
visions = []
def get_config_goal_data(config_id, goal_id):
    ind = config_ids.index(config_id)
    return trial_data[ind][goal_ids[ind].index(goal_id)]

def print_data(trial_data):
    for conf_ind, goals in enumerate(trial_data):
        for goal_ind, goal_id in enumerate(goals):
            print "Trial: config_id = %2d, goal_ind = %2d"
            print trial_data[conf_ind][goal_ind]

for config_id in configs:
    cur_goal_ids = []
    cur_c_visions = []
    cur_c_data = []
    for g_trial in range(num_goals):
        cur_c_g_visions = []
        cur_c_g_data = []
        t_info = TableInfo(config_id, g_trial)
        b_init = t_info.get_current_belief(t_info.get_visible_objects())
        goal_ind = sample_dist(b_init)
        for v_trial in range(num_visions):
            open_b, part_b = simulate_vision(num_objs, goal_ind)
            cur_data_q = [[], [], []]
            cur_data_i = [[], [], []]
            for g_r_trial in range(num_runs):
                num_steps, is_success, succ_grasp_steps = run_simulation(config_id, goal_ind, copy.copy(open_b), copy.copy(part_b), 0)
                cur_data_q[0].append(num_steps)
                cur_data_q[1].append(is_success)
                cur_data_q[2].append(succ_grasp_steps)

                num_steps, is_success, succ_grasp_steps = run_simulation(config_id, goal_ind, copy.copy(open_b), copy.copy(part_b), 1)
                cur_data_i[0].append(num_steps)
                cur_data_i[1].append(is_success)
                cur_data_i[2].append(succ_grasp_steps)
            avg_data_q = [float(sum(d))/len(d) for d in cur_data_q]
            avg_data_i = [float(sum(d))/len(d) for d in cur_data_i]
            cur_c_g_data.append([avg_data_q, avg_data_i])

        cur_goal_ids.append(goal_ind)
        cur_c_visions.append(cur_c_g_visions)
        cur_c_data.append(cur_c_g_data)

    visions.append(cur_c_visions)
    goal_ids.append(cur_goal_ids)
    config_ids.append(config_id)
    data.append(cur_c_data)

