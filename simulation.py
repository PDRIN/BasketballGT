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

def choose_strat(mixed_strategy_equi):
	thresholds = np.cumsum(mixed_strategy_equi)
	thresholds *= 100000

	rand = random.randint(1,100000)

	if rand <= thresholds[0]:
		return 0
	elif rand <= thresholds[1]:
		return 1
	else:
		return 2

def rand_shot_type(shot_chances):
	rand = random.randint(1,100000)

	if rand <= (shot_chances['chance_2'])*100000:
		return 2
	else:
		return 3

def get_shot_hit(shot_type, shot_accs):
	rand = random.randint(1,100000)

	if shot_type == 2:
		if rand > shot_accs['acc_2'] * 100000:
			return False
		else:
			return True

	elif shot_type == 3:
		if rand > shot_accs['acc_3'] * 100000:
			return False
		else:
			return True

def get_points_scored(shot_type, shot_hit):
	if shot_type == 2 and shot_hit:
		return 2
	elif shot_type == 3 and shot_hit:
		return 3
	else:
		return 0

n_turns = 100

data = read_data()

mixed_nash_p1_even = [0.37924, 0.10986, 0.5109]
mixed_nash_p2_even = [0.18665,0.23077,0.58258]

mixed_nash_p1_one = [0.79501,0,0.20499]
mixed_nash_p2_one = [0.66376,0.33624,0]

score1 = np.zeros((n_turns,), dtype=int)
score2 = np.zeros((n_turns,), dtype=int)

for turn in range(0, n_turns):
	strat1 = choose_strat(mixed_nash_p1_even)
	strat2 = choose_strat(mixed_nash_p2_even)

	shot_type = rand_shot_type(data['shot_chances']['even'][strat1][strat2])
	shot_hit = get_shot_hit(shot_type, data['shot_chances']['even'][strat1][strat2])

	points = get_points_scored(shot_type, shot_hit)

	score1[turn] = points

for turn in range(0, n_turns):
	strat1 = choose_strat(mixed_nash_p1_even)
	strat2 = choose_strat(mixed_nash_p2_even)

	shot_type = rand_shot_type(data['shot_chances']['even'][strat1][strat2])
	shot_hit = get_shot_hit(shot_type, data['shot_chances']['even'][strat1][strat2])

	points = get_points_scored(shot_type, shot_hit)

	score2[turn] = points

print(np.cumsum(score1)[-1])
print(np.cumsum(score2)[-1])