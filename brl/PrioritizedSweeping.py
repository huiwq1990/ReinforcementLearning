from RL_framework import *
import random
import time
from PriorityQueue import UniquePriorityQueue

class PrioritizedSweeping(RLAlgorithm):
    # model: the input model
    # e: the parameter for randomization
    def __init__(self, model, k = 2, epsilon = 1, degrading_constant = 0.99, discount_rate = 0.9):
        self.model = model
        # value model
        self.V = {}
        # book-keeping keeper
        self.keepr = Keeper()
        # parameters for the algorithm
        self.k = k
        self.epsilon = epsilon
        self.degrading_constant = degrading_constant
        self.discount_rate = discount_rate
        # priority queue
        self.queue = UniquePriorityQueue()
        self.delta = 0.001

    # compute the value function V(s)
    def get_v(self, state):
        return self.V.get(state, 0)

    def print_v_table(self):
        for state in self.model.states:
            print (state, self.get_v(state))

    # compute the best reward for from a state to another
    def get_best_reward(self, state, next_state):
        actions = self.model.get_actions(state)
        reward = self.get_reward(state, actions[0], next_state)
        for action in actions:
            reward = max(reward, self.get_reward(state, action, next_state))
        return reward

    # get the next best state
    # if the best 
    def get_next_best_state(self, state):
        L = self.model.get_next_states(state)
        best_state = [L[0]]
        m = self.get_v(L[0]) + self.get_best_reward(state, L[0])
        for s in L[1:]:
            # first, check for ties, then check for greater state
            temp = self.get_v(s) + self.get_best_reward(state, s)
            if abs(temp - m)  < self.delta*m:
                best_state.append(s)
            elif temp > m:
                m = temp
                best_state = [s]
        return random.choice(best_state)

    # for any state, get the best action with the highest expected reward
    # if there are actions with equal rewards, return one randomly
    def get_best_action(self, state, next_state):
        actions = self.model.get_actions(state)
        # small constant in this to differentiate between action with zero reward vs. no relation state
        constant = 0.1
        p = self.get_transition(state, actions[0], next_state)
        r = self.get_reward(state, actions[0], next_state) + constant
        # expected reward
        m = p*r
        best_action = [actions[0]]
        for a in actions[1:]:
            # first check, for tie
            # then check for greater probability
            temp = self.get_transition(state, a, next_state)*(self.get_reward(state, a, next_state) + constant)
            if abs(temp - m) < self.delta*m:
                best_action.append(a)
            elif temp > m:
                m = temp
                best_action = [a]
        return random.choice(best_action)

    # for any state, get the best action to get into that state from the current state
    # if there are actions with equal probability, choose a random one
    def get_best_action_probability(self, state, next_state):
        actions = self.model.get_actions(state)
        p = self.get_transition(state, actions[0], next_state)
        action = [actions[0]]
        for a in actions[1:]:
            # first check, for tie
            # then check for greater probability
            if abs(self.get_transition(state, a, next_state) - p) < self.delta:
                action.append(a)
            elif self.get_transition(state, a, next_state) > p:
                p = self.get_transition(state, a, next_state)
                action = [a]
        return random.choice(action)

    # compute impact C(s, s*) = sum over a P(s|s*,a)*delta(s)
    # s1: current state, s0: predecessor
    def compute_impact(self, s1, s0, delta):
        s = 0
        for action in self.model.get_actions(s0):
            s += self.get_transition(s0, action, s1)*delta
        return s

    # V(s, a) = sum over s' P(s'|s,a)*(R(s,a,s') + V(s')*discount_rate)
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
        for action in actions[1:]:
            V_new = max(V_new, self.compute_v_per_action(state, action))
        delta_change = abs(self.get_v(state) - V_new)
        # update the dictionary
        self.V[state] = V_new
        # now compute the priority queue for the predecessor
        for s0 in self.model.get_prev_states(state):
            capacity = self.compute_impact(state, s0, delta_change)
            self.queue.push_or_update(-capacity, s0)

    def choose_action(self, state):
        # with some probability, choose a random action
        action = None
        if random.random() < self.epsilon:
            actions = self.model.get_actions(state)
            action = random.choice(actions)
            self.epsilon *= self.degrading_constant
            # make sure that we do still explore at the minimum level
            self.epsilon = max(self.epsilon, 0.01)
        else:
            best_next_state = self.get_next_best_state(state)
            # action = self.get_best_action(state, best_next_state)
            action = self.get_best_action_probability(state, best_next_state)
        return action
    
    def sweep_queue(self):
        for i in range(self.k - 1):
            (v, state) = self.queue.pop()
            self.sweep(state)        

    def next(self, action = None):
        if action == None:  
            action = self.choose_action(self.model.current_state)
        current_state = self.model.current_state
        reward = self.model.perform(action)
        next_state = self.model.current_state
        self.update_transition(current_state, action, next_state)
        self.update_reward(current_state, action, next_state, reward)
        self.sweep(current_state)
        self.sweep_queue()
        # print self.V
        #if (current_state.id == 8):
            #print "state 8 has been reached"
            #print (current_state, action, next_state, reward)
            #print "reward = ", self.get_reward(current_state, action, next_state)            
        return (action, reward, next_state)