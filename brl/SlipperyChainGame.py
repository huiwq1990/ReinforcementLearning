from RL_game import *
from ChainModel import *

if __name__ == '__main__':
    if len(sys.argv) > 1:
        f = open(sys.argv[1],'w')
        run_game(SlipperyChainModel(), f)
    else:    
        run_game(SlipperyChainModel())
