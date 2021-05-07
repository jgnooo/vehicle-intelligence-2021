import numpy as np
import random
from math import sqrt, pi, exp

def gaussian_prob(obs, mu, sig):
    # Calculate Gaussian probability given
    # - observation
    # - mean
    # - standard deviation
    num = (obs - mu) ** 2
    denum = 2 * sig ** 2
    norm = 1 / sqrt(2 * pi * sig ** 2)
    return norm * exp(-num / denum)

# Gaussian Naive Bayes class
class GNB():
    # Initialize classification categories
    def __init__(self):
        self.classes = ['left', 'keep', 'right']
        self.means = {}
        self.stds = {}

    # Given a set of variables, preprocess them for feature engineering.
    def process_vars(self, vars):
        # The following implementation simply extracts the four raw values
        # given by the input data, i.e. s, d, s_dot, and d_dot.
        s, d, s_dot, d_dot = vars
        return [s], [(d % 4)], [s_dot], [d_dot]

    # Train the GNB using a combination of X and Y, where
    # X denotes the observations (here we have four variables for each) and
    # Y denotes the corresponding labels ("left", "keep", "right").
    def train(self, X, Y):
        '''
        Collect the data and calculate mean and standard variation
        for each class. Record them for later use in prediction.
        '''
        # TODO: implement code.
        val_with_lb = {}

        # val_with_lb['left'] = []
        # val_with_lb['keep'] = []
        # val_with_lb['right'] = []

        # for c in self.classes:
        #     for _ in range(4):
        #         val_with_lb[c].append([])

        # for x, y in zip(X, Y):
        #     x = self.process_vars(x)

        #     for idx, val in enumerate(x):
        #         val_with_lb[y][idx].append(val)

        for c in self.classes:
            val_with_lb[c] = np.empty((4, 0))

        for x, y in zip(X, Y):
            data = np.array(self.process_vars(x))
            val_with_lb[y] = np.append(val_with_lb[y], data, axis=1)
                
        means = {}
        stds = {}
        for c in self.classes:
            tmp = np.asarray(val_with_lb[c])
            means[c] = np.mean(tmp, axis=1)
            stds[c] = np.std(tmp, axis=1)
        
        self.means = means
        self.stds = stds


    # Given an observation (s, s_dot, d, d_dot), predict which behaviour
    # the vehicle is going to take using GNB.
    def predict(self, observation):
        '''
        Calculate Gaussian probability for each variable based on the
        mean and standard deviation calculated in the training process.
        Multiply all the probabilities for variables, and then
        normalize them to get conditional probabilities.
        Return the label for the highest conditional probability.
        '''
        # TODO: implement code.
        probs = {}
        
        for c in self.classes:
            curr_prob = 1.0
            for i in range(len(observation)):
                curr_prob *= gaussian_prob(observation[i], self.means[c][i], self.stds[c][i])

            probs[c] = curr_prob

        highest_prob = 0.0
        highest_class = 'keep'

        for c in self.classes:
            if probs[c] > highest_prob:
                highest_prob = probs[c]
                highest_class = c

        return highest_class