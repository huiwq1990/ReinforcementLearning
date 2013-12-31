from RL_game import *
from ChainModel import *

if __name__ == '__main__':
    
    f = open('hggame','w')
    run_game(SlipperyChainModel(), f)
   