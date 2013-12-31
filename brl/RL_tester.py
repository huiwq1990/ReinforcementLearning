import sys
from PrioritizedSweeping import *
from QLearning import *
from ChainModel import *
from ChainModel2 import *
from LoopModel import *

def invalid():
    print "Input not valid."
    print "Type 'help' for options."
    
def help():
    print
    print "learning_alg [args]"
    print
    learning_alg_help()
    print
    model_help()
    print
    
def model_help():
    print "Model Options:"
    print "   ChainModel - 'cm'"
    print "   SlipperyChainModel - 'scm'"
    print "   LoopModel - 'lm'"
    
def learning_alg_help():
    print "Learning Algorithm Options:"
    print
    print "   "+ps_args()
    print
    print "   "+ql_args()
    
def ps_args():
    return "PrioritizedSweeping - 'ps' model num_steps [file_name k e]"

def ql_args():
    return "Q-Learning - 'ql' model num_steps [file_name learning_rate discount_rate e]"

def parse_model(s):
    if s == 'cm':
        return ChainModel()
    elif s == 'scm':
        return SlipperyChainModel()
    elif s == 'lm':
        return LoopModel()
    else:
        invalid()

def ps(args):
    if len(args) >= 2:
        model = parse_model(args[0])
        num_steps = int(args[1])
        
        if len(args) >= 3:
            record_file = open(args[2], 'w')
        else:
            record_file = None
            
        if len(args) >= 4:
            k = float(args[3])
        else:
            k = None
       
        if len(args) >= 5:
            e = float(args[4])
        else:
            e = None
        
        if k != None and e !=None:
            ps = PrioritizedSweeping(model, k, e)
        elif k != None:
            ps = PrioritizedSweeping(model, k)
        else:
            ps = PrioritizedSweeping(model)
        
        if record_file != None:
            run(ps, num_steps, record_file)
        else:
            run(ps, num_steps)
    else:
        invalid()
    
def ql(args):
    if len(args) >= 2:
        model = parse_model(args[0])
        num_steps = int(args[1])
        
        if len(args) >= 3:
            record_file = open(args[2], 'w')
        else:
            record_file = None
            
        if len(args) >= 4:
            learning_rate = float(args[3])
        else:
            learning_rate = None
       
        if len(args) >= 5:
            discount_rate = float(args[4])
        else:
            discount_rate = None
            
        if len(args) >= 6:
            e = float(args[5])
        else:
            e = None
        
        if learning_rate != None and discount_rate !=None and e != None:
            ql = QLearning(model, learning_rate, discount_rate, e)
        elif learning_rate != None and discount_rate !=None:
            ql = QLearning(model, learning_rate, discount_rate)
        elif learning_rate != None:
            ql = QLearning(model, learning_rate)
        else:
            ql = QLearning(model)
        
        if record_file != None:
            run(ql, num_steps, record_file)
        else:
            run(ql, num_steps)
    else:
        invalid()
    
def run(l_alg, num_steps, record_file=None):
    if record_file != None:
        record = True
    else:
        record = False
    
    if record:
        record_file.write("state,action,reward,total\n")
        
    total = 0
    state = l_alg.model.current_state
    for i in range(num_steps):
        (action, reward, next_state) = l_alg.next()
        if record:
            record_file.write(str(state.get_id())+","+str(action.get_id())+","+str(reward)+","+str(total)+"\n")
        state = next_state
        total += reward
   
    print total

if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == 'help':
            help()
        elif sys.argv[1] == 'ps':
            ps(sys.argv[2:])
        elif sys.argv[1] == 'ql':
            ql(sys.argv[2:])
        else:
            invalid()
    else:
        invalid()
