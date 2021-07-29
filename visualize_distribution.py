#!/usr/bin/python3

import json
import sys

from collections import defaultdict
from teams import TEAMS
from teams import TeamsPair


WESTERN_CONFERENCE = ["CSK", "SKA", "TOR", "JOK", "SEV", "SPA", "SOC", "VIT", "DMS", "DRG", "DMN", "LOK"]
EASTERN_CONFERENCE = ["AKB", "AVG", "MMG", "SAL", "TRA", "BAR", "AVT", "ADM", "SIB", "AMR", "NEF", "KUN"]
KHL = list(sorted(WESTERN_CONFERENCE + EASTERN_CONFERENCE))


if __name__ == "__main__":
	if (len(sys.argv) < 2):
		print("Usage: {} <results-distribution>".format(sys.argv[0]))
		sys.exit(0)

	results_distribution_filename = sys.argv[1]

	distribution = {}
	with open(results_distribution_filename, "r") as f:
		results_distribution = json.load(f)
		for pair, results in results_distribution.items():
			distribution[pair] = TeamsPair(pair).load_results(results)


	expected_points = []
	team_index = {}

	for index, team in enumerate(KHL):
		team_index[team] = index
		expected_points.append([0 for i in range(len(KHL))])


	for pair_code, pair in distribution.items():
		if pair.A not in KHL or pair.B not in KHL:
			continue
		a = team_index[pair.A]
		b = team_index[pair.B]

		total = sum(pair.results)
		for index in range(len(pair.results)):
			pair.results[index] /= float(total)

		expected_points[a][b] = pair.results.points()
		expected_points[b][a] = pair.results.inversed().points()

	print(KHL)
	print(expected_points)

