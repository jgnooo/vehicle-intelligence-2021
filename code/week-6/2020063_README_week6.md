# Week 7 - Hybrid A* Algorithm & Trajectory Generation

------

### Implementation

- Assignment #1 (https://github.com/ShineySun/ 참조)
under the directory [./GNB](./GNB), you are given two Python modules:

* `prediction.py`: the main module you run. The `main()` function does two things: (1) read an input file ([`train.json`](./GNB/train.json)) and train the GNB (Gaussian Naive Bayes) classifier using the data stored in it, and (2) read another input file ([`test.json`](./GNB/test.json)) and make predictions for a number of data points. The accuracy measure is taken and displayed.
* `classifier.py`: main implementation of the GNB classifier. You shall implement two methods (`train()` and `precict()`), which are used to train the classifier and make predictions, respectively.

- 구현 내용 :
    1. train() : Collect the data and calculate mean and standard variation for each class. Record them for later use in prediction.
    ```python
    def train(self, X, Y):
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
    ```
    - `self.classes` 를 이용하여 각 class `left,` `keep`, `right` 에 포함되어 있는 데이터의 mean, std를 구함
    - numpy, list 를 이용해 데이터를 모은 후 mean, std 함수를 사용해 mean, std를 각각 계산
       
    2. predict() : Calculate Gaussian probability for each variable based on the mean and standard deviation calculated in the training process. Multiply all the probabilities for variables, and 
                   then normalize them to get conditional probabilities. Return the label for the highest conditional probability.
    ```python
    def predict(self, observation):
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
    ```
    - `gaussian_prob` 함수를 이용해 observation 확률을 계산하여 multiply
    - `highest_prob`을 찾아 prediction

### 실행 결과
![week6](week6_result.png)

- Assignment #2