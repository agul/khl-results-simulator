#!/usr/bin/python3

import copy
import operator
from functools import reduce


class Score(list):
	SIZE = 6
	POINTS = [2, 2, 2, 1, 1, 0]

	def __init__(self):
		super().__init__([0 for i in range(self.SIZE)])

	def __init__(self, values=[0 for i in range(SIZE)]):
		super().__init__(values)

	@classmethod
	def size(cls):
		return cls.SIZE

	def inversed(self):
		inversed = copy.deepcopy(self)
		inversed.reverse()
		return inversed

	def points(self):
		return sum(reduce(operator.mul, data) for data in zip(self, self.POINTS))

	def append_result(self, score):
		for i in range(self.SIZE):
			self[i] += score[i]
