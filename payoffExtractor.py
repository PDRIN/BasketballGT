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
		self.acc_2 = 0
		self.acc_3 = 0

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

	if truePlayerIn in comp['players'] and truePlayerOut in comp['players']:
		return

	# print(comp)
	# print('In <<<<', truePlayerIn)
	# print('Out >>>>', truePlayerOut)

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

	else:
		comp[team]['type'] = Strats.THREE


def find_starting_comp(lines, starting_line, team_comps, team1, team2, positions, misses):
	#players that have entered via substitution are stored in these 2 lists, so they dont
	#get counted in the starting comp
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
			set_comp_type(team_comps, team1, positions, misses)
			set_comp_type(team_comps, team2, positions, misses)
			break

def get_team_names(line):
	columns = line.split(',')
	team1 = columns[1]
	team2 = columns[5][:-1]

	return team1, team2

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

def extract_line_data(team, other_team, action, team_comps, game_type_data, positions, misses):
	words = action.split(' ')

	#this section is in charge of substitutions
	if action.find('enters') > 0:	
		player_in = words[0] + ' ' + words[1]

		#Mbah and Lemon are 2 players whose names do not follow the pattern, for some reason
		#That's why they have to be handled separately
		if words[1] == 'Mbah':
			player_out = words[8] + ' ' + words[9]

		elif words[1] == 'Lemon':
			player_out = words[7] + ' ' + words[8]

		else:
			player_out = words[6] + ' ' + words[7]
		
		change_player(team_comps[team], player_out, player_in)

		set_comp_type(team_comps, team, positions, misses)

		return

	if team_comps[team]['type'] == None:
		set_comp_type(team_comps, team, positions, misses)
	if team_comps[other_team]['type'] == None:
		set_comp_type(team_comps, other_team, positions, misses)

	team_strat = team_comps[team]['type'].value
	other_team_strat = team_comps[other_team]['type'].value

	cell = game_type_data[team_strat][other_team_strat]

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

''' 
The main function. It reads the file, searching for the starting comp in the beggining of
each quarter (find_starting_comp) and searchs for relevant events: scores and substitutions (extract_line_data).
Parameters:
file = game file already opened as 'read only'
team_comps = empty dictionary (team_comps = {})
data = custom structured dictionary, will be used to store game stats (irrelevant for formation management)
'''
def get_game_data(file, team_comps, data):
	player_position_file = open('results/player_team_position.txt')
	player_positions = json.load(player_position_file)

	#a miss file was manually created to fill misses in the dataset used to get player positions
	player_position_miss_file = open('results/player_team_position_misses.txt')
	player_misses = json.load(player_position_miss_file)

	lines = file.readlines()
	
	team1, team2 = get_team_names(lines[0])

	find_starting_comp(lines, 0, team_comps, team1, team2, player_positions, player_misses)

	for i, line in enumerate(lines):

		columns = line.split(',')

		#team1 acts
		if columns[1]:
			if columns[1].find('Start') >= 0:
				find_starting_comp(lines, i, team_comps, team1, team2, player_positions, player_misses)

			extract_line_data(team1, team2, columns[1], team_comps, data, player_positions, player_misses)

		#team2 acts
		if columns[5] and columns[5] != '\n':
			extract_line_data(team2, team1, columns[5], team_comps, data, player_positions, player_misses)

def build_data_dict():
	data = {
		'even': [],
		'one-sided': []
	}

	for gameType in data:
		for strat1 in Strats:
			data[gameType].append([])
			for strat2 in Strats:
				data[gameType][strat1.value].append([])
				data[gameType][strat1.value][strat2.value] = Stats()

	return data

def calculate_data_acc(data):
	for gameType in data:
		for strat1 in Strats:
			for strat2 in Strats:
				stats = data[gameType][strat1.value][strat2.value]
				if stats.try_2 != 0:
					stats.acc_2 = stats.hit_2/stats.try_2
				if stats.try_3 != 0:
					stats.acc_3 = stats.hit_3/stats.try_3

def print_data(data, f):
	for gameType in data:
		for strat1 in Strats:
			for strat2 in Strats:
				stats = data[gameType][strat1.value][strat2.value]
				f.write(gameType + ' ' + strat1.name + ' ' + strat2.name + '\n')
				f.write(str(stats.try_2)  + ' ' +  str(stats.hit_2)  + ' ' + str(stats.acc_2) + '\n')
				f.write(str(stats.try_3)  + ' ' +  str(stats.hit_3)  + ' ' + str(stats.acc_3) + '\n\n')

def create_payoff():
	payoff_m = []
	for strat1 in Strats:
		payoff_m.append([])
		for strat2 in Strats:
			payoff_m[strat1.value].append([])

	return payoff_m

def calculate_payoff(data):
	payoff_m = create_payoff()

	for strat1 in Strats:
		for strat2 in Strats:
			cell = data[strat1.value][strat2.value]
			total_throws = cell.try_2 + cell.try_3
			total_points = (cell.hit_2 * 2) + (cell.hit_3 * 3)
			payoff = total_points / total_throws
			payoff_m[strat1.value][strat2.value] = payoff

	return payoff_m

def calculate_strat_usage(data):
	total_times_used = [0,0,0]
	even_times_used = [0,0,0]
	one_times_used = [0,0,0]

	total_confronts = 0
	even_confronts = 0
	one_confronts = 0

	for gameType in data:
		for strat1 in Strats:
			for strat2 in Strats:
				cell = data[gameType][strat1.value][strat2.value]

				total_confronts += cell.try_2 + cell.try_3
				total_times_used[strat1.value] += cell.try_2 + cell.try_3

				if gameType == 'even':
					even_confronts += cell.try_2 + cell.try_3
					even_times_used[strat1.value] += cell.try_2 + cell.try_3

				elif gameType == 'one-sided':
					one_confronts += cell.try_2 + cell.try_3
					one_times_used[strat1.value] += cell.try_2 + cell.try_3


	for strat in Strats:
		total_times_used[strat.value] /= total_confronts
		even_times_used[strat.value] /= even_confronts
		one_times_used[strat.value] /= one_confronts	

	return total_times_used, even_times_used, one_times_used

def calculate_shot_chances(data):
	shot_chances = []

	for strat1 in Strats:
		shot_chances.append([])
		for strat2 in Strats:
			shot_chances[strat1.value].append([])
			shot_chances[strat1.value][strat2.value] = {}

			shot_cell = shot_chances[strat1.value][strat2.value]
			data_cell = data[strat1.value][strat2.value]

			chance_2 = data_cell.try_2/(data_cell.try_2 + data_cell.try_3)
			chance_3 = data_cell.try_3/(data_cell.try_2 + data_cell.try_3)

			shot_cell['chance_2'] = chance_2
			shot_cell['chance_3'] = chance_3
			shot_cell['acc_2'] = data_cell.acc_2
			shot_cell['acc_3'] = data_cell.acc_3

	return shot_chances

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

ignore_files = [
	'201710200PHI.txt',
	'201710240ORL.txt',
	'201710250PHI.txt',
	'201710280MEM.txt',
	'201712230IND.txt',
	'201801280HOU.txt',
	'201802060BRK.txt',
	'201802090DET.txt',
	'201803150DEN.txt',
	'201805020HOU.txt'
]

for d in dirs:

	cod = os.fsencode(d)
	
	for i, file in enumerate(os.listdir(cod)):
		filename = os.fsdecode(file)
		path = d+filename

		if filename in ignore_files:
			continue

		f = open(path, 'r')

		team_comps = {}

		if d == evenDir:
			get_game_data(f, team_comps, data['even'])
		else:
			get_game_data(f, team_comps, data['one-sided'])

calculate_data_acc(data)

data_filename = 'results/result_data.txt'
data_f = open(data_filename, 'w')
print_data(data, data_f)

results = {
	'payoffs': {},
	'strat-usage': {
		'total': [],
		'even': [],
		'one-sided': []
	},
	'shot_chances': {}
}

results['payoffs']['even'] = calculate_payoff(data['even'])
results['payoffs']['one-sided'] = calculate_payoff(data['one-sided'])

results['strat-usage']['total'], results['strat-usage']['even'], results['strat-usage']['one-sided'] = calculate_strat_usage(data)

results['shot_chances']['even'] = calculate_shot_chances(data['even'])
results['shot_chances']['one-sided'] = calculate_shot_chances(data['one-sided'])

results_filename = 'results/results.txt'
results_f = open(results_filename, 'w')
results_f.write(json.dumps(results, indent=2))