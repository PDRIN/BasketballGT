#separate one-sided games from balanced games in two directories

import os
import shutil

threshold = 30

srcDirectory = 'data/raw/2018/'
srcDirectoryCod = os.fsencode(srcDirectory)

dstDirectory = 'data/splitted/'


for i, file in enumerate(os.listdir(srcDirectoryCod)):
	filename = os.fsdecode(file)

	print(filename)

	with open (srcDirectory + filename, 'r') as f:
		lines = f.read().splitlines()
		lastline = lines[-1]
		columns = lastline.split(',')
		score = columns[3]

		s = score.split('-')

		print(s)

		if abs(int(s[0]) - int(s[1])) >= threshold:
			shutil.copy(srcDirectory + filename, dstDirectory + 'one_sided/' + filename)
		else:
			shutil.copy(srcDirectory + filename, dstDirectory + 'balanced/' + filename)

print(i+1)