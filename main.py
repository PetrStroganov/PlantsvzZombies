import pygame
from pvz import game

screen_dict = {1: game}

if __name__ == '__main__':
    pygame.init()
    size = w, h = 1000, 600
    screen = pygame.display.set_mode(size)
    screen_id = 1
    while screen_id:
        screen_id = screen_dict[screen_id](screen)
