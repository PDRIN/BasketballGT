# 0 = time
# 1 = team1 (event)
# 2 = pointsAway (scored in this event)
# 3 = score
# 4 = pointsHome (scored in this event)
# 5 = team2 (event)
from enum import Enum
import os
import json

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

def remove_noise(string):
	newString = string
	if newString[-1] == '\n':
		newString = newString[:-1]
	if newString[0] == '\"':
		newString = newString[1:]
	
	return newString

def change_player(comp, player_out, player_in):
	truePlayerOut = remove_noise(player_out)
	truePlayerIn = remove_noise(player_in)

	print(truePlayerOut, truePlayerIn)

	comp['players'].remove(player_out)
	comp['players'].append(player_in)
	#solve_comp(comp)

def add_player_to_comp(comp, player):
	truePlayer = remove_noise(player)

	if truePlayer not in comp['players']:
		comp['players'].append(truePlayer)

def find_player(team, action, team_comps):
	words = action.split(' ')

	#if words[0][0] == '\"':
		#print('ADLER', action, path)

	if (action.find('misses') > 0) or (action.find('makes') > 0):
		add_player_to_comp(team_comps[team], words[0] + ' ' + words[1])

	elif action.find('enters') > 0:	
		if words[1] == 'Mbah':
			add_player_to_comp(team_comps[team], words[8] + ' ' + words[9])
		elif words[1] == 'Lemon':
			add_player_to_comp(team_comps[team], words[7] + ' ' + words[8])
		else:
			add_player_to_comp(team_comps[team], words[6] + ' ' + words[7])

def search_player(columns, team_comps, team1, team2):
	#team1 acts
	if columns[1] and len(team_comps[team1]['players']) < 5:
		find_player(team1, columns[1], team_comps)

	#team2 acts
	elif columns[5] and columns[5] != '\n' and len(team_comps[team2]['players']) < 5:
		find_player(team2, columns[5], team_comps)

def blank_teamcomp():
	return {
		'type': None,
		'players': []
	}

def first_read(file, team_comps):
	team1 = ''
	team2 = ''

	lines = file.readlines()

	for i, line in enumerate(lines):

		columns = line.split(',')

		if i == 0:
			team1 = columns[1]
			team2 = columns[5][:-1]
			team_comps[team1] = blank_teamcomp()
			team_comps[team2] = blank_teamcomp()


		elif i == 1 or i == 2:
			continue

		else:
			search_player(columns, team_comps, team1, team2)

		if len(team_comps[team1]['players']) == 5 and len(team_comps[team2]['players']) == 5:
			break

	print(team_comps)

def extract_payoff(team, victorious, action, team_comps, data):
	words = action.split(' ')

	#if words[0][0] == '\"':
		#print('ADLER', action, path)

	if (action.find('misses') > 0) or (action.find('makes') > 0):
		#soca bagulho no payoff

	elif action.find('enters') > 0:	

		player_out = words[0] + ' ' + words[1]

		if words[1] == 'Mbah':
			player_in = words[8] + ' ' + words[9]
			change_player(team_comps[team], player_out, player_in)

		elif words[1] == 'Lemon':
			player_in = words[7] + ' ' + words[8]
			change_player(team_comps[team], player_out, player_in)

		else:
			player_in = words[6] + ' ' + words[7]
			change_player(team_comps[team], player_out, player_in)


def search_team_action(columns, team_comps, data, team1, team2, victorious):
	#team1 acts
	if columns[1]:
		extract_payoff(team1, victorious, columns[1], team_comps, data)

	#team2 acts
	elif columns[5] and columns[5] != '\n':
		extract_payoff(team2, victorious, columns[1], team_comps, data)

def second_read(file, team_comps, data):
	team1 = ''
	team2 = ''

	lines = file.readlines()

	last_line = lines[-1]
	columns = last_line.split(',')
	score = columns[3]
	points = score.split('-')

	victorious = team1 if points[1] <= points[0] else team2

	for i, line in enumerate(lines):

		columns = line.split(',')

		if i == 0:
			team1 = columns[1]
			team2 = columns[5][:-1]

		elif i == 1 or i == 2:
			continue

		else:
			search_team_action(columns, team_comps, data, team1, team2, victorious)

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

################################################################################
################################################################################
################################################################################
################################################################################

evenDir = 'data/splitted/even/'
evenDirCod = os.fsencode(evenDir)
evenResultsFile = open('results/evenGames.txt', 'w')

oneDir = 'data/splitted/one_sided/'
oneDirCod = os.fsencode(oneDir)
oneResultsFile = open('results/oneGames.txt', 'w')

dirs = [evenDir, oneDir]

data = build_data_dic()

for d in dirs:

	cod = os.fsencode(d)
	
	for i, file in enumerate(os.listdir(cod)):
		# if d == evenDir:
		# 	read_file(path, data['even'])
		# else:
		# 	read_file(path, data['one-sided'])
		
		filename = os.fsdecode(file)

		path = d+filename

		f = open(path, 'r')

		team_comps = {}

		print(filename)

		first_read(f, team_comps)

		second_read(f, team_comps, data)

