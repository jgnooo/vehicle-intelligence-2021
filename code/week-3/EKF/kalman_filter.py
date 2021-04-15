import numpy as np
from math import sqrt
from math import atan2
from tools import Jacobian

class KalmanFilter:
    def __init__(self, x_in, P_in, F_in, H_in, R_in, Q_in):
        self.x = x_in
        self.P = P_in
        self.F = F_in
        self.H = H_in
        self.R = R_in
        self.Q = Q_in

    def predict(self):
        self.x = np.dot(self.F, self.x)
        self.P = np.dot(np.dot(self.F, self.P), self.F.T) + self.Q

    def update(self, z):
        S = np.dot(np.dot(self.H, self.P), self.H.T) + self.R
        K = np.dot(np.dot(self.P, self.H.T), np.linalg.inv(S))
        # Calculate new estimates
        self.x = self.x + np.dot(K, z - np.dot(self.H, self.x))
        self.P = self.P - np.dot(np.dot(K, self.H), self.P)

    def update_ekf(self, z):
        # TODO: Implement EKF update for radar measurements
        # 1. Compute Jacobian Matrix H_j
        # 2. Calculate S = H_j * P' * H_j^T + R
        # 3. Calculate Kalman gain K = H_j * P' * Hj^T + R
        # 4. Estimate y = z - h(x')
        # 5. Normalize phi so that it is between -PI and +PI
        # 6. Calculate new estimates
        #    x = x' + K * y
        #    P = (I - K * H_j) * P
        
        # 1. Compute Jacobian Matrix H_j
        H_j = Jacobian(self.x)
        
        # 2. Calculate S = H_j * P' * H_j^T + R
        S = np.dot(np.dot(H_j, self.P), H_j.T) + self.R

        # 3. Calculate Kalman gain K = H_j * P' * Hj^T + R => P' H_j^T S^-1
        K = np.dot(np.dot(self.P, H_j.T), np.linalg.inv(S))

        # 4. Estimate y = z - h(x')
        px, py, vx, vy = self.x
        rho = sqrt(px ** 2 + py ** 2)
        phi = atan2(py ,px)
        rho_dot = ((px * vx) + (py * vy)) / rho

        h_of_x = np.array([rho, phi, rho_dot])
        y = z - h_of_x

        # 5. Normalize phi so that it is between -PI and +PI
        def normalize(phi):
            if phi < -np.pi:
                phi = phi + 2 * np.pi
            elif phi > np.pi:
                phi = phi - 2 * np.pi
            return phi

        normalized_phi = normalize(y[1])
        y[1] = normalized_phi

        # 6. Calculate new estimates
        #    x = x' + K * y
        #    P = (I - K * H_j) * P
        self.x = self.x + np.dot(K, y)
        self.P = self.P - np.dot(K, np.dot(H_j, self.P))