#!/usr/bin/python

import sys
import math
import copy

from collections import deque
import queue


class State:
	def __init__(self,current,move=None):
		self.current = current
		self.path = []
		self.size = math.sqrt(len(self.current))
		self.parent = None

	def __str__(self):
		return(str(self.current))

	def is_goalstate(self):
		return self.current == [0,1,2,3,4,5,6,7,8]

	def make_move(self,move):
		pos = self.current.index(0)
		if move == "U":
			if pos-3 >= 0:
				dup = copy.deepcopy(self)
				tmp = dup.current[pos]
				dup.current[pos] = dup.current[pos-3]
				dup.current[pos-3] = tmp
				return dup
		if move == "D":
			if pos+3 <= 8:
				dup = copy.deepcopy(self)
				tmp = dup.current[pos]
				dup.current[pos] = dup.current[pos+3]
				dup.current[pos+3] = tmp
				return dup
		if move == "L":
			if pos%3 != 0:
				dup = copy.deepcopy(self)
				tmp = dup.current[pos]
				dup.current[pos] = dup.current[pos-1]
				dup.current[pos-1] = tmp
				return dup
		if move == "R":
			if pos%3 != 2:
				dup = copy.deepcopy(self)
				tmp = dup.current[pos]
				dup.current[pos] = dup.current[pos+1]
				dup.current[pos+1] = tmp
				return dup

	def find_path(self):
		direct_path = []
		while self.parent:
			direct_path.append(self.path)
			self = self.parent
		return direct_path

	def solver(self,method):
		if method == 'bfs':
			self.bfs()
		if method == 'dfs':
			self.dfs()

	def bfs(self):
		frontier = queue.Queue()
		frontier.put(self)
		explored = set()

		while frontier.qsize() != 0:
			cur_state = frontier.get()
			explored.add(tuple(cur_state.current))
			if cur_state.is_goalstate():
				return cur_state.path
			for dir in ['U','D','L','R']:
				tmp = cur_state.make_move(dir)
				if tmp:
					if tuple(tmp.current) not in explored:
						frontier.put(tmp)
						tmp.path.append(dir)
						tmp.parent = cur_state
		return None

	def dfs(self):
		frontier = []
		frontier.append(self)
		explored = set()

		while len(frontier) != 0:
			cur_state = frontier.pop()
			print(cur_state)
			explored.add(tuple(cur_state.current))
			if cur_state.is_goalstate():
				return cur_state
			for dir in ['R','L','D','U']:
				tmp = cur_state.make_move(dir)
				if tmp:
					if tuple(tmp.current) not in explored or [ x.current for x in frontier]:
						frontier.append(tmp)
						tmp.path = dir
						tmp.parent = cur_state
		return None

if __name__ == "__main__":
	a = State([0,1,2,3,4,5,6,7,8])
	print(a)
	print(a.is_goalstate())
	b = a.make_move('D')
	print(b)
	print(b.bfs())




	c = State([1,2,5,3,4,0,6,7,8])
	print(c)
	# print(c.bfs())
	print(c.dfs().find_path())


