from math import sqrt
import numpy as np

'''
Gradient Descent Algorithm for Linear Regression
    feature_matrix: matrix whose rows are samples and columns are features
    output: vector containing actual value
    initial_weights: vector containing intial weight values
    step_size: scalar value for step size
    tolerance: scalar value to test convergence
'''
def regression_gradient_descent(feature_matrix, output, initial_weights, step_size, tolerance):
    converged = False
    weights = np.array(initial_weights)

    while not converged:
        predictions = predict_output(feature_matrix, weights)
        errors = predictions - output
        gradient_sum_squares = 0

        # update each feature's weight
        for i in range(len(weights)):
            derivative = feature_derivative(errors, feature_matrix[:,i])
            gradient_sum_squares += derivative * derivative
            weights[i] = weights[i] - step_size * derivative

        gradient_magnitude = sqrt(gradient_sum_squares)

        if gradient_magnitude < tolerance:
            converged = True

    return(weights)



def feature_derivative(errors, feature):
    derivative = 2 * np.dot(errors, feature)
    return(derivative)

def predict_output(feature_matrix, weights):
    predictions = np.dot(feature_matrix, weights)
    return(predictions)
