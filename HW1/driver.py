#!/usr/bin/python

import sys
import math
import time
from resource import getrusage
import copy

from collections import deque
import queue


class State:
	def __init__(self, current, previous = None, move = None, depth = 0):
		self.current = current
		self.previous = previous
		self.move = move
		self.depth = depth
		self.zero_row = self.current.index(0)[0]  # Need to figure out what this returns, make this index a list of 2 elements (row, column)
		self.zero_column = self.current.index(0)[1]
		self.size = math.sqrt(len(self.current))

	def __str__(self):
		return(str(self.current))

	def is_goalstate(self):
		for i in range(self.size):
			for j in range(self.size):
				if self.current[i][j] != i*self.size + j
					return False
		return True

	def available_move(self):
		"""
		Return a list of legitimate moves
		"""
		moves = []
		if self.zero_row > 0:
			moves.append('U')
		if self.zero_row < self.size - 1:
			moves.append('D')
		if self.zero_column > 0:
			moves.append('L')
		if self.zero_column < self.size - 1:
			moves.append('R')
		return moves

	def make_move(self,move):
		"""
		Change the board according to a move
		"""
		if move == "U":
			self.current[self.zero_row][self.zero_column] = self.current[self.zero_row-1][self.zero_column]
			self.current[self.zero_row-1][self.zero_column] = 0
			self.zero_row -= 1
		elif move == "D":
			self.current[self.zero_row][self.zero_column] = self.current[self.zero_row+1][self.zero_column]
			self.current[self.zero_row+1][self.zero_column] = 0
			self.zero_row += 1
		elif move == "L":
			self.current[self.zero_row][self.zero_column] = self.current[self.zero_row][self.zero_column-1]
			self.current[self.zero_row][self.zero_column-1] = 0
			self.zero_column -= 1
		elif move == "R":
			self.current[self.zero_row][self.zero_column] = self.current[self.zero_row][self.zero_column+1]
			self.current[self.zero_row][self.zero_column+1] = 0
			self.zero_column += 1

	def get_successors(self):
		"""
		Return a list of states that are the result of making actions. (Do not really make the move.)
		"""
		moves = self.available_move()
		successors = []
		for move in moves:
			temp_board = self.current[:] # Want to create a shallow copy of the current board, need to check!!
			if move == "U":
				temp_board[self.zero_row][self.zero_column] = self.current[self.zero_row-1][self.zero_column]
				temp_board[self.zero_row-1][self.zero_column] = 0
				successors.append(State(temp_board, self, move, self.depth + 1))
			elif move == "D":
				temp_board[self.zero_row][self.zero_column] = self.current[self.zero_row+1][self.zero_column]
				temp_board[self.zero_row+1][self.zero_column] = 0
				successors.append(State(temp_board, self, move, self.depth + 1))
			elif move == "L":
				temp_board[self.zero_row][self.zero_column] = self.current[self.zero_row][self.zero_column-1]
				temp_board[self.zero_row][self.zero_column-1] = 0
				successors.append(State(temp_board, self, move, self.depth + 1))
			elif move == "R":
				temp_board[self.zero_row][self.zero_column] = self.current[self.zero_row][self.zero_column+1]
				temp_board[self.zero_row][self.zero_column+1] = 0
				successors.append(State(temp_board, self, move, self.depth + 1))
		return successors



class Solver:
	"""
	The Solver class contains methods that implements the search algorithms and 
	variables that record some key information regarding each algorithm.
	"""
	def __init__(self):
		self.nodes_expanded = 0
		self.fringe_size = 1
		self.max_fringe_size = 1
		self.path = []
		self.search_depth = 0
		self.max_search_depth = 0
		self.run_time = 0
		self.ram_usage = 0

	def bfs(self, init_state):
		"""
		Implements Breath-First Search
		"""
		start_time = time.time()
		frontier = queue.Queue()
		frontier.put(init_state)
		explored = set()

		# 
		while frontier.qsize() != 0:
			cur_state = frontier.get()
			explored.add(cur_state)
			self.fringe_size -= 1
			if cur_state.is_goalstate():
				temp_state = cur_state
				temp_path = []
				while temp_state.previous != None:
					temp_path.append(temp_state.move)
					temp_state = temp_state.previous
				self.path = temp_path.reverse()
				self.search_depth = cur_state.depth
				self.run_time = time.time() - start_time

		#
			children = cur_state.get_successors()
			self.nodes_expanded += 1
			for child in children:
				child.depth = cur_state.depth + 1
				if child not in explored:
					frontier.put(child)
					explored.add(child)
					self.fringe_size += 1
					if child.depth > self.max_search_depth:
						self.max_search_depth = child.depth
					if self.fringe_size > self.max_fringe_size:
						self.max_fringe_size self.fringe_size
			ram_temp = getrusage(RUSAGE_SELF).ru_maxrss
			if ram_temp > self.ram_usage:
				self.ram_usage = ram_temp


	def dfs(self, init_state):
		"""
		Implements Depth-First Search
		"""
		start_time = time.time()
		frontier = []
		frontier.append(init_state)
		explored = set()

		# 
		while frontier.qsize() != 0:
			cur_state = frontier.pop()
			explored.add(cur_state)
			self.fringe_size -= 1
			if cur_state.is_goalstate():
				temp_state = cur_state
				temp_path = []
				while temp_state.previous != None:
					temp_path.append(temp_state.move)
					temp_state = temp_state.previous
				self.path = temp_path.reverse()
				self.search_depth = cur_state.depth
				self.run_time = time.time() - start_time

		#
			children = cur_state.get_successors()
			self.nodes_expanded += 1
			children.reverse()
			for child in children:
				child.depth = cur_state.depth + 1
				if child not in explored:
					frontier.append(child)
					explored.add(child)
					self.fringe_size += 1
					if child.depth > self.max_search_depth:
						self.max_search_depth = child.depth
					if self.fringe_size > self.max_fringe_size:
						self.max_fringe_size self.fringe_size
			ram_temp = getrusage(RUSAGE_SELF).ru_maxrss
			if ram_temp > self.ram_usage:
				self.ram_usage = ram_temp




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


