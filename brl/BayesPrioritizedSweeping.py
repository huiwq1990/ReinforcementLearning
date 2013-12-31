from PrioritizedSweeping import *
import numpy
from RL_framework import Model
from Hypothesis import *
from PriorityQueue import UniquePriorityQueue
    
class BayesPrioritizedSweeping(RLAlgorithm):
    def __init__(self, model, k = 2 , discount_rate = 0.9, u0 = 1, std0 = 0.2, sampling_interval = 20):
        self.model = model
        self.discount_rate = discount_rate
        self.keepr = Keeper()
        # priority queue for ML
        self.ML_queue = UniquePriorityQueue()
        # comparison constant
        self.delta = 0.001
        # number of back-up per action
        self.k = k
        # default mean and std
        self.u0 = u0
        self.std0 = std0
        # draw initial hypothesis
        self.hypothesis = Hypothesis.draw_init_hypothesis(model, self.u0, self.std0)
        # maximum-likelihood V
        self.ML_V = {}
        # interval to draw samples
        self.sampling_interval = sampling_interval
    
    def get_ML_transition(self, s1, a, s2):
        return RLAlgorithm.get_transition(self, s1, a, s2)
    
    def get_ML_reward(self, s1, a, s2):
        return RLAlgorithm.get_reward(self, s1, a, s2)
    
    def get_ML_v(self, state):
        return self.ML_V.get(state, 0)
    
    def update_ML_v(self, state, value):
        self.ML_V[state] = value
    
    # compute impact C(s, s*) = sum over a P(s|s*,a)*delta(s)
    # s1: current state, s0: predecessor
    def compute_impact(self, s1, s0, delta, transition_func):
        s = 0
        for action in self.model.get_actions(s0):
            s += transition_func(s0, action, s1)*delta
        return s    
    
    # V(s, a) = sum over s' P(s'|s,a)*(R(s,a,s') + V(s')*discount_rate)
    def compute_v_per_action(self, state, action, transition_func, reward_func, v_func):
        s = 0
        for next_state in self.model.get_next_states(state):
            s += transition_func(state, action, next_state)*(
                reward_func(state, action, next_state) + v_func(next_state)*self.discount_rate)
        return s
    
    def sweep_ML(self, state):
        self.sweep(state,
                   self.get_ML_transition,
                   self.get_ML_reward,
                   self.get_ML_v,
                   self.update_ML_v,
                   self.ML_queue)
    
    def sweep_hypothesis(self, state):
        self.sweep(state,
                   self.hypothesis.get_transition,
                   self.hypothesis.get_reward,
                   self.hypothesis.get_v,
                   self.hypothesis.update_v,
                   self.hypothesis.queue)
    
    # perform a Bellman backup on that state, 
    def sweep(self, state, transition, reward, get_v, update_v, queue):
        actions = self.model.get_actions(state)
        V_new = self.compute_v_per_action(state, actions[0], transition,
                                          reward, get_v)
        for action in actions[1:]:
            V_new = max(V_new, self.compute_v_per_action(
                state, action, transition, reward, get_v))
        delta_change = abs(get_v(state) - V_new)
        # update the dictionary
        update_v(state, V_new)
        # now compute the priority queue for the predecessor
        for s0 in self.model.get_prev_states(state):
                capacity = self.compute_impact(state, s0, delta_change, transition)
                queue.push_or_update(-capacity, s0)

    # sweep the Bellman queue for ML estimate
    #def sweep_ML_queue(self):
        #for i in range(self.k - 1):
            #(priority, state) = self.ML_queue.pop()
            #self.sweep_ML(state)
    
    #def sweep_hypothesis_queue(self):
        #for i in range(self.k - 1):
            #(priority, state) = self.hypothesis.queue.pop()
            #self.sweep_hypothesis(state)
            
    def sweep_queue(self):
        for i in range(self.k - 1):
            (priority, state) = self.hypothesis.queue.pop()
            self.sweep_hypothesis(state)        
            (priority, state) = self.ML_queue.pop()
            self.sweep_ML(state)
    
    def draw_hypothesis(self):
        # using the optimistic mode - assuming for unseen (state, action) to have max reward
        hypothesis = Hypothesis.draw_hypothesis(self.model, self.keepr, self.keepr.max_reward, self.std0)
        # initialize the hypothesis' v function with ML approximate
        hypothesis.V = dict(self.ML_V)
        return hypothesis
        
    # short cut to compute v per action for the hypothesis
    def compute_action_hypothesis(self, state, action):
        return self.compute_v_per_action(state, action,
                                         self.hypothesis.get_transition,
                                         self.get_ML_reward,
                                         self.hypothesis.get_v)
    
    def choose_action(self, state):
        # get the best action using value - iteration formula
        # https://stellar.mit.edu/S/course/6/fa13/6.S078/courseMaterial/topics/topic1/lectureNotes/mdp_vi/mdp_vi.pdf
        actions = self.model.get_actions(state)
        m = self.compute_action_hypothesis(state, actions[0])
        best_action = [actions[0]]
        for action in actions[1:]:
            temp = self.compute_action_hypothesis(state, action)
            if abs(temp - m) < self.delta*m:
                best_action.append(action)
            elif temp > m:
                best_action = [action]
            return random.choice(best_action)    
    
    def choose_random_choice(self, state):
        return random.choice(self.model.get_actions(state))
        
    def check_to_draw_hypothesis(self):
        # draw the hypothesis at every start state
        # if self.model.current_state == self.model.start_state:
            # draw a new hypothesis
            # self.hypothesis = self.draw_hypothesis()
        # draw a hypothesis every 20 steps
        if self.model.num_steps() % 20 == 0:
            self.hypothesis = self.draw_hypothesis()
            # self.hypothesis.print_complete_reward()
            # self.hypothesis.print_complete_transition()
            
        
    def next(self, action=None):
        # check to draw a new hypothesis
        self.check_to_draw_hypothesis()
        if action == None:
            action = self.choose_action(self.model.current_state)
        current_state = self.model.current_state
        reward = self.model.perform(action)
        next_state = self.model.current_state
        # do book-keeping
        self.keepr.update_reward_and_transition(current_state, action, next_state, reward)
        # do sweeping
        self.sweep_ML(current_state)
        self.sweep_hypothesis(current_state)
        self.sweep_queue()
        if (self.model.current_state.id == 8):
            # print (action, reward, next_state)
            pass
        
        if (self.model.current_state.id == 1):
            # print (action, reward, next_state)
            pass
                
        # print self.ML_V
        # print (current_state, action, next_state, reward)
        # print self.hypothesis.V
        return (action, reward, next_state)
        
    def get_transition(self, s1, a, s2):
        raise Exception("this method is discontinued")
    
    def get_reward(self, s1, a, s2):
        raise Exception("this method is discontinued")