from RL_framework import *
import random

class ChainModel(Model):
    def __init__(self):
        self.name = "Chain Model"
        self.state = {}
        self.state[1] = State(1)
        self.state[2] = State(2)
        self.state[3] = State(3)
        self.state[4] = State(4)
        self.state[5] = State(5)
        self.act_a = Action(0)
        self.act_b = Action(1)
        self.states = self.get_states_by_id([1,2,3,4,5])
        self.actions = [self.act_a, self.act_b]
        self.start_state = self.state[1]
        self.current_state = self.start_state
        self.step = 0

    def get_action_by_id(self, id):
        if id == 0:
            return self.act_a
        elif id == 1:
            return self.act_b
        else:
            return None

    # perform an action on the model
    def perform(self, action):
        next_state = None
        reward = None
        if action == self.act_a:
            if self.current_state == self.state[5]:
                next_state = self.state[5]
                reward = 10
            else:
                id = self.current_state.get_id()
                next_state = self.state[id + 1]
                reward = 0
        else:
            next_state = self.state[1]
            reward = 2
        self.current_state = next_state
        self.step += 1
        return reward

    def get_next_states(self, state):
        L = [self.state[1]]
        if state == self.state[5]:
            L.append(self.state[5])
        else:
            L.append(self.state[state.get_id()+1])
        return L

    def get_states_by_id(self, L):
        states = []
        for id in L:
            states.append(self.state[id])
        return states
    
    def get_state_by_id(self, id):
        return self.state[id]

    def get_prev_states(self, state):
        if state == self.state[1]:
            return self.get_states_by_id([1,2,3,4,5])
        elif state == self.state[5]:
            return self.get_states_by_id([4,5])
        else:
            return self.get_states_by_id([state.get_id() - 1])

    def get_actions(self, state):
        return self.actions

# define the slippery chain model where with probability e, performing an action
# will have the opposite effect
class SlipperyChainModel(ChainModel):
    def __init__(self, e = 0.2):
        self.e = e
        self.name = "SlipperyChain"
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
