from RL_game import *
from LoopModel import *

if __name__ == '__main__':
    if len(sys.argv) > 1:
        f = open(sys.argv[1],'w')
        run_game(LoopModelDiffTrans(), f)
    else:    
        run_game(LoopModelDiffTrans())
