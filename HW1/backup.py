#!/usr/bin/python

import sys
import math

from collections import deque
import queue



def up(state,loc):
	if loc-3 >= 0:
		tmp = state[loc]
		state[loc] = state[loc-3]
		state[loc-3] = tmp
	return state

def down(state,loc):
	if loc+3 <= 8:
		tmp = state[loc]
		state[loc] = state[loc+3]
		state[loc+3] = tmp
	return state

def left(state,loc):
	if loc % 3 != 0:
		tmp = state[loc]
		state[loc] = state[loc-1]
		state[loc-1] = tmp
	return state

def right(state,loc):
	if loc % 3 != 2:
		tmp = state[loc]
		state[loc] = state[loc+1]
		state[loc+1] = tmp
	return state


def neighbors(board):
	current_loc = board.index('0')
	neighbors_loc = []
	if current_loc-3 >= 0:
		neighbors_loc.append(current_loc-3)
	if current_loc+3 <= 8:
		neighbors_loc.append(current_loc+3)
	if current_loc % 3 == 1:
		neighbors_loc.append(current_loc-1)
	if current_loc % 3 == 2:
		neighbors_loc.append(current_loc-1)
	if current_loc % 3 == 0:
		neighbors_loc.append(current_loc+1)
	if current_loc % 3 == 1:
		neighbors_loc.append(current_loc+1)
	return neighbors_loc


def bfs(initial,goal):
	path = [initial]
	# frontier = deque([initial.index('0')])
	frontier = queue.Queue()
	frontier.put(initial.index('0'))
	print(frontier)
	explored = []
	state = initial
	# explored_last_step = []

	while frontier.qsize() != 0:
		curr_loc = frontier.get()
		# explored.append(explored_last_step)
		# explored_last_step.append(curr_loc)
		explored.append(curr_loc)

		if state == goal:
			print ('success')
			return 1

		for neighbor in neighbors(state):
			if neighbor not in frontier.queue or explored:
				frontier.put(neighbor)

		print(frontier)
		print(explored)
		print(explored[-1])

		print(curr_loc)
		print(state)

		if(len(explored) > 1):
			print(explored[-1])
			print(explored[-2])
	
			if(explored[-1]-explored[-2] == -3):
				state_new = up(state,curr_loc)
			if(explored[-1]-explored[-2] == 3):
				state_new = down(state,curr_loc)
			if(explored[-1]-explored[-2] == -1):
				state_new = left(state,curr_loc)
			if(explored[-1]-explored[-2] == 1):
				state_new = right(state,curr_loc)
			path.append(state_new)
			state = state_new




	print ('failure')
	return 0


method = sys.argv[1]
board = sys.argv[2].split(',')
print(board)
goal = ['0','1','2','3','4','5','6','7','8']

bfs(board,goal)

print(explored)





'''
		state_new = up(state,curr_loc)
		if state_new == state:
			state_new = down(state,curr_loc)
			if state_new == state:
				state_new = left(state,curr_loc)
				if state_new == state:
					state_new = right(state,curr_loc)









	while len(frontier) != 0:
		curr_loc = frontier.popleft()
		# explored.append(explored_last_step)
		# explored_last_step.append(curr_loc)
		explored.append(curr_loc)

		if state == goal:
			print ('success')
			return 1

		for neighbor in neighbors(state):
			if neighbor not in frontier.queue or explored:
				frontier.append(neighbor)
'''