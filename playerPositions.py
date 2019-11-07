import os
import json
import pandas as pd

def convert_names(name):
	names = name.split(' ')
	names[0] = (names[0][0] + '.')
	new_name = ' '.join(names)

	return new_name

def read_line(line, teams):
	tokens = line.split(':')
	teamName = tokens[0]
	players = tokens[1].split(',')[:-1]
	teams[teamName] = players

def read_file(path):
	teams = {}
	f = open(path, 'r')

	for i, line in enumerate(f):
		read_line(line, teams)

	return teams

def linkPlayerPosition(playerPosition, teams, teamPlayerPosition):
	for team in teams:
		for player in teams[team]:
			pass
data = pd.read_csv("data/player_data.csv")

data = data.loc[data['year_end'] > 2016]
data = data[['name', 'position', 'year_end']]

smallname = data['name'].apply(convert_names)

data['smallname'] = smallname

data.to_csv('data/player_data_mod.csv')


teamPlayerPosition = {}

playersPath = 'results/playerByTeam.txt'
outF = open('results/player_team_position.txt', 'w')
teams = read_file(playersPath)

linkPlayerPosition(data, teams, teamPlayerPosition)


