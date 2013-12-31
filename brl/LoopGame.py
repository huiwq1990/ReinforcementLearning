from RL_game import *
from LoopModel import *

if __name__ == '__main__':
    if len(sys.argv) > 1:
        f = open(sys.argv[1],'w')
        run_game(LoopModel(), f)
    else:    
        run_game(LoopModel())
