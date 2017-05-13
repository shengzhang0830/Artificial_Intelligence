#!/usr/bin/python

import sys
import math
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


	def __init__(self):
		self

	def find_path(self):
		direct_path = []
		while self.parent:
			direct_path.append(self.path)
			self = self.parent
		return direct_path

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


