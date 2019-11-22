from enum import Enum
class Strats(Enum):
	LANE = 0
	THREE = 1
	LANE_THREE = 2

class Stats():
	def __init__(self):
		self.try_2 = 0
		self.hit_2 = 0
		self.try_3 = 0
		self.hit_3 = 0

def build_data_dic():
	data = {
		'even': {
			'vitoria': [],
			'derrota': []
		},
		'one-sided': {
			'vitoria': [],
			'derrota': []
		}
	}

	for gameType in data:
		for result in data[gameType]:
			for strat1 in Strats:
				data[gameType][result].append([])
				for strat2 in Strats:
					data[gameType][result][strat1.value].append([])
					data[gameType][result][strat1.value][strat2.value] = Stats()

	return data

data = build_data_dic()
print(data)
#print(data['even']['vitoria'][0][2].try_2)