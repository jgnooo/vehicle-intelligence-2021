# **[Week 3 Assignment] : EKF & Sensor Fusion**

------

### Implementation

- KalmanFilter - update_ekf( )

    - Implement EKF update for radar measurements

    - 구현 내용 :

        1. Compute Jacobian Matrix H_j
           - Radar measurements rho, phi, rho dot 을 이용해 Jacobian matrix 계산

        ```python
        H_j = Jacobian(self.x)
        ```

        2. Calculate S = H_j \* P' \* H_j^T + R
           - 계산된 Jacobian matrix,  matrix P를 이용해 matrix S 계산

        ```python
        S = np.dot(np.dot(H_j, self.P), H_j.T) + self.R
        ```

        3. Calculate Kalman gain K = H_j \* P' \* Hj^T + R
           - Kalman gain 계산

        ```python
        K = np.dot(np.dot(self.P, H_j.T), np.linalg.inv(S))
        ```

        4. Estimate y = z - h(x')

        ```python
        px, py, vx, vy = self.x
        rho = sqrt(px ** 2 + py ** 2)
        phi = atan2(py ,px)
        rho_dot = ((px * vx) + (py * vy)) / rho
        
        h_of_x = np.array([rho, phi, rho_dot])
        y = z - h_of_x
        ```

        5. Normalize phi so that it is between -PI and +PI
           - -PI ~ +PI 범위의 값으로 normalize

        ```python
        def normalize(phi):
        	if phi < -np.pi:
          	phi = phi + 2 * np.pi
          elif phi > np.pi:
            phi = phi - 2 * np.pi
          return phi
        
        normalized_phi = normalize(y[1])
        y[1] = normalized_phi
        ```

        6. Calculate new estimates
   - Update
        
        ```python
        self.x = self.x + np.dot(K, y)
        self.P = self.P - np.dot(K, np.dot(H_j, self.P))
```
        
        


### 실행 결과

![week3](./EKF/week3_result.png)

