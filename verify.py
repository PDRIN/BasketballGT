file = open('data/2018/201710170GSW.txt', 'r')

points2 = 0
points3 = 0
tech = 0
free = 0

for i,line in enumerate(file):
	if line.find(',2,') and line.find('makes 2')==0:
		print(i+1)