import numpy as np
from helpers import distance

class ParticleFilter:
    def __init__(self, num_particles):
        self.initialized = False
        self.num_particles = num_particles

    # Set the number of particles.
    # Initialize all the particles to the initial position
    #   (based on esimates of x, y, theta and their uncertainties from GPS)
    #   and all weights to 1.0.
    # Add Gaussian noise to each particle.
    def initialize(self, x, y, theta, std_x, std_y, std_theta):
        self.particles = []
        for i in range(self.num_particles):
            self.particles.append({
                'x': np.random.normal(x, std_x),
                'y': np.random.normal(y, std_y),
                't': np.random.normal(theta, std_theta),
                'w': 1.0,
                'assoc': [],
            })
        self.initialized = True

    # Add measurements to each particle and add random Gaussian noise.
    def predict(self, dt, velocity, yawrate, std_x, std_y, std_theta):
        # Be careful not to divide by zero.
        v_yr = velocity / yawrate if yawrate else 0
        yr_dt = yawrate * dt
        for p in self.particles:
            # We have to take care of very small yaw rates;
            #   apply formula for constant yaw.
            if np.fabs(yawrate) < 0.0001:
                xf = p['x'] + velocity * dt * np.cos(p['t'])
                yf = p['y'] + velocity * dt * np.sin(p['t'])
                tf = p['t']
            # Nonzero yaw rate - apply integrated formula.
            else:
                xf = p['x'] + v_yr * (np.sin(p['t'] + yr_dt) - np.sin(p['t']))
                yf = p['y'] + v_yr * (np.cos(p['t']) - np.cos(p['t'] + yr_dt))
                tf = p['t'] + yr_dt
            p['x'] = np.random.normal(xf, std_x)
            p['y'] = np.random.normal(yf, std_y)
            p['t'] = np.random.normal(tf, std_theta)

    # Find the predicted measurement that is closest to each observed
    #   measurement and assign the observed measurement to this
    #   particular landmark.
    def associate(self, predicted, observations):
        associations = []
        # For each observation, find the nearest landmark and associate it.
        #   You might want to devise and implement a more efficient algorithm.
        for o in observations:
            min_dist = -1.0
            for p in predicted:
                dist = distance(o, p)
                if min_dist < 0.0 or dist < min_dist:
                    min_dist = dist
                    min_id = p['id']
                    min_x = p['x']
                    min_y = p['y']
            association = {
                'id': min_id,
                'x': min_x,
                'y': min_y,
            }
            associations.append(association)
        # Return a list of associated landmarks that corresponds to
        #   the list of (coordinates transformed) predictions.
        return associations

    # Update the weights of each particle using a multi-variate
    #   Gaussian distribution.
    def update_weights(self, sensor_range, std_landmark_x, std_landmark_y,
                       observations, map_landmarks):
        # TODO: For each particle, do the following:
        # 1. Select the set of landmarks that are visible
        #    (within the sensor range).
        # 2. Transform each observed landmark's coordinates from the
        #    particle's coordinate system to the map's coordinates.
        # 3. Associate each transformed observation to one of the
        #    predicted (selected in Step 1) landmark positions.
        #    Use self.associate() for this purpose - it receives
        #    the predicted landmarks and observations; and returns
        #    the list of landmarks by implementing the nearest-neighbour
        #    association algorithm.
        # 4. Calculate probability of this set of observations based on
        #    a multi-variate Gaussian distribution (two variables being
        #    the x and y positions with means from associated positions
        #    and variances from std_landmark_x and std_landmark_y).
        #    The resulting probability is the product of probabilities
        #    for all the observations.
        # 5. Update the particle's weight by the calculated probability.
        import math

        def multi_gaussian_distribution(trans_x, trans_y, assoc_x, assoc_y, std_landmark_x, std_landmark_y):
            gauss_norm = 1. / (2. * np.pi * std_landmark_x * std_landmark_y)
            expo_x = np.power((trans_x - assoc_x) / std_landmark_x, 2)
            expo_y = np.power((trans_y - assoc_y) / std_landmark_y, 2)
            exponent = expo_x + expo_y
            gauss_distribution = gauss_norm * np.exp(-0.5 * exponent)
            return gauss_distribution

        for particle in self.particles:
            predicted_landmarks = []    
            for landmark_id in map_landmarks:
                if distance(particle, map_landmarks[landmark_id]) < sensor_range:
                    predicted_landmarks.append({'id': landmark_id,
                                                'x': map_landmarks[landmark_id]['x'],
                                                'y': map_landmarks[landmark_id]['y']})

            if len(predicted_landmarks) == 0:
                continue

            transformed_obs = []
            for obs in observations:
                transformed_x = particle['x'] + math.cos(particle['t']) * obs['x'] - math.sin(particle['t']) * obs['y']
                transformed_y = particle['y'] + math.sin(particle['t']) * obs['x'] + math.cos(particle['t']) * obs['y']

                transformed_obs.append({'x': transformed_x,
                                        'y': transformed_y})

            associations = self.associate(predicted_landmarks, transformed_obs)

            weight = 1.0
            particle['w'] = 1.0
            particle['assoc'] = []

            for i in range(len(associations)):
                transformed_x = transformed_obs[i]['x']
                transformed_y = transformed_obs[i]['y']

                assoc_x = associations[i]['x']
                assoc_y = associations[i]['y']

                weight *= multi_gaussian_distribution(transformed_x, transformed_y,
                                                      assoc_x, assoc_y,
                                                      std_landmark_x, std_landmark_y) + 1e-60

                particle['assoc'].append(associations[i]['id'])
            
            particle['w'] = weight

    # Resample particles with replacement with probability proportional to
    #   their weights.
    def resample(self):
        # TODO: Select (possibly with duplicates) the set of particles
        #       that captures the posteior belief distribution, by
        # 1. Drawing particle samples according to their weights.
        # 2. Make a copy of the particle; otherwise the duplicate particles
        #    will not behave independently from each other - they are
        #    references to mutable objects in Python.
        # Finally, self.particles shall contain the newly drawn set of
        #   particles.
        import copy

        weights = np.array([p['w'] for p in self.particles])
        weights_sum = np.sum(weights)
        resample_prob = weights / weights_sum
        resample_idx = np.random.choice(self.num_particles, self.num_particles, p=resample_prob)

        resampled_particles = []
        for idx in resample_idx:
            resampled_particles.append(copy.deepcopy(self.particles[idx]))

        self.particles = resampled_particles

    # Choose the particle with the highest weight (probability)
    def get_best_particle(self):
        highest_weight = -1.0
        for p in self.particles:
            if p['w'] > highest_weight:
                highest_weight = p['w']
                best_particle = p
        return best_particle
