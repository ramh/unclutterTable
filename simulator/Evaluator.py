#! /usr/bin/python

import random
import copy
import sys
from qmdp.state_rep import TableObject
from simulator.Experiment import run_simulation
from simulator.TableInfo import TableInfo
from simulator.utils import simulate_vision

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

class Evaluator():
    def __init__(self, debug = False):
        self.trial_data = []
        self.config_ids = []
        self.goal_ids = []
        self.visions = []
        self.debug = debug
        self.run_eval()

    def get_config_goal_data(self, config_id, goal_id):
        ind = self.config_ids.index(config_id)
        return self.trial_data[ind][self.goal_ids[ind].index(goal_id)]

    def print_data(self):
        for conf_ind, goals in enumerate(self.trial_data):
            for goal_ind, goal_id in enumerate(self.goal_ids[conf_ind]):
                for vis_ind, vis_type in enumerate(self.visions[conf_ind][goal_ind]):
                    print "Trial: config_id = %2d, goal_ind = %2d"
                    open_b, part_b = vis_type
                    print "Vision open:", ", ".join([ "%1.3f" % (o) for o in open_b])
                    print "Vision part:", ", ".join([ "%1.3f" % (o) for o in part_b])
                    print self.trial_data[conf_ind][goal_ind][vis_ind]

    def run_eval(self, configs = range(4, 5), num_goals = 2, num_visions = 5, num_runs = 3):
        n_runs = 0
        for config_id in configs:
            print "-" * 20, " Config %d " % (config_id), "-" * 20
            cur_goal_ids = []
            cur_c_visions = []
            cur_c_data = []
            for g_trial in range(num_goals):
                cur_c_g_visions = []
                cur_c_g_data = []
                #t_info = TableInfo(config_id, g_trial)
                #b_init = t_info.get_current_belief(t_info.get_visible_objects())
                #goal_ind = sample_dist(b_init)
                t_info = TableInfo(config_id)
                
                # only get goals that are buried
                n_tries = 0
                beg = -1
                while True and n_tries < 100:
                    goal_ind = random.randint(beg, t_info.numobjects - 1 )
                    if n_tries == 0 and goal_ind == -1:
                        beg = 0
                        break
                    if len(t_info.rem_part_occ_list) > 0:
                        break
                    n_tries += 1
                print "-" * 20, " Goal Ind %d " % (goal_ind), "-" * 20
                for v_trial in range(num_visions):
                    print "-" * 20, " Vision %d " % (v_trial), "-" * 20
                    open_b, part_b = simulate_vision(t_info.numobjects, goal_ind)
                    cur_data_q = [[], [], []]
                    cur_data_i = [[], [], []]
                    for g_r_trial in range(num_runs):
                        num_steps, is_success, succ_grasp_steps = run_simulation(config_id, goal_ind, copy.copy(open_b), copy.copy(part_b), 0)
                        cur_data_q[0].append(num_steps)
                        cur_data_q[1].append(is_success)
                        cur_data_q[2].append(succ_grasp_steps)
                        print "-" * 20, " Results Q ", "-" * 20
                        print num_steps, is_success, succ_grasp_steps

                        num_steps, is_success, succ_grasp_steps = run_simulation(config_id, goal_ind, copy.copy(open_b), copy.copy(part_b), 1)
                        cur_data_i[0].append(num_steps)
                        cur_data_i[1].append(is_success)
                        cur_data_i[2].append(succ_grasp_steps)
                        print "-" * 20, " Results I ", "-" * 20
                        print num_steps, is_success, succ_grasp_steps

                        print "Number of runs: %3d" % n_runs
                        n_runs += 1
                    avg_data_q = [float(sum(d))/len(d) for d in cur_data_q]
                    avg_data_i = [float(sum(d))/len(d) for d in cur_data_i]
                    cur_c_g_data.append([avg_data_q, avg_data_i])
                    cur_c_g_visions.append([open_b, part_b])

                cur_goal_ids.append(goal_ind)
                cur_c_visions.append(cur_c_g_visions)
                cur_c_data.append(cur_c_g_data)

            self.visions.append(cur_c_visions)
            self.goal_ids.append(cur_goal_ids)
            self.config_ids.append(config_id)
            self.trial_data.append(cur_c_data)

if __name__ == "__main__":
    import os
    import cPickle as pickle
    if len(sys.argv) == 1 or sys.argv[1] != "p":
        ev = Evaluator()
        ev.run_eval()
        pickle.dump(ev, file("eval_data.pickle", "w"))
        ev.print_data()
    else:
        ev = pickle.load(open("eval_data.pickle", "rb"))
        ev.print_data()

