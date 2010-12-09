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

        if latticeInd > 0:
            # Chance of successful removal of object = Full Graspability probability
            index = tableinfo.latticeids.index(latticeInd)
            prob = tableinfo.f_grasps[index]
            rand = random.random()
            if rand < prob:
                tableinfo.removeObject(index)
                successful_grasp_steps += 1
            num_steps += 1
        else:
            has_experiment_finished = True

    is_success = (latticeInd!=0) # the above while loop can quit only when latticeInd<=0, and when its != 0, its a success
    print "Result: ", num_steps, is_success, successful_grasp_steps
    return num_steps, is_success, successful_grasp_steps

run_simulation(2, 0, 0)
