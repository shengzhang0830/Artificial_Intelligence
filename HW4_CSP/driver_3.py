'''
Sheng Zhang
HW4 | Constraint Satisfaction Problem: Sudoku
'''

import sys
import math
import time
import copy
import heapq
import sys
import itertools


class Sudoku:
	'''
	Define the class that represents a Sudoku board
	'''
	def __init__(self, board): # board is a string
		self.board = {}  # Use a dictionary to represent the Sudoku board
		row_index = ['A','B','C','D','E','F','G','H','I']
		col_index = list(range(1,10))
		k = 0
		for i in row_index:
			for j in col_index:
				self.board[i+str(j)] = int(board[k])
				k += 1


class CSP:
	'''
	Define the class that solves Constraint Satisfaction Problems
	'''
	def __init__(self, sudoku):
		self.sudoku = sudoku
		self.var_domain = {}
		self.constraints = set()
		self.temp_var_domain = self.var_domain

		# Fill in self.var_domain, which keeps track of all variables and their possible domains
		for var, value in self.sudoku.board.items():
			if value != 0:
				self.var_domain[var] = [value]
			else:
				self.var_domain[var] = list(range(1,10))

		# Specify row and column constraints
		rac = 0
		for v1 in self.var_domain.keys():
			for v2 in self.var_domain.keys():
				if len(list(set(list(v1)).intersection(list(v2)))) == 1:
					# if the names of the variables matched on exactly one character, they are in the same row or the same column
					if (v2,v1) not in self.constraints:
						rac += 1
						self.constraints.add((v1,v2))

		# Specify square constraints
		square_1 = ['A1','A2','A3','B1','B2','B3','C1','C2','C3']
		square_2 = ['D1','D2','D3','E1','E2','E3','F1','F2','F3']
		square_3 = ['G1','G2','G3','H1','H2','H3','I1','I2','I3']
		square_4 = ['A4','A5','A6','B4','B5','B6','C4','C5','C6']
		square_5 = ['D4','D5','D6','E4','E5','E6','F4','F5','F6']
		square_6 = ['G4','G5','G6','H4','H5','H6','I4','I5','I6']
		square_7 = ['A7','A8','A9','B7','B8','B9','C7','C8','C9']
		square_8 = ['D7','D8','D9','E7','E8','E9','F7','F8','F9']
		square_9 = ['G7','G8','G9','H7','H8','H9','I7','I8','I9']
		squares = [square_1, square_2, square_3, square_4, square_5, square_6, square_7, square_8, square_9]
		for square in squares:
			square_constraints = list(itertools.combinations(square,2))
			for sq in square_constraints:
				if (sq[0],sq[1]) not in self.constraints and (sq[1],sq[0]) not in self.constraints:
					self.constraints.add(sq)

	def get_arc(self):
		'''
		Return a queue of tuples that keeps track of constraints in both directions
		'''
		arcs = Queue()
		for constraint in self.constraints:
			arcs.enqueue(constraint)
			arcs.enqueue((constraint[1],constraint[0]))

		return arcs

	def check_consistency(self, var, value, cur_assignment):
		'''
		Check that the assignment dict is still consistent after 'value' is assigned to 'var'
		'''
		consistent = True
		for assigned_var, assigned_value in cur_assignment.items():
			if (var,assigned_var) in self.constraints or (assigned_var,var) in self.constraints:
				if assigned_value[0] == value:
					consistent = False
					break
			if var == assigned_var:
				consistent = False
				break

		return consistent

	def get_assigned_and_unassigned(self):
		'''
		Return a tuple of two dictionaries, representing unassigned variables and assigned variables, with their domains
		'''
		variables = csp.var_domain.keys()
		assignment = {}
		for v in variables:
			if len(list(csp.var_domain[v])) == 1:
				assignment[v] = csp.var_domain[v]
			
		unassigned_var_domain = {}
		for v in variables:
			if v not in assignment.keys():
				unassigned_var_domain[v] = csp.var_domain[v]

		return (assignment,unassigned_var_domain)


class Queue:
	'''
	Define an efficient queue implementation, adapted from http://interactivepython.org/courselib/static/pythonds/BasicDS/ImplementingaQueueinPython.html
	'''
	def __init__(self):
		self.items = []

	def enqueue(self, item):
		self.items.insert(0, item)

	def dequeue(self):
		rm_item = self.items.pop()
		return rm_item

	def size(self):
		return len(self.items)


def ac3(csp):
	'''
	Implement the AC-3 algorithm; Return a boolean indicating whether inconsistency is found
	'''
	csp_arcs = csp.get_arc()
	while csp_arcs.size() != 0:
		(Xi, Xj) = csp_arcs.dequeue()
		if revise(csp, Xi, Xj):
			if len(csp.var_domain[Xi]) == 0:
				return False
			for constraint in csp.constraints:
				if Xi ==  constraint[1]:
					csp_arcs.enqueue(constraint)
	return True


def revise(csp, var_1, var_2):
	'''
	Define a helper function used by the AC-3 algorithm
	'''
	revised = False
	for d in csp.var_domain[var_1]:
		some_d2_satisfy = False
		for d2 in csp.var_domain[var_2]:
			if d != d2:
				some_d2_satisfy = True
				break
		if not some_d2_satisfy:
			csp.var_domain[var_1].remove(d)
			revised == True
	return revised


def backtracking_search(csp):
	'''
	Start the backtracking search algorithm
	'''
	return recursive_backtrack(csp,{})


def recursive_backtrack(csp,assignment):
	'''
	Implement the backtracking algorithm recursively; Return a solution, or a failure
	'''
	
	# Get unassigned variables based on assignment and the problem
	unassigned_var_domain = csp.get_assigned_and_unassigned()[1]

	# Check whether the assignment is complete
	if len(unassigned_var_domain) == 0:
		return csp.var_domain

	# Select the next to-be-assigned variable using the minimum remaining value heuristic (choose the one with the fewest possible values)
	var = sorted(unassigned_var_domain, key = lambda k: len(unassigned_var_domain[k]))[0]

	# Implement the backtrack algorithm
	for value in csp.var_domain[var]:
		if csp.check_consistency(var, value, assignment):
			assignment[var] = [value]
			csp.temp_var_domain[var] = [value]
			
			# Apply forward checking
			for constraint in csp.constraints:
				if var == constraint[0]:
					if value in csp.temp_var_domain[constraint[1]]:
						csp.temp_var_domain[constraint[1]].remove(value)
				elif var == constraint[1]:
					if value in csp.temp_var_domain[constraint[0]]:
						csp.temp_var_domain[constraint[0]].remove(value)
			
			result = recursive_backtrack(csp,assignment)
			if result != False:
				return result
		csp.temp_var_domain = csp.var_domain
		assignment[var] = csp.var_domain[var]
	return False



if __name__ == '__main__':

	# Check user input
	if len(sys.argv) != 2:
		print('ERROR: USAGE: python sudoku_board')
		sys.exit(0)
	else:
		sudoku_board = list(sys.argv[1])

	# Solve the sudoku board
	sudoku = Sudoku(sudoku_board)
	csp = CSP(sudoku)
	ac3(csp)  # use AC-3 to reduce the domain size
	assignment = backtracking_search(csp)
	# assignment = csp.var_domain

	# Output results to a file
	solution = ''
	for r in ['A','B','C','D','E','F','G','H','I']:
		for c in range(1,10):
			solution += str(assignment[r+str(c)])

	with open('output.txt','w') as out_file:
		out_file.write(solution)



# Shell commands for testing
# for i in ${seq 1 ${cat sudokus_start.txt | wc -l}}; do python driver_3.py ${sed -n ${i}p sudokus_start.txt}; done > sudoku_test.txt

