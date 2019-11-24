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

	# print(comp)
	# print('In <<<<', truePlayerIn)
	# print('Out >>>>', truePlayerOut)

	if truePlayerIn in comp['players'] and truePlayerOut in comp['players']:
		print("POSITION CHANGE\n")
		return

	comp['players'].remove(truePlayerOut)
	comp['players'].append(truePlayerIn)
	#print(comp, '\n')

def add_player_to_comp(comp, player, ignore_list):
	truePlayer = remove_noise(player)

	if truePlayer not in comp['players'] and truePlayer not in ignore_list:
		comp['players'].append(truePlayer)

def blank_teamcomp():
	return {
		'type': None,
		'players': []
	}

def search_player(team, action, team_comps, ignore_list):
	words = action.split(' ')

	if (action.find('misses') > 0) or (action.find('makes') > 0):
		add_player_to_comp(team_comps[team], words[0] + ' ' + words[1], ignore_list)

	elif action.find('enters') > 0:
		ignore_list.append(remove_noise(words[0] + ' ' + words[1]))

		if words[1] == 'Mbah':
			add_player_to_comp(team_comps[team], words[8] + ' ' + words[9], ignore_list)
		elif words[1] == 'Lemon':
			add_player_to_comp(team_comps[team], words[7] + ' ' + words[8], ignore_list)
		else:
			add_player_to_comp(team_comps[team], words[6] + ' ' + words[7], ignore_list)

	elif action.find('rebound') > 0:
		if remove_noise(words[3]) == 'Team':
			return
		add_player_to_comp(team_comps[team], words[3] + ' ' + words[4], ignore_list)

def find_starting_comp(lines, starting_line, team_comps, team1, team2):
	t1_ignore_list = []
	t2_ignore_list = []

	team_comps[team1] = blank_teamcomp()
	team_comps[team2] = blank_teamcomp()

	for i, line in enumerate(lines[starting_line:]):
		columns = line.split(',')

		#team1 acts
		if columns[1] and len(team_comps[team1]['players']) < 5:
			search_player(team1, columns[1], team_comps, t1_ignore_list)

		#team2 acts
		elif columns[5] and columns[5] != '\n' and len(team_comps[team2]['players']) < 5:
			search_player(team2, columns[5], team_comps, t2_ignore_list)

		if len(team_comps[team1]['players']) == 5 and len(team_comps[team2]['players']) == 5:
			break

def get_team_names(line):
	columns = line.split(',')
	team1 = columns[1]
	team2 = columns[5][:-1]

	return team1, team2

def first_read(file, team_comps):
	lines = file.readlines()

	team1, team2 = get_team_names(lines[0])

	find_starting_comp(lines, 0, team_comps, team1, team2)

	print(team_comps, '\n')

def get_keyword(words):
	player_name = remove_noise(words[0] + ' ' + words[1])
	if player_name == 'L. Mbah':
		keyword = words[5]
	elif player_name == 'W. Lemon':
		keyword = words[4]
	else:
		keyword = words[3]

	return keyword

def is_2_point(words):
	keyword = get_keyword(words)
	if keyword[0] == '2':
		return True
	return False

def is_3_point(words):
	keyword = get_keyword(words)
	if keyword[0] == '3':
		return True
	return False

def set_comp_type(comp, team, positions, misses):
	has_cf = False
	has_c = False

	for player in comp[team]['players']:

		player_position = positions[team][player]

		if len(player_position) >= 5:
			player_position = misses[team][player]

		if player_position == 'C-F' or player_position == 'F-C':
			has_cf = True
		if player_position == 'C':
			has_c = True

	if has_cf and has_c:
		comp[team]['type'] = Strats.LANE

	#xor operation
	elif has_c != has_cf:
		comp[team]['type'] = Strats.LANE_THREE

	comp[team]['type'] = Strats.THREE

def extract_payoff(team, other_team, victorious, action, team_comps, game_type_data, positions, misses):
	words = action.split(' ')

	# if action == 'Start of 2nd quarter':
	# 	print(action.find("start"))

	if action.find('enters') > 0:	
		player_in = words[0] + ' ' + words[1]

		if words[1] == 'Mbah':
			player_out = words[8] + ' ' + words[9]
			change_player(team_comps[team], player_out, player_in)

		elif words[1] == 'Lemon':
			player_out = words[7] + ' ' + words[8]
			change_player(team_comps[team], player_out, player_in)

		else:
			player_out = words[6] + ' ' + words[7]
			change_player(team_comps[team], player_out, player_in)

		set_comp_type(team_comps, team, positions, misses)

		return

	team_strat = team_comps[team]['type'].value
	other_team_strat = team_comps[team]['type'].value

	if team == victorious:
		cell = game_type_data['victory'][team_strat][other_team_strat]
	else:
		cell = game_type_data['defeat'][team_strat][other_team_strat]

	if (action.find('misses') > 0):
		if is_2_point(words):
			cell.try_2 += 1

		elif is_3_point(words):
			cell.try_3 += 1

	if (action.find('makes') > 0):
		if is_2_point(words):
			cell.try_2 += 1
			cell.hit_2 += 1

		elif is_3_point(words):
			cell.try_3 += 1
			cell.hit_3 += 1

def get_victorious_team(line, team1, team2):
	columns = line.split(',')
	score = columns[3]
	points = score.split('-')

	victorious = team1 if points[1] <= points[0] else team2

	return victorious

def second_read(file, team_comps, data):
	player_position_file = open('results/player_team_position.txt')
	player_positions = json.load(player_position_file)

	#a miss file was manually created to fill misses in the dataset used to get player positions
	player_position_miss_file = open('results/player_team_position_misses.txt')
	player_misses = json.load(player_position_miss_file)

	lines = file.readlines()
	
	team1, team2 = get_team_names(lines[0])

	victorious = get_victorious_team(lines[-1], team1, team2)

	set_comp_type(team_comps, team1, player_positions, player_misses)
	set_comp_type(team_comps, team2, player_positions, player_misses)

	for i, line in enumerate(lines):

		columns = line.split(',')

		#team1 acts
		if columns[1]:
			if columns[1].find('Start') >= 0:
				find_starting_comp(lines, i, team_comps, team1, team2)
				set_comp_type(team_comps, team1, player_positions, player_misses)
				set_comp_type(team_comps, team2, player_positions, player_misses)

			extract_payoff(team1, team2, victorious, columns[1], team_comps, data, player_positions, player_misses)

		#team2 acts
		if columns[5] and columns[5] != '\n':
			extract_payoff(team2, team1, victorious, columns[5], team_comps, data, player_positions, player_misses)

#		search_team_action(columns, team_comps, data, team1, team2, victorious, player_position, player_misses)

def build_data_dict():
	data = {
		'even': {
			'victory': [],
			'defeat': []
		},
		'one-sided': {
			'victory': [],
			'defeat': []
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

def print_data(data):
	for gameType in data:
		for result in data[gameType]:
			for strat1 in Strats:
				for strat2 in Strats:
					print(gameType, result, strat1, strat2)
					print(data[gameType][result][strat1.value][strat2.value].try_2)
					print(data[gameType][result][strat1.value][strat2.value].hit_2)
					print(data[gameType][result][strat1.value][strat2.value].try_3)
					print(data[gameType][result][strat1.value][strat2.value].hit_3)
					print('=======================================================')
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

data = build_data_dict()

# for d in dirs:

# 	cod = os.fsencode(d)
	
# 	for i, file in enumerate(os.listdir(cod)):
# 		# if d == evenDir:
# 		# 	read_file(path, data['even'])
# 		# else:
# 		# 	read_file(path, data['one-sided'])
		
# 		filename = os.fsdecode(file)

# 		path = d+filename

# 		f = open(path, 'r')

# 		team_comps = {}

# 		print(filename)

# 		first_read(f, team_comps)

# 		second_read(f, team_comps, data)


filename = 'data/raw/2018/201710170CLE.txt'
f = open(filename, 'r')
team_comps = {}
first_read(f, team_comps)
f.seek(0)
second_read(f, team_comps, data['even'])

print_data(data)