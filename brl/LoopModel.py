from RL_framework import *
from GraphModel import *
from random import random

class LoopModel(GraphModel):
    def __init__(self):
        self.name = "Loop"
        self.act_a = Action(0)
        self.act_b = Action(1)
        self.state = {}
        self.state[0] = StateNode(0, [self.act_a,self.act_b], [1,5], [0,0], [4,5,6,7,8])
        self.state[1] = StateNode(1, [self.act_a,self.act_b], [2,2], [0,0], [0])
        self.state[2] = StateNode(2, [self.act_a,self.act_b], [3,3], [0,0], [1])
        self.state[3] = StateNode(3, [self.act_a,self.act_b], [4,4], [0,0], [2])
        self.state[4] = StateNode(4, [self.act_a,self.act_b], [0,0], [1,1], [3])
        self.state[5] = StateNode(5, [self.act_a,self.act_b], [0,6], [0,0], [0])
        self.state[6] = StateNode(6, [self.act_a,self.act_b], [0,7], [0,0], [5])
        self.state[7] = StateNode(7, [self.act_a,self.act_b], [0,8], [0,0], [6])
        self.state[8] = StateNode(8, [self.act_a,self.act_b], [0,0], [2,2], [7])
        self.states = self.get_states_by_id([0,1,2,3,4,5,6,7,8])
        self.actions = [self.act_a, self.act_b]
        self.start_state = self.state[0]
        self.current_state = self.start_state
        self.step = 0

class SpecialLoopModel(LoopModel):
    def __init__(self):
        self.name = "SpecialLoop"
        self.act_a = Action(0)
        self.act_b = Action(1)
        self.state = {}
        self.state[0] = StateNode(0, [self.act_a,self.act_b], [1,5], [0,0], [4,5,6,7,8])
        self.state[1] = StateNode(1, [self.act_a,self.act_b], [2,2], [0,0], [0])
        self.state[2] = StateNode(2, [self.act_a,self.act_b], [3,3], [0,0], [1])
        self.state[3] = StateNode(3, [self.act_a,self.act_b], [4,4], [0,0], [2])
        self.state[4] = StateNode(4, [self.act_a,self.act_b], [0,0], [1,1], [3])
        self.state[5] = StateNode(5, [self.act_a,self.act_b], [0,6], [0,0], [0])
        self.state[6] = StateNode(6, [self.act_a,self.act_b], [0,7], [0,0], [5])
        self.state[7] = StateNode(7, [self.act_a,self.act_b], [0,8], [0,0], [6])
        self.state[8] = StateNode(8, [self.act_a,self.act_b], [0,0], [3,3], [7])
        self.states = self.get_states_by_id([0,1,2,3,4,5,6,7,8])
        self.actions = [self.act_a, self.act_b]
        self.start_state = self.state[0]
        self.current_state = self.start_state
        self.step = 0
        
class LoopModelDeadEnd(GraphModel):
    def __init__(self):
        self.name = "LoopDeadEnd"
        self.act_a = Action(0)
        self.act_b = Action(1)
        self.state = {}
        self.state[0] = StateNode(0, [self.act_a,self.act_b], [1,5], [0,0], [4,5,6,7])
        self.state[1] = StateNode(1, [self.act_a,self.act_b], [2,2], [0,0], [0])
        self.state[2] = StateNode(2, [self.act_a,self.act_b], [3,3], [0,0], [1])
        self.state[3] = StateNode(3, [self.act_a,self.act_b], [4,4], [0,0], [2])
        self.state[4] = StateNode(4, [self.act_a,self.act_b], [0,0], [1,1], [3])
        self.state[5] = StateNode(5, [self.act_a,self.act_b], [0,6], [0,0], [0])
        self.state[6] = StateNode(6, [self.act_a,self.act_b], [0,7], [0,0], [5])
        self.state[7] = StateNode(7, [self.act_a,self.act_b], [0,8], [2,0], [6])
        self.state[8] = StateNode(8, [self.act_a,self.act_b], [8,8], [0,0], [7])
        self.states = self.get_states_by_id([0,1,2,3,4,5,6,7,8])
        self.actions = [self.act_a, self.act_b]
        self.start_state = self.state[0]
        self.current_state = self.start_state
        self.step = 0
        
        
class LoopModelDiffTrans(GraphModel):
    def __init__(self):
        self.name = "LoopDiffTrans"
        self.act_a = Action(0)
        self.act_b = Action(1)
        self.state = {}
        self.state[0] = StateNode(0, [self.act_a,self.act_b], [1,5], [0,0], [4,5,6,7,8])
        self.state[1] = StateNode(1, [self.act_a,self.act_b], [2,2], [0,0], [0])
        self.state[2] = StateNode(2, [self.act_a,self.act_b], [3,3], [0,0], [1])
        self.state[3] = StateNode(3, [self.act_a,self.act_b], [4,4], [0,0], [2])
        self.state[4] = StateNode(4, [self.act_a,self.act_b], [0,0], [1,1], [3])
        self.state[5] = StateNode(5, [self.act_a,self.act_b], [0,6], [0,0], [0])
        self.state[6] = StateNode(6, [self.act_a,self.act_b], [0,7], [0,0], [5])
        self.state[7] = StateNode(7, [self.act_a,self.act_b], [0,8], [0,0], [6])
        self.state[8] = StateNode(8, [self.act_a,self.act_b], [0,0], [6,6], [7])
        self.states = self.get_states_by_id([0,1,2,3,4,5,6,7,8])
        self.actions = [self.act_a, self.act_b]
        self.start_state = self.state[0]
        self.current_state = self.start_state
        self.step = 0
        
    def perform(self, action):
        reward = None
        if action in self.actions:
            (next_state_id, reward) = self.current_state.perform(action)
            
            if self.current_state == self.state[8]:
                if random() > 0.5:
                    reward = -2
            
            self.current_state = self.state[next_state_id]
            self.step += 1
        return reward
