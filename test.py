import pandas as pd

data = pd.read_csv("data/player_data.csv")

data = data.loc[data['year_end'] > 2016]

print(data.position.unique())