#!/usr/bin/python3

import random

from score import Score


TEAMS = {
	"Vladivostok": "ADM",
	"Admiral": "ADM",
	"Bars Kazan": "AKB",
	"Ak Bars": "AKB",
	"Amur Khabarovsk": "AMR",
	"Amur": "AMR",
	"Avangard": "AVG",
	"Avangard Omsk": "AVG",
	"Yekaterinburg": "AVT",
	"Avtomobilist": "AVT",
	"Barys Nur-Sultan": "BAR",
	"Barys": "BAR",
	"CSKA Moscow": "CSK",
	"CSKA": "CSK",
	"Din. Minsk": "DMN",
	"Dinamo Mn": "DMN",
	"Dyn. Moscow": "DMS",
	"Dynamo Msk": "DMS",
	"Dinamo Riga": "DRG",
	"Dinamo R": "DRG",
	"Jokerit": "JOK",
	"Kunlun": "KUN",
	"Kunlun RS": "KUN",
	"Lokomotiv Yaroslavl": "LOK",
	"Lokomotiv": "LOK",
	"Metallurg Magnitogorsk": "MMG",
	"Metallurg Mg": "MMG",
	"Niznekamsk": "NEF",
	"Neftekhimik": "NEF",
	"Salavat Ufa": "SAL",
	"Salavat Yulaev": "SAL",
	"Cherepovets": "SEV",
	"Severstal": "SEV",
	"Sibir Novosibirsk": "SIB",
	"Sibir": "SIB",
	"SKA St. Petersburg": "SKA",
	"SKA": "SKA",
	"Sp. Moscow": "SPA",
	"Spartak": "SPA",
	"Sochi": "SOC",
	"HC Sochi": "SOC",
	"Nizhny Novgorod": "TOR",
	"Torpedo": "TOR",
	"Tractor Chelyabinsk": "TRA",
	"Traktor": "TRA",
	"Podolsk": "VIT",
	"Vityaz": "VIT",

	"Slovan Bratislava": "SLO",
	"Lada": "LAD",
	"HC Yugra": "YUG",
	"Metallurg Novokuznetsk": "MNK",
	"Medvescak Zagreb": "MED",
}


SIB_ADJUST_PROBABILITY_COEF = 0.4


class TeamsPair:
	@staticmethod
	def get_pair_code(team_a, team_b):
		A = min(team_a, team_b)
		B = max(team_a, team_b)
		return "{}-{}".format(A, B)

	def __init__(self, pair_code):
		self.results = Score()
		self.A, self.B = pair_code.split('-')

	def load_results(self, results):
		self.results = Score(results)
		return self

	def get_prediction(self, team_a, team_b):
		total = sum(self.results)
		verdict = random.uniform(0, total - 1)

		if self.A == "SIB":
			verdict -= sum(self.results[:3]) / float(total) * SIB_ADJUST_PROBABILITY_COEF
		if self.B == "SIB":
			verdict += sum(self.results[3:]) / float(total) * SIB_ADJUST_PROBABILITY_COEF
		verdict = int(verdict + 0.5)  # round by taking floor

		prediction = Score()
		cur_sum = 0
		for i in range(prediction.size()):
			cur_sum += self.results[i]
			if cur_sum > verdict:
				prediction[i] = 1
				break


		if team_a == self.B and team_b == self.A:
			prediction.reverse()

		return prediction

	def add_winner(self, team, ot, so):
		index = 0

		if ot:
			index += 1
		elif so:
			index += 2

		if team == self.B:
			index = 5 - index

		self.results[index] += 1
