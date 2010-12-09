
def half_gauss(sigma=0.07):
    while True:
        num = random.gauss(0., sigma)
        if num < 0. or num > 1.:
                continue
        return num

def part_gauss(sigma=0.1):
    while True:
        num = random.gauss(0.2, sigma)
        if num < 0. or num > 1.:
                continue
        return num

def simulate_vision(num_objects, goal_ind):
    open_b = [0.] * num_objects
    part_b = [0.] * num_objects
    for i in range(num_objects):
        if i == goal_ind:
            open_b[i] = 1. - half_gauss()
            part_b[i] = 1. - part_gauss()
        else:
            open_b[i] = half_gauss()
            part_b[i] = part_gauss()
    return open_b, part_b

