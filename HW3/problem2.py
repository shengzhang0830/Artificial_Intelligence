import sys
import numpy as np
import matplot as plt
import sklearn import preprocessing


def GradientDescent(X, Y, alpha, iterations, print_risk=False):
	"""
	Implement gradient descent for linear regression
	X: Input
	Y: Output
	alpha: Learning rate parameter
	iterations: Number of interactions allowed in the gradient descent algorithm
	"""

	n = X.shape[0]
	beta = np.zeros((X.shape[1]),1)

	for i in range(1:iterations):
		beta = beta - alpha/float(n)*np.dot(np.transpose(X), np.dot(X, beta) - Y)
		risk = ((np.dot(X, beta) - Y)**2)/(2*float(n))

		if print_risk:
			print "..."   # Check

	return beta



if __name__ == '__main__':

	# Check user input
	if len(sys.argv) != 3:
		print 'Usage: python <input.csv> <output.csv>'
		sys.exit(0)
	
	# Read in data
	raw_data = genfromtxt(sys.argv[1], delimiter = ',')
	X_raw = raw_data[:,:-1]
	Y = raw_data[:,[-1]]

	# Scale Xs
	X_scaled = preprocessing.scale(X_raw)

	# Add in the intercept column
	X = add_dummy_feature(X_scaled)

	# 