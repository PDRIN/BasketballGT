import numpy as np
from chart_studio import plotly as py
from plotly import graph_objects as go

def remove_noise(string):
	newString = string
	if newString[-1] == '\n':
		newString = newString[:-1]
	if newString[0] == '\"':
		newString = newString[1:]
	
	return newString

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

def extract_score(team, other_team, action, score):
	words = action.split(' ')

	if (action.find('misses') > 0):
		if is_2_point(words):
			score.append(0)

		elif is_3_point(words):
			score.append(0)

	if (action.find('makes') > 0):
		if is_2_point(words):
			score.append(2)

		elif is_3_point(words):
			score.append(3)

def get_scores(file):
	lines = file.readlines()
	
	team1, team2 = get_team_names(lines[0])

	score1 = [0]
	score2 = [0]

	for i, line in enumerate(lines):

		columns = line.split(',')

		#team1 acts
		if columns[1]:
			extract_score(team1, team2, columns[1], score1)

		#team2 acts
		if columns[5] and columns[5] != '\n':
			extract_score(team2, team1, columns[5], score2)

	return score1, score2

directory = 'data/splitted/'
game_type = 'one_sided/'
filename = '201710240MIN.txt'
path = directory+game_type+filename
game_file = open(path, 'r')

score1, score2 = get_scores(game_file)

print(score1)
print(score2)
print(np.cumsum(score1)[-1])
print(np.cumsum(score2)[-1])
possessions1 = np.arange(0,len(score1))
possessions2 = np.arange(0,len(score2))

trace1 = go.Scatter(
    x = possessions1,
    y = np.cumsum(score1),
    name = "Time A",
    line = {'width': 4},
    textfont = {'size': 30}
)

trace2 = go.Scatter(
    x = possessions2,
    y = np.cumsum(score2),
    name = "Time B",
    line = {'width': 4},
    textfont = {'size': 70}
)

layout = go.Layout(
    xaxis=go.layout.XAxis(
        tickfont={'size': 30},
        title='Possessions',
        titlefont={'size': 30}),
    yaxis=go.layout.YAxis(
    	tickfont={'size': 30},
        title='Score',
        titlefont={'size': 30}),
    title = 'Game Plot',
    titlefont={'size': 50},
    showlegend = False
)

data = [trace1, trace2]


value = input('Print (y == yes)? ')
if value == 'y':
	number = input('Type game number XX: ')
	
	name = game_type[:-1] + '_game_' + number + '_' + filename

	py.plot(dict(data=data, layout=layout), filename=name)