'''
Sheng Zhang
HW2 | Adversarial Search Problem: 2048-Game
'''

from BaseAI_3 import BaseAI
from Grid_3 import Grid
import math
import time
from operator import attrgetter


def eval(grid):
	'''
	Use heuristics to help evaluate the utility of a particular configuration of the grid to help ordering children states

	Metrics:
	1) Number of empty cells
	2) Max value of all tiles
	3) Monotonicity: reward for edge strategy and difference between sides
	4) Smoothness: difference between neighboring tiles
	'''

	# Specify the 1st measure: empty cells
	empty_cells = len(grid.getAvailableCells())
	
	# Specify the 2st measure: max tile
	max_tile = grid.getMaxTile()
	
	# Specify the 3rd measure: monotonicity
	'''
	diff_sides = sum([(m4 - m1) for m4, m1, in zip(grid.map[3], grid.map[0])])
	diff_sides_2 = []
	for i in range(0, grid.size):
		temp_diff = grid.map[i][3] - grid.map[i][0]
		diff_sides_2.append(temp_diff)
	diff_sides_2 = sum(diff_sides_2)
	
	reward_edge_strategy = []
	for i in range(0, grid.size):
		if grid.map[i] == sorted(grid.map[i]):
			reward_edge_strategy.append(max(grid.map[i]))
	for j in range(0, grid.size):
		if grid.map[3][j] >= grid.map[2][j] and grid.map[2][j] >= grid.map[1][j] and grid.map[1][j] >= grid.map[0][j]:
			reward_edge_strategy.append(grid.map[3][j])
	reward = sum(reward_edge_strategy)

	edge_star = grid.map[3][3]
	'''
	monotonicity = grid.map[3][3] + grid.map[3][2]*0.5**2 + grid.map[2][3]*0.5**2 + grid.map[3][1]*0.5**4 + grid.map[1][3]*0.5**4 + grid.map[2][2]*0.5**4 + grid.map[3][0]*0.5**6 + grid.map[2][1]*0.5**6 + grid.map[1][2]*0.5**6 + grid.map[0][3]*0.5**6

	# Specify the 4th measure: smoothness
	neighboring_pairs = []
	for i in range(0, grid.size):
		for j in range(0, grid.size):
			if i < 3:
				neighboring_pairs.append((i,j,i+1,j))
			if j < 3:
				neighboring_pairs.append((i,j,i,j+1))
	'''
	diff_neighbors = []
	sv_neighbors = []
	for index_pair in neighboring_pairs:
		if grid.map[index_pair[0]][index_pair[1]] != 0 and grid.map[index_pair[2]][index_pair[3]] != 0:
			diff = abs(grid.map[index_pair[0]][index_pair[1]] - grid.map[index_pair[2]][index_pair[3]])
			diff_neighbors.append(diff)
		if grid.map[index_pair[0]][index_pair[1]] == grid.map[index_pair[2]][index_pair[3]]:
			sv_neighbors.append(grid.map[index_pair[0]][index_pair[1]])
	total_diff_neighbors = sum(diff_neighbors)
	total_sv = sum(sv_neighbors)
	'''
	smoothness = []
	for index_pair in neighboring_pairs:
		smoothness.append(abs(grid.map[index_pair[0]][index_pair[1]]-grid.map[index_pair[2]][index_pair[3]]))
	smoothness = -sum(smoothness)

	# Calculate the final score
	if len(grid.getAvailableCells()) != 0:	
		score = 3*empty_cells + max_tile + 10*monotonicity + 0.2*smoothness
	else:
		score = 0

	return score


# Set time limit to 0.2 seconds for each move
time_limit = 0.2
	

class State:
	'''
	Represent a state of the grid
	'''
	def __init__(self, grid, move = None, depth = 0):
		self.grid = grid
		self.eval = eval(self.grid)
		self.move = move
		self.depth = depth

	def __str__(self):
		return(str(self.grid.map))

	def max_children(self):
		'''
		Return a list of children states of the current state for the maximum algorithm
		'''
		children = []
		moves = self.grid.getAvailableMoves()
		for move in moves:
			temp_grid = self.grid.clone()
			temp_grid.move(move)
			children.append(State(temp_grid, move, self.depth + 1))
		children = sorted(children, key = attrgetter('eval'))
		children.reverse()

		return children

	def min_children(self):
		'''
		Return a list of children states of the current state for the minimum algorithm
		'''
		children = []
		moves = self.grid.getAvailableCells()
		for move in moves:
			temp_grid = self.grid.clone()
			temp_grid_2 = self.grid.clone()
			temp_grid.map[move[0]][move[1]] = 2
			temp_grid_2.map[move[0]][move[1]] = 4
			children.append(State(temp_grid, None, self.depth + 1))
			children.append(State(temp_grid_2, None, self.depth + 1))
		children = sorted(children, key = attrgetter('eval'))

		return children

def minimize(state, alpha, beta, max_depth):
	'''
	Specify the minimize algorithm as shown in class
	'''

	global start_time, exceed_times

	if time.clock() - start_time >= time_limit:
		raise(Time_out_exception)

	if len(state.min_children()) == 0:
		return (None, eval(state.grid))

	if state.depth >= max_depth:
		return (None, eval(state.grid))

	(min_child, min_util) = (None, math.inf)

	for child in state.min_children():

		(_, util) = maximize(child, alpha, beta, max_depth)

		if util < min_util:
			(min_child, min_util) = (child, util)

		if min_util <= alpha:
			break

		if min_util < beta:
			beta = min_util

	return (min_child, min_util)


def maximize(state, alpha, beta, max_depth):
	'''
	Specify the minimize algorithm as shown in class
	'''

	global start_time, exceed_times

	if time.clock() - start_time >= time_limit:
		raise(Time_out_exception)

	if len(state.max_children()) == 0:
		return (None, eval(state.grid))

	if state.depth >= max_depth:
		return (None, eval(state.grid))


	(max_child, max_util) = (None, -math.inf)

	for child in state.max_children():

		(_, util) = minimize(child, alpha, beta, max_depth)

		if util > max_util:
			(max_child, max_util) = (child, util)

		if max_util >= beta:
			break

		if max_util > alpha:
			alpha = max_util

	return (max_child, max_util)


def decision(state, max_depth):
	'''
	Specify the decision function as shown in class
	'''

	global start_time, exceed_times

	(child, util) = maximize(state, -math.inf, math.inf, max_depth)
	
	print(util)

	return child



class Time_out_exception(Exception):
	'''
	Handle an exception if running time for a move is over the time limit
	'''
	pass


class PlayerAI(BaseAI):
	'''
	Specify the PlayerAI class that inherits from the BaseAI class
	'''
	def getMove(self, grid):
		initial_state = State(grid, None, 0)
		# Keep record of the start time
		global start_time
		start_time = time.clock()
		global exceed_times
		exceed_times = 0
		# Perform iterative deepening on the minimax algorithm
		max_depth = 1
		last_decision = decision(initial_state, max_depth)
		while True:
			max_depth += 1
			try:
				last_decision = decision(initial_state, max_depth)
			except Time_out_exception:
				break
		return last_decision.move


