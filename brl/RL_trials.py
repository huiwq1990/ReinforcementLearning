import sys
from PrioritizedSweeping import *
from PrioritizedSweepingPolicy import *
from PrioritizedSweepingHeuristics import *
from PrioritizedQLearning import *
from QLearning import *
from QLearn import *
from ChainModel import *
from ChainModel2 import *
from LoopModel import *
from BayesPrioritizedSweeping import *

def get_learner(algorithm, model):
    if algorithm == "QLearning":
        if model.name == "SlipperyChain":
            return QLearning(model)
        elif model.name == "Loop":
            return QLearning(model)
        elif model.name == "LoopDeadEnd":
            return QLearning(model,0.2,0.99,0.001,0.999)
        elif model.name == "LoopDiffTrans":
            return QLearning(model,0.3,0.2,0.2,0.999)
        else:
            return QLearning(model)
            
    elif algorithm == "PrioritizedSweeping":
        if model.name == "SlipperyChain":
            return PrioritizedSweeping(model,2,0.2,0.99,0.9)
        elif model.name == "Loop":
            return PrioritizedSweeping(model,2,0.999,0.99,0.9)
        elif model.name == "LoopDeadEnd":
            return PrioritizedSweeping(model,5,0.999,0.99,0.9)
        elif model.name == "LoopDiffTrans":
            return PrioritizedSweeping(model,5,0.8,0.99,0.9)
        else:
            return PrioritizedSweeping(model)
        
        
    elif algorithm == "PrioritizedSweepingPolicy":
        return PrioritizedSweepingPolicy(model)
        
    elif algorithm == "PrioritizedSweepingHeuristics":
        if model.name == "SlipperyChain":
            return PrioritizedSweepingHeuristics(model,2,0.9,0.99,0.9)
        elif model.name == "Loop":
            return PrioritizedSweepingHeuristics(model,2,0.9,0.99,0.9)
        elif model.name == "LoopDeadEnd":
            return PrioritizedSweepingHeuristics(model,1,0.999,0.999,0.999)
        elif model.name == "LoopDiffTrans":
            return PrioritizedSweepingHeuristics(model,5,0.9,0.99,0.9)
        else:
            return PrioritizedSweepingHeuristics(model)
        
    elif algorithm == "QLearn":
        return QLearn(model)
        
    elif algorithm == "PrioritizedQLearning":
        return PrioritizedQLearning(model)
        
    elif algorithm == "BayesDP":
        if model.name == "SlipperyChain":
            return BayesPrioritizedSweeping(model,10,0.9,1,0.2,20)
        elif model.name == "Loop":
            return BayesPrioritizedSweeping(model,10,0.9,1,0.2,20)
        elif model.name == "LoopDeadEnd":
            return BayesPrioritizedSweeping(model)
        elif model.name == "LoopDiffTrans":
            return BayesPrioritizedSweeping(model,1,0.2,1,0.2,20)
        else:
            return BayesPrioritizedSweeping(model)
            
    else:
        raise Exception(algorithm + " not found")

def get_model(model_name):
    if model_name == "Chain":
        return ChainModel()
    elif model_name == "SlipperyChain":
        return SlipperyChainModel()
    elif model_name == "Chain2":
        return ChainModel2()
    elif model_name == "Loop":
        return LoopModel()
    elif model_name == "LoopDeadEnd":
        return LoopModelDeadEnd()
    elif model_name == "LoopDiffTrans":
        return LoopModelDiffTrans()
    elif model_name == "SpecialLoop":
        return SpecialLoopModel()
    else:
        raise Exception(model_name+ " not found")

def run_trials(num_trials, num_phases, num_steps, algorithm = "QLearning", model_name = "Chain"):
    learners = []
    for i in range(num_trials):
        m = get_model(model_name)
        #learners.append(QLearn(m,m.actions))
        learners.append(get_learner(algorithm, m))

    phase_avgs = []
    for i in range(num_phases):
        totals = []
        for learner in learners:
            total = 0
            for j in range(num_steps):
                (action, reward, next_state) = learner.next()
                total += reward
            totals.append(total)

        phase_avgs.append(sum(totals)/(1.0*len(totals)))

        for learner in learners:
            learner.model.reset()

    return phase_avgs

if __name__ == '__main__':
    if len(sys.argv) >= 4:
        model_name = "Chain"
        if len(sys.argv) == 6:
            model_name = sys.argv[5]
        avgs = run_trials(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), sys.argv[4], model_name)
        for (i,avg) in enumerate(avgs):
            print "Phase " + str(i+1) + ": " + str(avg)
    else:
        print "Invalid input."
