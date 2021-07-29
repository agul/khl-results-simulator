#!/usr/bin/python3

import json
import random
import sys

from score import Score
from teams import TEAMS
from teams import TeamsPair


ITERATIONS_COUNT = 100000
EASTERN_CONFERENCE = ["AKB", "AVG", "MMG", "SAL", "TRA", "BAR", "AVT", "ADM", "SIB", "AMR", "NEF", "KUN"]


class Standings:
	def __init__(self):
		self.results = {}
		for team in TEAMS.values():
			self.results[team] = Score()

	def register_match(self, home, away, results):
		self.results[home].append_result(results)
		self.results[away].append_result(list(reversed(results)))

	def build_standings(self, teams):
		standings = []
		for team in teams:
			score = self.results[team]
			standings.append((score.points(), score, team))
		standings.sort(reverse=True)

		# for points, score, team in standings:
		# 	print("{} {} {}".format(team, json.dumps(score), points))

		return standings

	def find_team_rank(self, teams_list, team):
		standings = self.build_standings(teams_list)
		for index, row in enumerate(standings):
			if row[2] == team:
				return index, *row


if __name__ == "__main__":
	if (len(sys.argv) < 3):
		print("Usage: {} <results-distribution> <calendar>".format(sys.argv[0]))
		sys.exit(0)

	random.seed(19621031)  # first match of HC Sibir

	results_distribution_filename = sys.argv[1]
	calendar_filename = sys.argv[2]

	distribution = {}
	with open(results_distribution_filename, "r") as f:
		results_distribution = json.load(f)
		for pair, results in results_distribution.items():
			distribution[pair] = TeamsPair(pair).load_results(results)


	with open(calendar_filename, "r") as f:
		calendar = json.load(f)

	accumulated_standings = Standings()
	matches_accumulated_results = [Score() for i in range(len(calendar))]
	sibir_ranks_in_conference = []
	sibir_points = []
	for iter in range(ITERATIONS_COUNT):
		if iter % 1000 == 0:
			print("Iteration {}".format(iter), file=sys.stderr)
		standings = Standings()

		for index, match in enumerate(calendar):
			home = match["home"]
			away = match["away"]

			pair = TeamsPair.get_pair_code(home, away)
			prediction = distribution[pair].get_prediction(home, away)

			standings.register_match(home, away, prediction)
			accumulated_standings.register_match(home, away, prediction)
			matches_accumulated_results[index].append_result(prediction)

		# regular_season_predicted_results = standings.build_standings(EASTERN_CONFERENCE)
		rank = standings.find_team_rank(EASTERN_CONFERENCE, "SIB")
		sibir_ranks_in_conference.append(rank[0] + 1)
		sibir_points.append(rank[1])

	print(sibir_ranks_in_conference)
	print(sibir_points)

	print("Expected rank: {}".format(sum(sibir_ranks_in_conference) / float(ITERATIONS_COUNT)))

	expected_rank = accumulated_standings.find_team_rank(EASTERN_CONFERENCE, "SIB")
	expected_points = expected_rank[1] / float(ITERATIONS_COUNT)
	print("Expected points: {}".format(expected_points))

	expected_score = list(expected_rank[2])
	for index in range(Score.size()):
		expected_score[index] /= float(ITERATIONS_COUNT)
	print("Expected rank: ", expected_score)

	expected_standings = accumulated_standings.build_standings(EASTERN_CONFERENCE)
	for row in expected_standings:
		print(row[2], row[0] / float(ITERATIONS_COUNT))

	for index, match in enumerate(calendar):
		home = match["home"]
		away = match["away"]
		if "SIB" in [home, away]:
			probability = matches_accumulated_results[index]
			total = sum(probability)
			for index in range(len(probability)):
				probability[index] /= float(total)
			if away == "SIB":
				probability.reverse()
			print("{},{},{},{},{},{},{},{}".format(home, away, *probability))


