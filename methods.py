import pygame
import sys
import os


def load_image(name):
    if not os.path.isfile(name):
        print(f"Файл с изображением '{name}' не найден")
        sys.exit()
    image = pygame.image.load(name)
    return image

def lawn_x(x):
    center_x = 0
    column = 0
    if 250 < x < 325:
        center_x = 280
        column = 1
    elif 325 <= x < 400:
        center_x = 360
        column = 2
    elif 400 <= x < 485:
        center_x = 440
        column = 3
    elif 485 <= x < 560:
        center_x = 520
        column = 4
    elif 560 <= x < 640:
        center_x = 600
        column = 5
    elif 640 <= x < 715:
        center_x = 675
        column = 6
    elif 715 <= x < 785:
        center_x = 750
        column = 7
    elif 785 <= x < 870:
        center_x = 830
        column = 8
    elif 870 <= x < 960:
        center_x = 920
        column = 9
    return center_x, column


def lawn_y(y):
    center_y = 0
    line = 0
    if 30 < y < 130:
        center_y = 80
        line = 1
    elif 130 <= y < 220:
        center_y = 170
        line = 2
    elif 220 <= y < 320:
        center_y = 270
        line = 3
    elif 320 <= y < 420:
        center_y = 370
        line = 4
    elif 420 <= y < 525:
        center_y = 475
        line = 5
    return center_y, line