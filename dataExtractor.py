# 0 = time
# 1 = team1 (event)
# 2 = pointsAway (scored in this event)
# 3 = score
# 4 = pointsHome (scored in this event)
# 5 = team2 (event)

file = open('data/2018/201710170CLE.txt', 'r')

lines_proccessed = 0
score = [0,0]


at2_attempt = 0
at2_success = 0
at3_attempt = 0
at3_success = 0

for i, line in enumerate(file):

	columns = line.split(',')

	#game start
	if i == 0:
		lines_proccessed += 1
		team1 = columns[1]
		team2 = columns[5]
		print(team1, team2)
		continue

	#quarter start and jump ball
	elif columns[1] and (columns[5] and columns[5] != '\n'):
		lines_proccessed += 1
		continue

	elif columns[1]:
		if columns[1].find('misses') > 0:
			if columns[1].find('2-pt') > 0:
				at2_attempt += 1
				lines_proccessed+=1
			elif columns[1].find('3-pt') > 0:
				at3_attempt += 1
				lines_proccessed+=1
			elif columns[1].find('free') > 0:
				lines_proccessed+=1

		elif columns[1].find('makes') > 0:
			if columns[1].find('2-pt') > 0:
				at2_attempt += 1
				at2_success += 1
				lines_proccessed+=1
				score[0] += 2
			elif columns[1].find('3-pt') > 0:
				at3_attempt += 1
				at3_success += 1
				lines_proccessed+=1
				score[0] += 3
			elif columns[1].find('free') > 0:
				lines_proccessed+=1
				score[0] += 1

	elif columns[5] and columns[5] != '\n':

		if columns[5].find('misses') > 0:
			if columns[5].find('2-pt') > 0:
				at2_attempt += 1
				lines_proccessed+=1
			elif columns[5].find('3-pt') > 0:
				at3_attempt += 1
				lines_proccessed+=1
			elif columns[5].find('free') > 0:
				lines_proccessed+=1

		elif columns[5].find('makes') > 0:
			if columns[5].find('2-pt') > 0:
				at2_attempt += 1
				at2_success += 1
				lines_proccessed+=1
				score[1] += 2
			elif columns[5].find('3-pt') > 0:
				at3_attempt += 1
				at3_success += 1
				lines_proccessed+=1
				score[1] += 3
			elif columns[5].find('free') > 0:
				lines_proccessed+=1
				score[1] += 1

print('lines_proccessed = ', lines_proccessed)
print(score, at2_attempt, at2_success, at3_attempt, at3_success)