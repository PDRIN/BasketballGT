import numpy
import random

def read_data():
	filename = 'payoffs.txt'
	f = open(filename, 'r')

	lines = f.readlines()

	

possession_number = 100
strats = ['alternate', 'repeat_enemy', 'random']

for strat1 in strats:
	for strat2 in strats:
		pass