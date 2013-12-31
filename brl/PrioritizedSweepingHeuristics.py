from RL_framework import *
from PrioritizedSweeping import *
import random
from PriorityQueue import UniquePriorityQueue

class PrioritizedSweepingHeuristics(PrioritizedSweeping):
    # model: the input model
    # e: the parameter for randomization
    def __init__(self, model, k = 2, epsilon = 0.90, degrading_constant = 0.99, discount_rate = 0.9):
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
        # keep track of the number of (state, action)
        self.num_actions = {}
        # priority queue
        self.queue = UniquePriorityQueue()
        self.delta = 0.001

    # get the number of times for a pair (state, action)
    def get_num_actions(self, state, action):
        return self.num_actions.get((state, action), 0)

    # get the least performed action for this state
    def get_least_action(self, state):
        actions = self.model.actions
        m = self.get_num_actions(state, actions[0])
        least_action = [actions[0]]
        # first, check for tie
        # then find the least performed action
        for action in actions[1:]:
            if self.get_num_actions(state, action) == m:
                least_action.append(action)
            elif self.get_num_actions(state, action) < m:
                m = self.get_num_actions(state, action)
                least_action = [action]          
        return (random.choice(least_action), 4.0/(4 + m**2))

    # update the action count per state
    def update_action(self, state, action):
        self.num_actions[(state, action)] = self.get_num_actions(state, action) + 1

    # get the best action using value - iteration formula
    # https://stellar.mit.edu/S/course/6/fa13/6.S078/courseMaterial/topics/topic1/lectureNotes/mdp_vi/mdp_vi.pdf
    def get_best_action_value_iteration(self, state):
        actions = self.model.actions
        m = self.compute_v_per_action(state, actions[0])
        best_action = [actions[0]]
        for action in actions[1:]:
            temp = self.compute_v_per_action(state, action)
            if abs(temp - m) < self.delta*m:
                best_action.append(action)
            elif temp > m:
                best_action = [action]
        return random.choice(best_action)

    def choose_action(self, state):
        # with some probability, choose a random action
        (least_action, epsilon) = self.get_least_action(state)
        action = None
        if random.random() < epsilon:
            self.update_action(state, least_action)
            action = least_action
        else:
            # best_next_state = self.get_next_best_state(state)
            # action = self.get_best_action(state, best_next_state)
            # action = self.get_best_action_probability(state, best_next_state)
            action = self.get_best_action_value_iteration(state)
            #if state.id == 8:
                #print "best action", (state, action)
        return action