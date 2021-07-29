#!/usr/bin/python

import json
import sys

from teams import TEAMS


if __name__ == "__main__":
	if (len(sys.argv) < 2):
		print("Usage: {} <json-results-from-icehockey24>".format(sys.argv[0]))
		sys.exit(0)

	with open(sys.argv[1], "r") as f:
		season_results = json.load(f)

	all_teams = set()
	for match in season_results:
		all_teams.add(match["home"])
		all_teams.add(match["away"])

	fail = False
	for team in all_teams:
		if team not in TEAMS:
			print("\"{}\": \"\",".format(team), file=sys.stderr)
			fail = True
	if fail:
		sys.exit(1)

	for match in season_results:
		match["home"] = TEAMS.get(match["home"])
		match["away"] = TEAMS.get(match["away"])

	print(json.dumps(season_results))
