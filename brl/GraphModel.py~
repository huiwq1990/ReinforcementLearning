from RL_framework import *

class StateNode(State):
    def __init__(self, id, actions, next_state_ids, rewards, prev_state_ids):
        self.id = id
        self.next_state_ids = next_state_ids
        self.prev_state_ids = prev_state_ids
        self.asr = {}
        for i, a in enumerate(actions):
            self.asr[str(a)] = (next_state_ids[i],rewards[i])
            
    def perform(self, action): 
        return self.asr[str(action)]
        
    def get_next_state_ids(self):
        return self.next_state_ids
        
    def get_prev_state_ids(self):
        return self.prev_state_ids
        

class GraphModel(Model):
    def get_action_by_id(self, id):
        try:
            return self.actions[id]
        except Exception:
            return None

    #def perform_action_a(self):
    #    return self.perform(self.act_a)

    #def perform_action_b(self):
    #    return self.perform(self.act_b)

    #def set_current_state_by_state_id(self, id):
    #    self.current_state = self.state[id]
            
    # perform an action on the model
    def perform(self, action):
        reward = None
        if action in self.actions:
            (next_state_id, reward) = self.current_state.perform(action)
            self.current_state = self.state[next_state_id]
            self.step += 1
        return reward

    def get_next_states(self, state):
        L = []
        for id in self.state[state.get_id()].get_next_state_ids():
            L.append(self.state[id])
        return L

    def get_states_by_id(self, L):
        states = []
        for id in L:
            states.append(self.state[id])
        return states

    def get_prev_states(self, state):
        L = []
        for id in self.state[state.get_id()].get_prev_state_ids():
            L.append(self.state[id])
        return L

    def get_actions(self, state):
        return self.actions
