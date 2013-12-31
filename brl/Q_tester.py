from QLearning import *
from ChainModel import *

ps = QLearning(SlipperyChainModel(0.1), 0.5, 0.8, 0)
for i in range(10000):
	print ps.next()
# expect state 5 to have the highest potential
# for state in ps.model.states:
# 	print ps.get_v(state)

# for i in range(1, 6):
# 	print "transition model"
# 	print ps.get_transition_table(ps.model.state[i], ps.model.act_a)
# 	print ps.get_transition_table(ps.model.state[i], ps.model.act_b)
# 	print "reward model"
# 	print ps.get_reward_table(ps.model.state[i], ps.model.act_a)
# 	print ps.get_reward_table(ps.model.state[i], ps.model.act_b)
