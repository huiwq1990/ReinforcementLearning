import os, sys
import pygame
from ChainModel import *
from ChainModel2 import *
from LoopModel import *
from board import Board

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 400
BG_COLOR = (0,0,0)

def run_game(model, record_file=None):
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    board = Board(model,300)
    
    if record_file != None:
        record = True
    else:
        record = False
        
    if record:
        record_file.write("state,action,reward,total\n")
    
    total = 0
    while True:
        time_passed = clock.tick(50)
        
        state = board.model.current_state
        action = None
        reward = None
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    action = 0
                    reward = board.actionA()
                elif event.key == pygame.K_LEFT:
                    action = 1
                    reward = board.actionB()
                elif event.key == pygame.K_UP:
                    action = 2
                    reward = board.actionC()
                elif event.key == pygame.K_DOWN:
                    action = 3
                    reward = board.actionD()
                
        if record and reward != None:
            total += reward
            record_file.write(str(state.get_id())+","+str(action)+","+str(reward)+","+str(total)+"\n")
        
        screen.fill(BG_COLOR)
        board.display(screen)
        
        pygame.display.flip()
        
#if __name__ == '__main__':
#    if len(sys.argv) > 1:
#        f = open(sys.argv[1],'w')
#        run_game(f)
#    else:    
#        run_game()
