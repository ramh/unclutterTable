import random

from TableInfo import TableInfo
from qmdp.qmdp import *

def run_simulation(configId, goalInd, open_b, part_b, planner_type):
    num_steps = 0
    successful_grasp_steps = 0
    has_experiment_finished = False
    tableinfo = TableInfo(configId, goalInd)
    tableinfo.open_b = open_b
    tableinfo.part_b = part_b

    while(not has_experiment_finished):
        visible_objects = tableinfo.get_visible_objects()
        belief = tableinfo.get_current_belief(visible_objects)
        print "EXECUTE PLANNING Input: ", belief, visible_objects, planner_type
        latticeInd = execute_planning_step(belief, visible_objects, planner_type)
        print "EXECUTE PLANNING Output: ", latticeInd

        if latticeInd == 0:
            has_experiment_finished = True # no longer going to search for the goal
        elif latticeInd < 0:
            has_experiment_finished = True
            if abs(latticeInd) not in tableinfo.latticeids: # goal already removed (no more uncertainities on grasps)
                successful_grasp_steps += 1 # return goal is a success grasp always
            else:
                index = tableinfo.latticeids.index(-latticeInd)
                prob = tableinfo.f_grasps[index]
                rand = random.random()
                if rand < prob: # Chance of successful removal of object = Full Graspability probability
                    tableinfo.removeObject(index)
                    successful_grasp_steps += 1
                    has_experiment_finished = True  # grasped & returned the goal object successfully
        else:
            index = tableinfo.latticeids.index(latticeInd)
            prob = tableinfo.f_grasps[index]
            rand = random.random()
            if rand < prob: # Chance of successful removal of object = Full Graspability probability
                tableinfo.removeObject(index)
                successful_grasp_steps += 1
        num_steps += 1

    is_success = (latticeInd!=0) # the above while loop can quit only when latticeInd<=0, and when its != 0, its a success
    print "Result: ", num_steps, is_success, successful_grasp_steps
    return num_steps, is_success, successful_grasp_steps

#run_simulation(2, 0, [ 0.95, 0.2, 0.1, 0.5, 0.1 ], [ 0.95, 0.2, 0.1, 0.5, 0.1 ], 0)

