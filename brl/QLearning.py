from RL_framework import *
import random

class QLearning(RLAlgorithm):
    # model: the input model
    # e: the parameter for randomization
    def __init__(self, model, learning_rate = 0.2, discount_rate = 0.2, epsilon = 0.2, degrading_constant = 0.999):
        """ Implementation of Q-learning, with learning rate, discount rate, and epsilon, which is the parameter for exploration"""
        self.model = model
        # parameters for the algorithm
        self.learning_rate = learning_rate
        self.discount_rate = discount_rate
        self.epsilon = epsilon
        self.degrading_constant = degrading_constant
        self.Q = {}
        # the difference constant - used to check if two quantities are roughly the same
        self.detla = 0.001

    # return the quality function
    def get_Q(self, state, action):
        return self.Q.get((state, action), 0)

    def get_max_Q(self, state):
        m = 0
        for action in self.model.get_actions(state):
            m = max(m, self.get_Q(state, action))
        return m

    def choose_action(self, state, return_q=False):
        q = [self.get_Q(state, a) for a in self.model.actions]
        maxQ = max(q)
        if random.random() < self.epsilon:
            #action = random.choice(self.actions)
            minQ = min(q); mag = max(abs(minQ), abs(maxQ))
            q = [q[i] + random.random() * mag - .5 * mag for i in range(len(self.model.actions))] # add random values to all the actions, recalculate maxQ
            maxQ = max(q)
        count = q.count(maxQ)
        if count > 1:
            best = [i for i in range(len(self.model.actions)) if q[i] == maxQ]
            i = random.choice(best)
        else:
            i = q.index(maxQ)
        action = self.model.actions[i]
        if return_q: # if they want it, give it!
            return action, q
        return action

    # for any state, get the best action by computing the quality function  Q(state, action)
    def get_best_action(self, state):
        actions = self.model.get_actions(self.model.current_state)
        m = self.get_Q(state, actions[0])
        best_action = [actions[0]]
        for action in actions[1:]:
            # first, check for ties
            if abs(self.get_Q(state, action) - m) < self.detla:
                best_action.append(action)
            elif self.get_Q(state, action) > m:
                m = self.get_Q(state, action)
                best_action = [action]
        return random.choice(best_action)

    # update the quality function
    def update_Q(self, s1, a, s2, r):
        q = self.get_Q(s1, a)
        if (s1, a) in self.Q:
            self.Q[(s1, a)] = q + self.learning_rate * (r + self.discount_rate * self.get_max_Q(s2) - q)
        else:
            self.Q[(s1, a)] = r

    def choose_action_simple(self, state):
        if random.random() < self.epsilon:
            actions = self.model.get_actions(state)
            action = random.choice(actions)
            self.epsilon *= self.degrading_constant
        else:
            action = self.get_best_action(state)
        return action
        
    def next(self, action = None):
        if action == None:
            # with some probability, choose a random action
            action = self.choose_action_simple(self.model.current_state)
        current_state = self.model.current_state
        reward = self.model.perform(action)
        next_state = self.model.current_state
        self.update_Q(current_state, action, next_state, reward)
        return (action, reward, next_state)