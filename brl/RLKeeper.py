# this class keeps auxiliary information for RL algorithm
class Keeper(object):
    def __init__(self):
        self.sum_reward_squares = {}
        self.sum_reward = {}
        self.visit_count_state = {}
        self.visit_count_state_action = {}
        # reward model
        self.R = {}
        # transition model
        self.P = {}
        # max reward
        self.max_reward = 0

    def get_sum_reward(self, state, action):
        return self.sum_reward.get((state, action), 0)

    def get_var_reward(self, state, action):
        n = float(self.get_visit_count(state, action))
        if n == 0:
            return 0
        SS = self.get_sum_reward_squares(state, action)
        S = self.get_sum_reward(state, action)
        var = (SS - S**2/n)/n
        # for numerical stability
        if var < 0:
            return 0
        return var

    def update_sum_reward(self, state, action, r):
        self.sum_reward[(state, action)] = self.get_sum_reward(state, action) + r

    def get_sum_reward_squares(self, state, action):
        return self.sum_reward_squares.get((state, action), 0)

    def update_sum_reward_squares(self, state, action, r):
        self.sum_reward_squares[(state, action)] = self.get_sum_reward_squares(state, action) + r**2

    def get_visit_count(self, state, action = None, next_state = None):
        if action == None:
            return self.visit_count_state.get(state, 0)
        if next_state == None:
            return self.visit_count_state_action.get((state, action), 0)
        return self.P.get((state, action, next_state), 0)

    def increase_count(self, state, action):
        self.visit_count_state[state] = self.get_visit_count(state) + 1
        self.visit_count_state_action[(state, action)] = self.get_visit_count(state, action) + 1

    def get_reward(self, s1, a, s2):
        """ compute the reward for state, action, next state"""
        v = (s1, a, s2)
        if v in self.R:
            (s, total) = self.R[v]
            return float(s)/total
        return 0

    def update_reward(self, s1, a, s2, r):
        """ Update the reward model"""
        self.update_reward_sums(s1, a, r)
        (s, total) = self.R.get((s1, a, s2), (0, 0))
        self.R[(s1, a, s2)] = (s + r, total + 1)
        self.max_reward = max(self.max_reward, r)

    def update_reward_sums(self, state, action, r):
        self.update_sum_reward(state, action, r)
        self.update_sum_reward_squares(state, action, r)

    def get_reward_table(self, state, action, next_states):
        L = []
        for next_state in next_states:
            if self.get_reward(state, action, next_state) > 0:
                L.append((next_state, self.get_reward(state, action, next_state)))
        return L

    # compute transition function P(s1, a, s2)
    def get_transition(self, s1, a, s2):
        v = (s1, a, s2)
        if v in self.P:
            return self.P[v]/float(self.get_visit_count(s1, a))
        return 0

    # update the transition model, keeping track of counts
    def update_transition(self, s1, a, s2):
        """ Update the transition statistics (including the count for state, (state, action), (state, action, next_state)) """
        self.increase_count(s1, a)
        self.P[(s1, a, s2)] = self.P.get((s1, a, s2), 0) + 1

    # update both reward and transition
    def update_reward_and_transition(self, state, action, next_state, reward):
        self.update_transition(state, action, next_state)
        self.update_reward(state, action, next_state, reward)

    def get_transition_table(self, state, action, next_states):
        L = []
        for next_state in next_states:
            if self.get_transition(state, action, next_state) > 0:
                L.append((next_state, self.get_transition(state, action, next_state)))
        return L