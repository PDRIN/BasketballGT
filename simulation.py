import numpy as np
import random
import json
from enum import Enum

class Strats(Enum):
	LANE = 0
	THREE = 1
	LANE_THREE = 2

def read_data():
	filename = 'results/results.txt'
	with open(filename) as f:
	    data = json.load(f)
	    return data

def choose_strats(mixed_strategy_equi):
	thresholds = np.cumsum(mixed_strategy_equi)
	thresholds *= 100000

	rand = random.randint(1,100000)


# def mixed_strategy(m):
# 	a00 = (m[0][0] - m[0][2]) - (m[1][0] - m[1][2])
# 	a01 = (m[0][1] - m[0][2]) - (m[1][1] - m[1][2])
# 	b0 = (m[1][2] - m[0][2])

# 	a10 = (m[1][0] - m[1][2]) - (m[2][0] - m[2][2])
# 	a11 = (m[1][1] - m[1][2]) - (m[2][1] - m[2][2])
# 	b1 = (m[2][2] - m[1][2])

# 	a = np.array([[a00, a01], [a10, a11]])
# 	b = np.array([b0,b1])

# 	p0, p1 = np.linalg.solve(a,b)

# 	p2 = 1 - p0 - p1

# 	return [p0, p1, p2]

# data = read_data()

# nash_mix_strat_even = mixed_strategy(data['payoffs']['even'])
# nash_mix_strat_one = mixed_strategy(data['payoffs']['one-sided'])

# print(mixed_strategy(data['payoffs']['even']))
# print(mixed_strategy(data['payoffs']['one-sided']))

n_turns = 100

data = read_data()

mixed_nash_p1_even = [0.37924, 0.10986, 0.5109]
mixed_nash_p2_even = [0.18665,0.23077,0.58258]

mixed_nash_p1_one = [0.79501,0,0.20499]
mixed_nash_p2_one = [0.66376,0.33624,0]

for turn in xrange(0, n_turns):
	strat1 = choose_strat(mixed_nash_p1_even)
	strat2 = choose_strat(mixed_nash_p2_even)

	shot_type = rand_shot_type(shot_type_chance)
	shot_hit = 



