#!/usr/bin/python3

import json
import sys


if __name__ == "__main__":
	with open("processed/2020-2021.json", "r") as f:
		season_results = json.load(f)

	calendar = []
	for match in season_results:
		home = match["home"]
		away = match["away"]
		calendar.append({"home": home, "away": away})

	print(json.dumps(calendar))
