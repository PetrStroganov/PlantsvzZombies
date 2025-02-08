import pygame
from pvz import game, game_over, game_win, menu

if __name__ == '__main__':
    pygame.init()
    size = w, h = 1000, 600
    screen = pygame.display.set_mode(size)
    screen_id = 4
    screen_dict = {
        1: game,
        2: game_over,
        3: game_win,
        4: menu
    }
    while screen_id:
        screen_id = screen_dict[screen_id](screen)
