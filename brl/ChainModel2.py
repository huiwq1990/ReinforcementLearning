from RL_framework import *
from GraphModel import *
import random

class ChainModel2(GraphModel):
    def __init__(self):
        self.name = "Chain Model"
        self.act_a = Action(0)
        self.act_b = Action(1)
        self.state = {}
        self.state[1] = StateNode(1, [self.act_a,self.act_b], [1,2], [2,0], [1,2,3,4,5])
        self.state[2] = StateNode(2, [self.act_a,self.act_b], [1,3], [2,0], [1])
        self.state[3] = StateNode(3, [self.act_a,self.act_b], [1,4], [2,0], [2])
        self.state[4] = StateNode(4, [self.act_a,self.act_b], [1,5], [2,0], [3])
        self.state[5] = StateNode(5, [self.act_a,self.act_b], [1,5], [2,10], [4,5])
        self.states = self.get_states_by_id([1,2,3,4,5])
        self.actions = [self.act_a, self.act_b]
        self.start_state = self.state[1]
        self.current_state = self.start_state
        self.step = 0

# define the slippery chain model where with probability e, performing an action
# will have the opposite effect
class SlipperyChainModel2(ChainModel2):
    def __init__(self, e = 0.2):
        self.e = e
        ChainModel.__init__(self)

    def perform(self, action):
        if random.random() < self.e:
            return ChainModel.perform(self, self.get_action_by_id(1 - action.id))
        else:
            return ChainModel.perform(self, action)


# m = SlipperyChainModel(0.1)
# a = m.act_a
# b = m.act_b
# print m.perform(a)
# print m.current_state
# print m.perform(a)
