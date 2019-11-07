import os
import json

def printTeamsDict(d, out):
	for key in d:
		out.write(key + ':')
		for player in d[key]:
			out.write(player + ',')
		out.write('\n')

def removeNoise(string):
	newString = string
	if newString[-1] == '\n':
		newString = newString[:-1]
	if newString[0] == '\"':
		newString = newString[1:]
	
	return newString

def appendIfNotExist(array, item):
	trueItem = removeNoise(item)
	
	if trueItem not in array:
		array.append(trueItem)

def findPlayers(teamName,  action, path):
	words = action.split(' ')

	#if words[0][0] == '\"':
		#print('ADLER', action, path)

	if (action.find('misses') > 0) or (action.find('makes') > 0):
		appendIfNotExist(teams[teamName], words[0] + ' ' + words[1])

	elif action.find('enters') > 0:
		appendIfNotExist(teams[teamName], words[0] + ' ' + words[1])
		
		if words[1] == 'Mbah':
			appendIfNotExist(teams[teamName], words[8] + ' ' + words[9])
		elif words[1] == 'Lemon':
			appendIfNotExist(teams[teamName], words[7] + ' ' + words[8])
		else:
			appendIfNotExist(teams[teamName], words[6] + ' ' + words[7])

def addKeytoDict(d, key):
	if key not in d.keys():
		d[key] = []

def read_line(columns, team1, team2, path):
	#team1 acts
	if columns[1]:
		findPlayers(team1, columns[1],path)

	#team2 acts
	elif columns[5] and columns[5] != '\n':
		findPlayers(team2, columns[5],path)

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
			read_line(columns, team1, team2,path)

teams = {}

direc = 'data/raw/2018/'
codDirec = os.fsencode(direc)

outFileName = 'results/playerByTeam.txt'
outF = open(outFileName, 'w')

for i, file in enumerate(os.listdir(codDirec)):

	filename = os.fsdecode(file)

	path = direc+filename
	
	read_file(path)

# file = direc + '201710200CHO.txt'

# read_file(file, outFileName)

printTeamsDict(teams, outF)