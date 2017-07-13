'''
Sheng Zhang
HW3 | Machine Learning: Classification - Perceptron
'''

import sys
import numpy as np
import matplotlib.pyplot as plt
from sklearn import preprocessing


def Perceptron_learning(X, Y, output_file):
	'''
	Implement the perceptron learning algorithm manually to record steps toward convergence
	'''
	W = np.zeros((X.shape[1]+1, 1))
	convergence = False
	while not convergence:
		error_any_i = False
		for i in range(0,X.shape[0]):
			if Y[i] * f(W[0,0] + np.dot(X[i,:], W[1:,0])) <= 0:
				error_any_i = True
				W[0,0] = W[0,0] + Y[i] * 1
				W[1:,0] = W[1:,0] + Y[i]*np.transpose(X[i,:])
				'''
				fig, ax = plt.subplots()
				x_value = np.linspace(0, 15)
				y_value = (W[0,0] + W[1,0]*x_value)/W[2,0]  # the line is w0 + w1*x1 + w2*x2 = 0
				ax.axis([0,15,-20,20])
				ax.plot(x_value, y_value)
				ax.scatter(X[:,[0]], X[:,[1]], c = Y)
				plt.show()
				'''

		for j in range(0,X.shape[1]):
			output_file.write(str(int(W[j,0])) + ',')
		output_file.write(str(int(W[X.shape[1],0])) + '\n')

		if error_any_i == False:
			convergence = True
			fig, ax = plt.subplots()
			x_value = np.linspace(0, 15)
			y_value = -(W[0,0] + W[1,0]*x_value)/W[2,0]  # the line is w0 + w1*x1 + w2*x2 = 0
			ax.axis([0,15,-20,20])
			ax.plot(x_value, y_value)
			ax.scatter(X[:,[0]], X[:,[1]], c = Y)
			plt.show()

	return W


def f(x):
	'''
	Define the activation function used in the perceptron learning algorithm
	'''
	if x > 0:
		return 1
	else:
		return -1



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
	X = raw_data[:,:-1]
	Y = raw_data[:,[-1]]

	# Scale Xs
	# X = preprocessing.scale(X)

	# Visualize the data
	fig, ax = plt.subplots()
	ax.scatter(X[:,[0]], X[:,[1]], c = Y)
	plt.show()

	# Run the Perceptron Learning Algorithm
	output = open(output_file, 'w')
	weights = Perceptron_learning(X, Y, output)
	output.close()

	