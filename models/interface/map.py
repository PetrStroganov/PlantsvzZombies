import pygame
from methods import load_image


class Map:
    image = pygame.transform.scale(load_image("images/background.jpg"), (1000, 600))
    def __init__(self):
        self.map_hitbox = pygame.rect.Rect(0, 0, 1000, 600)
        self.map_color = pygame.color.Color((0, 120, 255))
        self.sprite = pygame.sprite.Sprite()
        self.sprite.image = Map.image
        self.sprite.rect = self.map_hitbox
        self._ = pygame.sprite.GroupSingle()
        self._.add(self.sprite)
        self.field = Field()

    def draw(self, screen: pygame.Surface, is_show_hitbox=True):
        if is_show_hitbox:
            pygame.draw.rect(screen, self.map_color, self.map_hitbox, width=2)
        self._.draw(screen)


class Field:
    CELL_SIZE = 100
    def __init__(self):
        self.field_hitbox = pygame.rect.Rect(250, 75, 710, 500)
        self.field_color = pygame.color.Color((0, 0, 255))
        self.field = [[None] * 8 for _ in range(6)]

    def draw(self, screen: pygame.Surface, is_show_hitbox=True):
        if is_show_hitbox:
            pygame.draw.rect(screen, self.field_color, self.field_hitbox, width=2)

