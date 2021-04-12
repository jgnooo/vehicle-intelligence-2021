# **[Week 2 Assignment] : Markov Localization**

------

### Implementation

- motion_model( )

  - For each possible prior positions, calculate the probability that the vehicle will move to the position specified by `position` given as input.
  - 구현 내용 :

  ```python
  def motion_model(position, mov, priors, map_size, stdev):
  	position_prob = 0.0
    mu = mov
  
    probs = []
    for i in range(map_size):
        p_trans = norm_pdf(position - i, mov, stdev)
        p_prior = priors[i]
        p = p_trans * p_prior
        probs.append(p)
  
    position_prob = sum(probs)
    return position_prob
  ```

  

- observation_model( )

  - Given the `observations`, calculate the probability of this measurement being observed using `pseudo_ranges`.
  - 구현 내용 :

  ```python
  def observation_model(landmarks, observations, pseudo_ranges, stdev):
      distance_prob = 1.0
      
      if len(observations) == 0 or len(observations) > len(pseudo_ranges):
          distance_prob = 0.0
      else:
          for i in range(len(observations)):
              x_t = observations[i]
              mu = pseudo_ranges[i]
              p = norm_pdf(x_t, mu, stdev)
              distance_prob *= p
  
      return distance_prob
  ```

### 실행 결과

![week2](./week2.gif)
