from RL_framework import *
import heapq
import random
from PrioritizedSweeping import *

class PrioritizedSweepingPolicy(PrioritizedSweeping):
    # model: the input model
    # e: the parameter for randomization
    def __init__(self, model, k = 2, epsilon = 0.90, degrading_constant = 0.99, discount_rate = 0.9):
        self.model = model
        # value model
        self.V = {}
        # book-keeping keeper
        self.keepr = Keeper()
        # policy model
        self.policy = {}
        for state in self.model.states:
            self.policy[state] = [random.choice(self.model.actions)]
        # parameters for the algorithm
        self.k = k
        self.epsilon = epsilon
        self.degrading_constant = degrading_constant
        self.discount_rate = discount_rate
        # priority queue
        self.queue = UniquePriorityQueue()
        self.delta = 0.001

    # V(s, a) = sum over s' P(s'|s,a)*(R(s,a,s') + V(s')*discount-rate)
    def compute_v_per_action(self, state, action):
        s = 0
        for next_state in self.model.get_next_states(state):
            s += self.get_transition(state, action, next_state)*(
                self.get_reward(state, action, next_state) + self.get_v(next_state)*self.discount_rate)
        return s

    # perform a Bellman backup on that state
    def sweep(self, state):
        actions = self.model.get_actions(state)
        V_new = self.compute_v_per_action(state, actions[0])
        self.policy[state] = [actions[0]]
        for action in actions[1:]:
            temp = self.compute_v_per_action(state, action) 
            # first, check for ties
            # then check for improvement
            if abs(temp - V_new) < self.delta*V_new:
                self.policy[state].append(action)
            elif temp > V_new:
                V_new = temp
                self.policy[state] = [action]

        delta = abs(self.get_v(state) - V_new)
        # update the dictionary
        self.V[state] = V_new
        for s0 in self.model.get_prev_states(state):
            capacity = self.compute_impact(state, s0, delta)
            self.queue.push_or_update(-capacity, s0)

    def choose_action(self, state):
        # with some probability, choose a random action
        action = None
        if random.random() < self.epsilon:
            actions = self.model.get_actions(state)
            action = random.choice(actions)
            self.epsilon *= self.degrading_constant
            # make sure that we do still explore at the minimum level
            self.epsilon = min(self.epsilon, 0.1)
        else:
            action = random.choice(self.policy[state])
        return action

    def next(self, action = None):
        if action == None:
            action = self.choose_action(self.model.current_state)
        current_state = self.model.current_state
        reward = self.model.perform(action)
        next_state = self.model.current_state
        self.update_transition(current_state, action, next_state)
        self.update_reward(current_state, action, next_state, reward)
        self.sweep(current_state)
        for i in range(self.k - 1):
            (v, state) = self.queue.pop()
            self.sweep(state)
        return (action, reward, next_state)