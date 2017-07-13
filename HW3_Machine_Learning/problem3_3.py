'''
Sheng Zhang
HW3 | Machine Learning: Classification - SVM, Logistic Regression, K-NN, Decision Trees, Random Forests
'''

import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import preprocessing
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn import linear_model
from sklearn.metrics import accuracy_score
from sklearn import svm
from sklearn.neighbors import KNeighborsClassifier
from sklearn import tree
from sklearn.ensemble import RandomForestClassifier
from numpy import array
from csv import reader


if __name__ == '__main__':

	# Check user input
	if len(sys.argv) != 3:
		print('ERROR: USAGE: python <input.csv> <output.csv>')
		sys.exit(0)
	else:
		input_file = sys.argv[1]
		output_file = sys.argv[2]

	# Read in data
	raw_data = pd.read_csv(input_file)
	X_raw = raw_data[['A','B']]
	Y = raw_data['label']

	# Visualize the data
	fig, ax = plt.subplots()
	ax.scatter(X_raw['A'], X_raw['B'], c = Y)
	plt.show()

	# Split dataset into training and test sets with stratified sampling
	X_train, X_test, Y_train, Y_test = train_test_split(X_raw, Y, test_size = 0.4, random_state = 7, stratify = Y)

	# Open output file for writing
	output = open(output_file, 'w')

	# Run SVM with a linear kernel
	svm_linear = svm.SVC()
	param_grid = {'C': [0.1, 0.5, 1, 5, 10, 50, 100], 'kernel': ['linear']}
	svm_linear_cv = GridSearchCV(svm_linear, param_grid, cv=5)
	svm_linear_cv.fit(X_train, Y_train)
	svm_linear_insample = svm_linear_cv.best_score_
	svm_linear = svm_linear_cv.best_estimator_
	Y_pred_test_svm_linear = svm_linear.predict(X_test)
	svm_linear_outsample = accuracy_score(Y_test, Y_pred_test_svm_linear)
	output.write('svm_linear,%.4f' % svm_linear_insample + ',%.4f' % svm_linear_outsample + '\n')

	# Run SVM with a polynomial kernel
	svm_poly = svm.SVC()
	param_grid = {'C': [0.1, 1, 3], 'gamma': [0.1, 0.5], 'degree': [4, 5, 6], 'kernel': ['poly']}
	svm_poly_cv = GridSearchCV(svm_poly, param_grid, cv=5)
	svm_poly_cv.fit(X_train, Y_train)
	svm_poly_insample = svm_poly_cv.best_score_
	svm_poly = svm_poly_cv.best_estimator_
	Y_pred_test_svm_poly = svm_poly.predict(X_test)
	svm_poly_outsample = accuracy_score(Y_test, Y_pred_test_svm_poly)
	output.write('svm_polynomial,%.4f' % svm_poly_insample + ',%.4f' % svm_poly_outsample + '\n')

	# Run SVM with a RBF kernel
	svm_rbf = svm.SVC()
	param_grid = {'C': [0.1, 0.5, 1, 5, 10, 50, 100], 'gamma': [0.1, 0.5, 1, 3, 6, 10], 'kernel': ['rbf']}
	svm_rbf_cv = GridSearchCV(svm_rbf, param_grid, cv=5)
	svm_rbf_cv.fit(X_train, Y_train)
	svm_rbf_insample = svm_rbf_cv.best_score_
	svm_rbf = svm_rbf_cv.best_estimator_
	Y_pred_test_svm_rbf = svm_rbf.predict(X_test)
	svm_rbf_outsample = accuracy_score(Y_test, Y_pred_test_svm_rbf)
	output.write('svm_rbf,%.4f' % svm_rbf_insample + ',%.4f' % svm_rbf_outsample + '\n')

	# Run logistic regression
	log_reg = linear_model.LogisticRegression()
	param_grid = {'C': [0.1, 0.5, 1, 5, 10, 50, 100]}
	log_reg_cv = GridSearchCV(log_reg, param_grid, cv=5)
	log_reg_cv.fit(X_train, Y_train)
	log_reg_insample = log_reg_cv.best_score_
	log_reg = log_reg_cv.best_estimator_
	Y_pred_test_log_reg = log_reg.predict(X_test)
	log_reg_outsample = accuracy_score(Y_test, Y_pred_test_log_reg)
	output.write('logistic,%.4f' % log_reg_insample + ',%.4f' % log_reg_outsample + '\n')

	# Run K-NN
	knn = KNeighborsClassifier()
	param_grid = {'n_neighbors': list(range(1,51)), 'leaf_size': list(range(5,65,5))}
	knn_cv = GridSearchCV(knn, param_grid, cv=5)
	knn_cv.fit(X_train, Y_train)
	knn_insample = knn_cv.best_score_
	knn = knn_cv.best_estimator_
	Y_pred_test_knn = knn.predict(X_test)
	knn_outsample = accuracy_score(Y_test, Y_pred_test_knn)
	output.write('knn,%.4f' % knn_insample + ',%.4f' % knn_outsample + '\n')

	# Run decision trees
	dt = tree.DecisionTreeClassifier()
	param_grid = {'max_depth': list(range(1,51)), 'min_samples_split': list(range(2,11))}
	dt_cv = GridSearchCV(dt, param_grid, cv=5)
	dt_cv.fit(X_train, Y_train)
	dt_insample = dt_cv.best_score_
	dt = dt_cv.best_estimator_
	Y_pred_test_dt = dt.predict(X_test)
	dt_outsample = accuracy_score(Y_test, Y_pred_test_dt)
	output.write('decision_tree,%.4f' % dt_insample + ',%.4f' % dt_outsample + '\n')

	# Run random forests
	rf = RandomForestClassifier()
	param_grid = {'max_depth': list(range(1,51)), 'min_samples_split': list(range(2,11))}
	rf_cv = GridSearchCV(rf, param_grid, cv=5)
	rf_cv.fit(X_train, Y_train)
	rf_insample = rf_cv.best_score_
	rf = rf_cv.best_estimator_
	Y_pred_test_rf = rf.predict(X_test)
	rf_outsample = accuracy_score(Y_test, Y_pred_test_rf)
	output.write('random_forest,%.4f' % rf_insample + ',%.4f' % rf_outsample + '\n')

	# Finish writing to the output file
	output.close()

