import os
import json
import pandas as pd

def convert_names(name):
	names = name.split(' ')
	names[0] = (names[0][0] + '.')
	new_name = ' '.join(names)

	return new_name


data = pd.read_csv("data/player_data.csv")

data = data[['name', 'year_end', 'position']]
data = data.loc[data['year_end'] > 2016]

data['name'] = data['name'].apply(convert_names)

print(data)