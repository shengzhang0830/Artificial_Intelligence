'''
Sheng Zhang
HW1 | Search Algorithm: N-Puzzle
'''

import sys
import math
import time
import resource
import copy
import heapq


def manhattan_distance(state):
	'''
	Calculate the manhattan distance toward the goal state
	'''
	horiz = []
	vert = []
	for i in state.current:
		if i != 0:
			horiz.append(abs(state.current.index(i)%3 - i%3))
			vert.append(abs(state.current.index(i)/3 - i/3))			
	m_dist = sum(horiz + vert)
	return m_dist


class State:
	'''
	Represent a state of the board
	'''
	def __init__(self, current, previous = None, move = None, depth = 0):
		self.current = current
		self.previous = previous
		self.move = move
		self.depth = depth
		self.size = int(math.sqrt(len(self.current)))
		self.zero_loc = self.current.index(0)

	def __str__(self):
		return(str(self.current))

	def is_goalstate(self):
		'''
		Check if the current state is the goal state
		'''
		for i in range(0, len(self.current)):
			if self.current[i] != i:
				return False
		return True

	def available_move(self):
		'''
		Return a list of legitimate moves
		'''
		moves = []
		if self.zero_loc > (self.size - 1):
			moves.append('Up')
		if self.zero_loc < (self.size * (self.size - 1)):
			moves.append('Down')
		if self.zero_loc % self.size != 0:
			moves.append('Left')
		if self.zero_loc % self.size != 2:
			moves.append('Right')
		return moves

	def make_move(self,move):
		'''
		Change the board according to a move
		'''
		if move == 'Up':
			self.current[self.zero_loc] = self.current[self.zero_loc - self.size]
			self.current[self.zero_loc - self.size] = 0
			self.zero_loc -= self.size
		elif move == 'Down':
			self.current[self.zero_loc] = self.current[self.zero_loc + self.size]
			self.current[self.zero_loc + self.size] = 0
			self.zero_loc += self.size
		elif move == 'Left':
			self.current[self.zero_loc] = self.current[self.zero_loc - 1]
			self.current[self.zero_loc - 1] = 0
			self.zero_loc -= 1
		elif move == 'Right':
			self.current[self.zero_loc] = self.current[self.zero_loc + 1]
			self.current[self.zero_loc + 1] = 0
			self.zero_loc += 1

	def get_successors(self):
		'''
		Return a list of states that are the result of making actions. (Do not really make the move.)
		'''
		moves = self.available_move()
		successors = []
		for move in moves:
			temp_board = copy.copy(self.current)  # Want to create a shallow copy of the current board
			if move == 'Up':
				temp_board[self.zero_loc] = self.current[self.zero_loc - self.size]
				temp_board[self.zero_loc - self.size] = 0
				successors.append(State(temp_board, self, move, self.depth + 1))
			elif move == 'Down':
				temp_board[self.zero_loc] = self.current[self.zero_loc + self.size]
				temp_board[self.zero_loc + self.size] = 0
				successors.append(State(temp_board, self, move, self.depth + 1))
			elif move == 'Left':
				temp_board[self.zero_loc] = self.current[self.zero_loc - 1]
				temp_board[self.zero_loc - 1] = 0
				successors.append(State(temp_board, self, move, self.depth + 1))
			elif move == 'Right':
				temp_board[self.zero_loc] = self.current[self.zero_loc + 1]
				temp_board[self.zero_loc + 1] = 0
				successors.append(State(temp_board, self, move, self.depth + 1))
		return successors

	def __repr__(self):
		return str(self.current)

	def __eq__(self, other):
		if isinstance(other, self.__class__):
			return self.current == other.current
		else:
			return False

	def __ne__(self, other):
		if isinstance(other, self.__class__):
			return self.current != other.current
		else:
			return True

	def __hash__(self):
		return hash(str(self.current))


class Queue:
	'''
	Define an efficient queue implementation, adapted from http://interactivepython.org/courselib/static/pythonds/BasicDS/ImplementingaQueueinPython.html
	'''
	def __init__(self):
		self.items = []
		self.q_set = set()

	def enqueue(self, item):
		self.items.insert(0, item)
		self.q_set.add(item)

	def dequeue(self):
		rm_item = self.items.pop()
		self.q_set.remove(rm_item)
		return rm_item

	def size(self):
		return len(self.items)


class Stack:
	'''
	Define an efficient stack implementation, adapted from http://interactivepython.org/courselib/static/pythonds/BasicDS/ImplementingaStackinPython.html
	'''
	def __init__(self):
		self.items = []
		self.s_set = set()

	def push(self, item):
		self.items.append(item)
		self.s_set.add(item)

	def pop(self):
		rm_item = self.items.pop()
		self.s_set.remove(rm_item)
		return rm_item

	def size(self):
		return len(self.items)


class Priority_Queue:
	'''
	Define an efficient priority queue implementation
	'''
	def __init__(self):
		self.items = []
		self.p_set = set()

	def push(self, value_key_pair):
		'''
		Push a new value-key pair (tuple) into the priority queue and perform "decrease key" if the item is already in the priority queue
		'''
		if value_key_pair[1] not in self.p_set:
			heapq.heappush(self.items, value_key_pair)
			self.p_set.add(value_key_pair[1])
		else:
			min_value = value_key_pair[0]
			for pair in self.items:
				if pair[1] == value_key_pair[1]:
					if min_value > pair[0]:
						min_value = pair[0]
					pair[0] = -1  # Make sure to pop out the ones that are repeating
					heapq.heappop(self.items)
			heapq.heappush(self.items, (min_value, value_key_pair[1]))

	def pop(self):
		rm_item = heapq.heappop(self.items)
		self.p_set.remove(rm_item[1])
		return rm_item

	def size(self):
		return len(self.items)


class Solver:
	'''
	Define methods that implement the search algorithms, as well as variables that record some key information regarding each algorithm.
	'''
	def __init__(self):
		self.nodes_expanded = 0
		self.path = []
		self.search_depth = 0
		self.max_search_depth = 0
		self.run_time = 0
		self.max_usage = 0

	def bfs(self, init_state):
		'''
		Implements Breath-First Search, following the algorithm introduced in lecture
		'''
		start_time = time.time()
		frontier = Queue()
		frontier.enqueue(init_state)
		explored = set()

		while frontier.size() != 0:
			cur_state = frontier.dequeue()
			explored.add(cur_state)
			if cur_state.is_goalstate():
				temp_state = cur_state
				temp_path = []
				while temp_state.previous != None:
					temp_path.append(temp_state.move)
					temp_state = temp_state.previous
				temp_path.reverse()
				self.path = temp_path
				self.search_depth = cur_state.depth
				self.run_time = time.time() - start_time
				return True

			children = cur_state.get_successors()
			self.nodes_expanded += 1
			for child in children:
				child.depth = cur_state.depth + 1
				if child not in explored:
					if child not in frontier.q_set:
						frontier.enqueue(child)
						explored.add(child)
						if child.depth > self.max_search_depth:
							self.max_search_depth = child.depth
			ram_temp = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
			if ram_temp > self.max_usage:
				self.max_usage = ram_temp
		self.run_time = time.time() - start_time
		return False

	def dfs(self, init_state):
		'''
		Implements Depth-First Search, following the algorithm introduced in lecture
		'''
		start_time = time.time()
		frontier = Stack()
		frontier.push(init_state)
		explored = set()

		while frontier.size() != 0:
			cur_state = frontier.pop()
			explored.add(cur_state)
			if cur_state.is_goalstate():
				temp_state = cur_state
				temp_path = []
				while temp_state.previous != None:
					temp_path.append(temp_state.move)
					temp_state = temp_state.previous
				temp_path.reverse()
				self.path = temp_path
				self.search_depth = cur_state.depth
				self.run_time = time.time() - start_time
				return True

			children = cur_state.get_successors()
			self.nodes_expanded += 1
			children.reverse()
			for child in children:
				child.depth = cur_state.depth + 1
				if child not in explored:
					if child not in frontier.s_set:
						frontier.push(child)
						explored.add(child)
						if child.depth > self.max_search_depth:
							self.max_search_depth = child.depth
			ram_temp = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
			if ram_temp > self.max_usage:
				self.max_usage = ram_temp
		self.run_time = time.time() - start_time
		return False

	def astar(self, init_state):
		'''
		Implements A* Search, following the algorithm introduced in lecture
		'''
		start_time = time.time()
		frontier = Priority_Queue()
		temp_pair = (manhattan_distance(init_state) + init_state.depth, init_state)
		frontier.push(temp_pair)
		explored = set()

		while frontier.size() != 0:
			cur_state = frontier.pop()[1]
			explored.add(cur_state)
			if cur_state.is_goalstate():
				temp_state = cur_state
				temp_path = []
				while temp_state.previous != None:
					temp_path.append(temp_state.move)
					temp_state = temp_state.previous
				temp_path.reverse()
				self.path = temp_path
				self.search_depth = cur_state.depth
				self.run_time = time.time() - start_time
				return True

			children = cur_state.get_successors()
			self.nodes_expanded += 1
			for child in children:
				child.depth = cur_state.depth + 1
				if child not in explored:
					if child not in frontier.p_set:
						temp_pair_child = (manhattan_distance(child) + child.depth, child)
						frontier.push(temp_pair_child)
						explored.add(child)
						if child.depth > self.max_search_depth:
							self.max_search_depth = child.depth
					# else:
						# Decrease key already handled by the push function in the Priority_Queue class
			ram_temp = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
			if ram_temp > self.max_usage:
				self.max_usage = ram_temp
		self.run_time = time.time() - start_time
		return False


if __name__ == '__main__':
	
	# Check user input
	if len(sys.argv) != 3:
		print 'ERROR: USAGE: python driver.py <method> <board>'
		sys.exit(0)

	# Process user input
	method = sys.argv[1]
	board = [int(x) for x in sys.argv[2].split(',')]
	state = State(board)
	solver = Solver()

	# Solve the problem with the user-specified method
	if method == 'bfs':
		solver.bfs(state)
	elif method == 'dfs':
		solver.dfs(state)
	elif method == 'ast':
		solver.astar(state)
	else:
		print 'Please type in bfs, dfs, or ast as the method for solving the problem.'
		sys.exit(0)

	# Write the results to an output file		
	output_file = open('output.txt', 'w')
	output_file.write('path_to_goal: ' + str(solver.path) + '\n')
	output_file.write('cost_of_path: ' + str(len(solver.path)) + '\n')
	output_file.write('nodes_expanded: ' + str(solver.nodes_expanded) + '\n')
	output_file.write('search_depth: ' + str(solver.search_depth) + '\n')
	output_file.write('max_search_depth: ' + str(solver.max_search_depth) + '\n')
	output_file.write('running_time: %.8f' % solver.run_time + '\n')
	output_file.write('max_ram_usage: %.8f' % (float(solver.max_usage) / 1000000) + '\n')
	output_file.close()