from RLKeeper import Keeper

class RLObject(object):
    def __init__(self, id):
        self.id = id

    # def __eq__(self, other):
    #   if isinstance(other, self.__class__):
    #       return self.__dict__ == other.__dict__
    #   else:
    #       return False

    # def __ne__(self, other):
    #   return not self.__eq__(other)  

    def get_id(self):
        return self.id

class Action(RLObject):
    def __str__(self):
        return "Action " + str(self.id)

    def __repr__(self):
        return self.__str__()

class State(RLObject):
    def __str__(self):
        return "State " + str(self.id)
        
    def __repr__(self):
        return self.__str__()

class Model(RLObject):
    def __init__(self, name):
        self.name = name
        # list of all actions
        self.actions = []
        # list of all states
        self.states = []
        self.start_state = None
        self.current_state = None
        self.step = 0

    def __str__(self):
        s = "Model:" + self.name + "\n"
        s += "States:" + str(self.states) + "\n"
        s += "Actions:" + str(self.actions) + "\n"
        return s 

    def get_current_state(self):
        raise Exception("not implemented")

    # get all available actions for this state
    def get_actions(self, state):
        raise Exception("not implemented")

    # get the available next states from this state - might
    # not be available for some algorithms
    def get_next_states(self, state):
        raise Exception("not implemented")

    def perform(self, action):
        raise Exception("not implemented")

    def num_steps(self):
        return self.step
        
    def reset(self):
        self.current_state  = self.start_state

class RLAlgorithm(object):
    def __init__(self):
        self.keepr = Keeper()
        self.model = Model()

    # compute transition function P(s1, a, s2)
    def get_transition(self, s1, a, s2):
       return self.keepr.get_transition(s1, a, s2)

    def get_reward(self, s1, a, s2):
        return self.keepr.get_reward(s1, a, s2)

    def get_transition_table(self, state, action):
        return self.keepr.get_transition_table(state, action, self.model.get_next_states(state))

    def get_reward_table(self, state, action):
        return self.keepr.get_reward_table(state, state, action, self.model.get_next_states(state))

    # update the transition model, keeping track of counts
    def update_transition(self, s1, a, s2):
        self.keepr.update_transition(s1, a, s2)

    # keeping track of the reward model
    def update_reward(self, s1, a, s2, r):
       self.keepr.update_reward(s1, a, s2, r)