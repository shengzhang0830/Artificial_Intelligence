'''
Sheng Zhang
HW3 | Machine Learning: Regression
'''

import sys
import numpy as np
import matplotlib as plt
from sklearn import preprocessing


def GradientDescent(X, Y, alpha, iterations):
	"""
	Implement gradient descent for linear regression
	X: Input
	Y: Output
	alpha: Learning rate parameter
	iterations: Number of interactions allowed in the gradient descent algorithm
	"""

	n = X.shape[0]
	beta = np.zeros((X.shape[1],1))

	for i in range(1,iterations):
		beta = beta - alpha*np.dot(np.transpose(X), np.dot(X, beta) - Y)/float(n)
		# risk = ((np.dot(X, beta) - Y)**2)/(2*float(n))

	return beta



if __name__ == '__main__':

	# Check user input
	if len(sys.argv) != 3:
		print('ERROR: USAGE: python <input.csv> <output.csv>')
		sys.exit(0)
	else:
		input_file = sys.argv[1]
		output_file = sys.argv[2]

	# Read in data
	raw_data = np.genfromtxt(input_file, delimiter = ',')
	X_raw = raw_data[:,:-1]
	Y = raw_data[:,[-1]]

	# Scale Xs
	X_scaled = preprocessing.scale(X_raw)

	# Add in the intercept column
	X = preprocessing.add_dummy_feature(X_scaled)

	# Run gradient descent for the nine pairs of learning rates and number of iterations given, and print the results to a file
	with open (output_file, 'w') as output:
		for alpha in [0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1, 5, 10, 0.3]:
			n_iter = 100
			beta = GradientDescent(X, Y, alpha, n_iter)
			output.write(str(alpha) + ',' + str(n_iter) + ',%.3f' % beta[0] + ',%.3f' % beta[1] + ',%.3f' % beta[2] + '\n')
		
