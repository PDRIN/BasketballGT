gameStats = {
	'team1': {},
	'team2': {}
}

def reset_game_stats(d):
	teams = ['team1', 'team2']
	for team in teams:
		d[team]['num_throws_2'] = 0,
		d[team]['num_score_2'] = 0,
		d[team]['num_throws_3'] = 0,
		d[team]['num_score_3'] = 0,
		d[team]['rate_2'] = 0,
		d[team]['rate_3'] = 0,
		d[team]['final_score'] = 0,

		d[team]['num_throws_2'] = 0,
		d[team]['num_score_2'] = 0,
		d[team]['num_throws_3'] = 0,
		d[team]['num_score_3'] = 0,
		d[team]['rate_2'] = 0,
		d[team]['rate_3'] = 0,
		d[team]['final_score'] = 0

reset_game_stats(gameStats)
print(gameStats)