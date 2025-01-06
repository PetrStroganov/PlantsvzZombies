import pygame
from methods import load_image


class HUD:
    image = pygame.transform.scale(load_image("images/menu_vertical.png"), (130, 600))

    def __init__(self):
        self.menu_hitbox = pygame.rect.Rect(0, 0, 131, 600)
        self.menu_color = pygame.color.Color((100, 255, 51))
        self.sprite = pygame.sprite.Sprite()
        self.sprite.image = HUD.image
        self.sprite.rect = self.menu_hitbox
        self._ = pygame.sprite.GroupSingle()
        self._.add(self.sprite)

    def draw(self, screen: pygame.Surface, is_show_hitbox=True):
        if is_show_hitbox:
            pygame.draw.rect(screen, self.menu_color, self.menu_hitbox, width=2)
        self._.draw(screen)
