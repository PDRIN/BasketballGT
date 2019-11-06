import os
import json

def printTeamsDict(d, out):
	for key in d:
		out.write(key + ':')
		for player in d[key]:
			out.write(player + ',')
		out.write('\n')

def removeNewLine(string):
	if string[-1] == '\n':
		return string[:-1]
	else:
		return string

def appendIfNotExist(array, item):
	trueItem = removeNewLine(item)
	if trueItem not in array:
		array.append(trueItem)

def findPlayers(teamName,  action):
	words = action.split(' ')

	if (action.find('misses') > 0) or (action.find('makes') > 0):
		appendIfNotExist(teams[teamName], words[0] + ' ' + words[1])

	elif action.find('enters') > 0:
		appendIfNotExist(teams[teamName], words[0] + ' ' + words[1])
		appendIfNotExist(teams[teamName], words[6] + ' ' + words[7])

def addKeytoDict(d, key):
	if key not in d.keys():
		d[key] = []

def read_line(columns, team1, team2):
	#team1 acts
	if columns[1]:
		findPlayers(team1, columns[1])

	#team2 acts
	elif columns[5] and columns[5] != '\n':
		findPlayers(team2, columns[5])

def read_file(path):
	f = open(path, 'r')

	team1 = ''
	team2 = ''

	for i, line in enumerate(f):

		columns = line.split(',')

		if i == 0:
			team1 = columns[1]
			team2 = columns[5][:-1]
			addKeytoDict(teams, team1)
			addKeytoDict(teams, team2)

		elif i == 1 or i == 2:
			continue

		else:
			read_line(columns, team1, team2)

teams = {}

direc = 'data/raw/2018/'
codDirec = os.fsencode(direc)

outFileName = 'playerByTeam.txt'
outF = open(outFileName, 'w')

for i, file in enumerate(os.listdir(codDirec)):

	filename = os.fsdecode(file)

	path = direc+filename
	
	read_file(path)

# file = direc + '201710200CHO.txt'

# read_file(file, outFileName)

printTeamsDict(teams, outF)