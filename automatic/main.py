import pygame
import globals
import numpy as np
import multiprocessing as mp
import math
import json

from bot import Bot
from board import Board

INPUT_MAP = {
    pygame.K_UP: 0,
    pygame.K_DOWN: 1,
    pygame.K_LEFT: 2,
    pygame.K_RIGHT: 3
}

DIRECTIONS_MAP = {
    0: "up",
    1: "down",
    2: "left",
    3: "right",
}

BOT = True

def handle_input(board, event):    
    if event.type == pygame.KEYUP:
        if event.key == pygame.K_SPACE:
            board.reset()
        
        elif event.key in INPUT_MAP.keys():
            dir = DIRECTIONS_MAP[INPUT_MAP[event.key]]
            board.move(direction=dir)

def main():
    globals.init()

    pygame.init()
    screen = pygame.display.set_mode((globals.WIDTH, globals.HEIGHT))
    clock = pygame.time.Clock()

    global pool
    mp.freeze_support()
    mp.set_start_method('spawn')

    board = Board()
    bot = Bot()
    running = True

    pool = mp.Pool(processes=8)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if not BOT: handle_input(board, event)

        if BOT:
            action = bot.get_best_action(board, depth=1, pool=pool)
            board.move(DIRECTIONS_MAP[action])
        
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
