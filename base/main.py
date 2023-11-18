import pygame
import globals
import numpy as np
from board import Board

INPUT_MAP = {
    pygame.K_UP: 0,
    pygame.K_DOWN: 1,
    pygame.K_LEFT: 2,
    pygame.K_RIGHT: 3
}

def handle_input(board):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                board.reset()
            
            elif event.key in INPUT_MAP.keys():
                dir = globals.DIRECTIONS_MAP[INPUT_MAP[event.key]]
                board.move(direction=dir)

def main():
    globals.init()

    pygame.init()
    screen = pygame.display.set_mode((globals.WIDTH, globals.HEIGHT))
    clock = pygame.time.Clock()
    running = True

    board = Board()

    while running:
        handle_input(board)
        
        if board.is_game_over():
            print("GAME OVER, HIGHEST TILE: ", np.max(board.board))
            running = False

        screen.fill(pygame.Color(globals.BG_COLOR))
        board.render(pygame, screen)

        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()

if __name__ == '__main__':
    main()