import pygame
import time
import random
from methods import load_image, lawn_y, lawn_x


class Sun:
    image = pygame.transform.scale(load_image("images/sun.png"), (50, 50))

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

        self.sun_hitbox = pygame.rect.Rect(self.x, self.y, 50, 50)
        self.sun_color = pygame.color.Color((255, 255, 0))

        self.sprite = pygame.sprite.Sprite()
        self.sprite.image = Sun.image
        self.sprite.rect = self.sun_hitbox
        self._ = pygame.sprite.GroupSingle()
        self._.add(self.sprite)
        self.picked = False
        self.death_time = time.time()
        spawn_sound = pygame.mixer.Sound("models/sounds/sunspawn.mp3")
        spawn_sound.play()

    def draw(self, screen: pygame.Surface, is_show_hitbox=True):
        if is_show_hitbox and time.time() - self.death_time < 6:
            pygame.draw.rect(screen, self.sun_color, self.sun_hitbox, width=2)
        if time.time() - self.death_time < 6:
            self._.draw(screen)

    def is_clicked(self, mouse_pos):
        return self.sprite.rect.collidepoint(mouse_pos)


class FallingSun(Sun):
    def __init__(self):
        super().__init__(random.randint(250, 900), 0)
        self.falling_y = random.randint(50, 500)

    def draw(self, screen: pygame.Surface, is_show_hitbox=True):
        super().draw(screen, is_show_hitbox)
        self.y += 1 / 3
        self.sprite.rect.y = self.y
        if self.y >= self.falling_y:
            self.y = self.falling_y


class Pea:
    pass
