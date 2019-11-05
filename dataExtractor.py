# 0 = time
# 1 = team1 (event)
# 2 = pointsAway (scored in this event)
# 3 = score
# 4 = pointsHome (scored in this event)
# 5 = team2 (event)

import os

balancedDir = 'data/splitted/balanced/'
balancedDirCod = os.fsencode(balancedDir)

for i, file in enumerate(os.listdir(balancedDirCod)):
	filename = os.fsdecode(file)

	print(filename)

	score = [0,0]
	at2_attempt = 0
	at2_success = 0
	at2_rate = 0
	at3_attempt = 0
	at3_success = 0
	at3_rate = 0

	with open (balancedDir + filename, 'r') as f:

		for i, line in enumerate(f):

			columns = line.split(',')

			#game start
			if i == 0:
				team1 = columns[1]
				team2 = columns[5]
				print(team1, 'x', team2[:-1])
				continue

			#quarter start and jump ball
			elif columns[1] and (columns[5] and columns[5] != '\n'):
				continue

			elif columns[1]:
				if columns[1].find('misses') > 0:
					if columns[1].find('2-pt') > 0:
						at2_attempt += 1
					elif columns[1].find('3-pt') > 0:
						at3_attempt += 1

				elif columns[1].find('makes') > 0:
					if columns[1].find('2-pt') > 0:
						at2_attempt += 1
						at2_success += 1
						score[0] += 2
					elif columns[1].find('3-pt') > 0:
						at3_attempt += 1
						at3_success += 1
						score[0] += 3
					elif columns[1].find('free') > 0:
						score[0] += 1

			elif columns[5] and columns[5] != '\n':

				if columns[5].find('misses') > 0:
					if columns[5].find('2-pt') > 0:
						at2_attempt += 1
					elif columns[5].find('3-pt') > 0:
						at3_attempt += 1

				elif columns[5].find('makes') > 0:
					if columns[5].find('2-pt') > 0:
						at2_attempt += 1
						at2_success += 1
						score[1] += 2
					elif columns[5].find('3-pt') > 0:
						at3_attempt += 1
						at3_success += 1
						score[1] += 3
					elif columns[5].find('free') > 0:
						score[1] += 1

		at2_rate = at2_success/at2_attempt
		at3_rate = at3_success/at3_attempt

	print(at2_rate, at3_rate, '\n')