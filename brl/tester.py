from LoopModel import *
from ChainModel import *
from ChainModel2 import *
from PrioritizedSweeping import *
from QLearning import *
from QLearn import *
from PrioritizedQLearning import *
import RL_trials

# model = ChainModel()
# # ps = QLearn(model, model.actions)
# ps = QLearning(model, 0.2, 0.2, 0.99)
# # ps = PrioritizedSweeping(model, 3)
# #ps = PrioritizedQLearning(model)

# total = 0
# for i in range(1000):
# 	(action, reward, state) = ps.next() 
# 	# print action, reward, state
# 	total = total + reward
# print "total", total / float(1000)
# total = 0
# model.current_state = model.state[1]
# for i in range(10000):
# 	(action, reward, state) = ps.next() 
# 	total = total + reward
# print "total", total / float(10000)
# total = 0
# model.current_state = model.state[1]
# for i in range(10000):
# 	(action, reward, state) = ps.next() 
# 	total = total + reward
# print "total", total/ float(10000)
# total = 0
# model.current_state = model.state[1]
# for i in range(10000):
# 	(action, reward, state) = ps.next() 
# 	total = total + reward
# print "total", total / float(10000)
# total = 0
# model.current_state = model.state[1]
# for i in range(10000):
# 	(action, reward, state) = ps.next() 
# 	total = total + reward
# print "total", total / float(10000)
# total = 0
# model.current_state = model.state[1]
# for i in range(10000):
# 	(action, reward, state) = ps.next() 
# 	total = total + reward
# print "total", total / float(10000)
# total = 0
# model.current_state = model.state[1]
# for i in range(10000):
# 	(action, reward, state) = ps.next() 
# 	total = total + reward
# 	# print action, state
# print "total", total / float(10000)

avgs = RL_trials.run_trials(10, 8, 1000, "BayesDP", "Chain")
for (i,avg) in enumerate(avgs):
    print "Phase " + str(i+1) + ": " + str(avg) 