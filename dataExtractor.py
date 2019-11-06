# 0 = time
# 1 = team1 (event)
# 2 = pointsAway (scored in this event)
# 3 = score
# 4 = pointsHome (scored in this event)
# 5 = team2 (event)

import os
import json

def reset_game_stats(dic):
	teams = ['team1', 'team2']
	for team in teams:
		dic[team]['num_throws_2'] = 0
		dic[team]['num_score_2'] = 0
		dic[team]['num_throws_3'] = 0
		dic[team]['num_score_3'] = 0
		dic[team]['rate_2'] = 0
		dic[team]['rate_3'] = 0
		dic[team]['final_score'] = 0

		dic[team]['num_throws_2'] = 0
		dic[team]['num_score_2'] = 0
		dic[team]['num_throws_3'] = 0
		dic[team]['num_score_3'] = 0
		dic[team]['rate_2'] = 0
		dic[team]['rate_3'] = 0
		dic[team]['final_score'] = 0

def read_team_action(team, columns):

	if team == 'team1':
		team_col = 1
	elif team == 'team2':
		team_col = 5

	if columns[team_col].find('misses') > 0:

		if columns[team_col].find('2-pt') > 0:
			gameStats[team]['num_throws_2'] += 1

		elif columns[team_col].find('3-pt') > 0:
			gameStats[team]['num_throws_3'] += 1

	elif columns[team_col].find('makes') > 0:

		if columns[team_col].find('2-pt') > 0:
			gameStats[team]['num_throws_2'] += 1
			gameStats[team]['num_score_2'] += 1
			gameStats[team]['final_score'] += 2

		elif columns[team_col].find('3-pt') > 0:
			gameStats[team]['num_throws_3'] += 1
			gameStats[team]['num_score_3'] += 1
			gameStats[team]['final_score'] += 3

		elif columns[team_col].find('free') > 0:
			gameStats[team]['final_score'] += 1

def read_line(line, i, results):
	columns = line.split(',')

	#game start line
	if i == 0:
		team1 = columns[1]
		team2 = columns[5]
		results.write(team1 + ' x ' + team2)

	#team1 throws
	elif columns[1]:
		read_team_action('team1', columns)

	#team2 throws
	elif columns[5] and columns[5] != '\n':
		read_team_action('team2', columns)

def read_file(path, results):
	f = open(path, 'r')

	for i, line in enumerate(f):
		read_line(line, i, results)

################################################################################
################################################################################
################################################################################
################################################################################

gameStats = {
	'team1': {},
	'team2': {}
}

reset_game_stats(gameStats)

evenDir = 'data/splitted/even/'
evenDirCod = os.fsencode(evenDir)
evenResultsFile = open('results/evenGames.txt', 'w')

oneDir = 'data/splitted/one_sided/'
oneDirCod = os.fsencode(oneDir)
oneResultsFile = open('results/oneGames.txt', 'w')

dirs = [evenDir, oneDir]

for d in dirs:

	cod = os.fsencode(d)
	
	if d == evenDir:
		resultFilePath = 'results/evenGames.txt'
	else:
		resultFilePath = 'results/oneGames.txt'

	results = open(resultFilePath, 'w')
	
	for i, file in enumerate(os.listdir(cod)):
		
		filename = os.fsdecode(file)

		path = d+filename

		results.write(path + '\n')
		
		reset_game_stats(gameStats)
		read_file(path, results)

		results.write(json.dumps(gameStats))
		results.write('\n\n')

	results.close()

