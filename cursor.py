import pygame
from methods import load_image


class Cursor:
    def __init__(self):
        self.sprite = pygame.sprite.Sprite()
        self.sprite.image = load_image("images/crosshair.png")
        self.sprite.rect = self.sprite.image.get_rect()
        self._ = pygame.sprite.GroupSingle()
        self._.add(self.sprite)

    # Движение мышки
    def move(self, x: int, y: int):
        self.sprite.rect.x = x - 25
        self.sprite.rect.y = y - 25

    # Отрисовка
    def draw(self, screen: pygame.Surface):
        self._.draw(screen)
