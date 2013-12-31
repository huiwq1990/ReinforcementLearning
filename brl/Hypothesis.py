from RL_framework import *
from ChainModel import *
from PriorityQueue import *
import numpy

# for a model, this class holds all the data
class Hypothesis(object):
    def __init__(self, model):
        # transition model
        self.P = {}
        # probability model
        self.R = {}
        # game model
        self.model = model
        # priority queue
        self.queue = UniquePriorityQueue()
        # potential function        
        self.V = {}
    
    def get_transition(self, state, action, next_state):
        return self.P.get((state, action), {}).get(next_state, 0)
    
    # only return the reward if next_state can be visited
    def get_reward(self, state, action, next_state = None):
        if (next_state in self.model.get_next_states(state)):
            (u, std) = self.R.get((state, action))
            return random.gauss(u, std)
        return 0
    
    def print_complete_reward(self):
        print "Complete reward model"
        for state in self.model.states:
            for action in self.model.actions:
                print state, action, self.R.get((state, action), (-1,-1))
                
    def print_complete_transition(self):
        print "Complete transition model"
        for state in self.model.states:
            for action in self.model.actions:
                print state, action, self.P.get((state, action), {})
        
    def get_reward_table(self, state, action):
        return self.R[(state, action)]
    
    def get_transition_table(self, state, action, next_states):
        L = []
        for next_state in next_states:
            if self.get_transition(state, action, next_state) > 0:
                L.append((next_state, self.get_transition(state, action, next_state)))
        return L
    
    def get_v(self, state):
        return self.V.get(state, 0)
    
    def update_v(self, state, value):
        self.V[state] = value
    
    @staticmethod
    def draw_init_hypothesis(model, u0 = 0, std0 = 1):
        """ Sample an initial hypothesis for this model with u0, std0
        @model: RL_framework.Model
        """
        hypothesis = Hypothesis(model)
        # iterate through every state, action pairs
        for state in model.states:
            for action in model.actions:
                # reward model
                hypothesis.R[(state, action)] = (u0, std0)
                # transition model
                next_states = model.get_next_states(state)
                alphas = [1]*len(next_states)
                p = numpy.random.dirichlet(alphas)
                hypothesis.P[(state, action)] = {}
                for index, next_state in enumerate(next_states):
                    hypothesis.P[(state, action)][next_state] = p[index]
        return hypothesis

    @staticmethod
    def draw_hypothesis(model, keepr, u0 = 1, std0 = 1):
        """ Sample a hypothesis for this model with data from the keepr
        @model: RL_framework.Model
        """
        hypothesis = Hypothesis(model)
        for state in model.states:
            for action in model.actions:
                # transition model
                next_states = model.get_next_states(state)
                alphas = [1 + keepr.get_visit_count(state, action, next_state) for next_state in next_states]
                p = numpy.random.dirichlet(alphas)
                hypothesis.P[(state, action)] = {}
                for index, next_state in enumerate(next_states):
                    hypothesis.P[(state, action)][next_state] = p[index]
                # reward model
                # simplification: using sample variance instead of doing the priors
                n = keepr.get_visit_count(state, action)
                if n == 0:
                    sample_mean = u0
                    std = std0
                    tmp = std0**2/(model.num_steps() + 1)
                else:
                    # should think about whether to keep a minimum variance model
                    tmp = max((keepr.get_var_reward(state, action))**0.5, std0)/float(n)
                    sample_mean = float(keepr.get_sum_reward(state, action))/n
                    std = (keepr.get_var_reward(state, action))**0.5
                    std = max(std, std0)
                u = numpy.random.normal(sample_mean, tmp)
                hypothesis.R[(state, action)] = (u, std)
        return hypothesis
        
#model = ChainModel()
#hypothesis = Hypothesis.get_init_hypothesis(model)
#s1 = model.state[1]
#s2 = model.state[2]
#act_a = model.act_a
#act_b = model.act_b
#print hypothesis.get_reward_table(s1, act_a)
#print hypothesis.get_reward_table(s1, act_b)
#print hypothesis.get_reward_table(s2, act_a)
#print hypothesis.get_reward_table(s2, act_b)
#print hypothesis.get_transition_table(s1, act_a, model.get_next_states(s1))


