from enum import Enum

class Strats(Enum):
	LANE = 0
	THREE = 1
	LANE_THREE = 2

def create_payoff_matrix():
	payoff_m = []
	for strat1 in Strats:
		payoff_m.append([])
		for strat2 in Strats:
			payoff_m[strat1.value].append([])

	return payoff_m

def calculate_payoff_matrix(data, payoff_m):
	for strat1 in Strats:
		for strat2 in Strats:
			cell = data[strat1.value][stra2.value]
			payoff = (cell.acc_2 * 2) + (cell.acc_3 * 3)
			payoff_m[strat1.value][stra2.value] = payoff