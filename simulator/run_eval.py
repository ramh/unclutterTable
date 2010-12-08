#! /usr/bin/python

import random
import sys
from qmdp.state_rep import TableObject

configs = range(1, 5)
num_goals = 25
num_runs = 10

for config_id in configs:
    for g_trial in range(num_goals):
        t_info = TableInfo(config_id)

        for g_r_trial in range(num_runs):
            pass

