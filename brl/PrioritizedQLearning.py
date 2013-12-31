from RL_framework import *
from QLearning import *
import random
from PriorityQueue import *

# implementation from here:
# http://www.tu-chemnitz.de/informatik/KI/scripts/ws0910/ml09_9.pdf

class PrioritizedQLearning(QLearning):
    # model: the input model
    # e: the parameter for randomization
    def __init__(self, model, learning_rate = 0.2, discount_rate = 0.2, epsilon = 0.9,
        num_state = 2, degrading_constant = 0.99, threshold = 0.2):
        """ Implementation of Q-learning, with learning rate, discount rate, and epsilon, which is the parameter for exploration"""
        self.model = model
        # book-keeping keeper
        self.keepr = Keeper()
        # parameters for the algorithm
        self.learning_rate = learning_rate
        self.discount_rate = discount_rate
        self.epsilon = epsilon
        self.num_state = num_state
        self.degrading_constant = degrading_constant
        self.threshold = threshold
        self.Q = {}
        # min-queue
        self.queue = UniquePriorityQueue()
        # the difference constant - used to check if two quantities are roughly the same
        self.detla = 0.001

    # update the quality function
    # using an explicit formula Q[s,a] = E[R(s,a)] + discount_rate*sum[T(state, action, s')*max_{a'}Q(s',a')]
    def update_Q(self, s1, a, s2, r):
        S = 0
        for state in self.model.get_next_states(s1):
            S += self.discount_rate * self.get_transition(s1, a, state) * (self.get_reward(s1, a, state) + self.get_max_Q(state))
        self.Q[(s1, a)] = S

    def sweep(self, s1, a, s2, r):
        q = self.get_Q(s1, a)
        p = abs(r + self.discount_rate * self.get_max_Q(s2) - q)
        # might need to push this to the top of the queue
        self.queue.push(-p, (s1, a, s2, r))

        # now perform the state sweep
        for i in range(self.num_state):
            if len(self.queue) > 0:
                (p, (s1, a, s2, r)) = self.queue.pop()
                q = self.get_Q(s1, a)
                # update the value of Q
                self.Q[(s1, a)] = q + self.learning_rate*(r + self.discount_rate * self.get_max_Q(s2) - q)
                for prev_state in self.model.get_prev_states(s1):
                    for action in self.model.actions:
                        r1 = self.get_reward(prev_state, action, s1)
                        q1 = self.get_Q(prev_state, action)
                        p1 = abs(r1 + self.discount_rate*self.get_max_Q(s1) - q1)
                        if p1 > self.threshold:
                            self.queue.push_or_update(-p1, (prev_state, action, s1, r1))
            else:
                break

    def next(self, action = None):
        if action == None:
            # with some probability, choose a random action
            action = self.choose_action_simple(self.model.current_state)
        current_state = self.model.current_state
        reward = self.model.perform(action)
        next_state = self.model.current_state
        self.update_reward(current_state, action, next_state, reward)
        self.update_transition(current_state, action, next_state)
        self.sweep(current_state, action, next_state, reward)
        return (action, reward, next_state)