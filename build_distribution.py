#!/usr/bin/python3

import json
import sys

from collections import defaultdict
from teams import TEAMS
from teams import TeamsPair

FILES = [
	# "processed/2016-2017.json",
	# "processed/2017-2018.json",
	"processed/2018-2019.json",
	"processed/2019-2020.json",
	"processed/2020-2021.json",
]


if __name__ == "__main__":
	distribution = dict()

	for filename in FILES:
		with open(filename, "r") as f:
			season_results = json.load(f)

		for match in season_results:
			home = match["home"]
			away = match["away"]
			winner = home if match["home_score"] > match["away_score"] else away
			
			pair = TeamsPair.get_pair_code(home, away)
			if pair not in distribution:
				distribution[pair] = TeamsPair(pair)
			distribution[pair].add_winner(winner, match["ot"], match["so"])

	distribution_json = dict()
	for key, value in distribution.items():
		distribution_json[key] = value.results
	print(json.dumps(distribution_json))
