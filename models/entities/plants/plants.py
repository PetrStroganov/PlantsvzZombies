import pygame
from pvz import *
from methods import load_image, lawn_x, lawn_y


class Plant:
    def __init__(self, health, cost, x, y):
        self.x = x
        self.y = y
        self.health = health
        self.cost = cost
        self.line = 0
        self.column = 0

    def draw(self, screen: pygame.Surface, is_show_hitbox=True):
        if self.health > 0:
            self._.draw(screen)
        else:
            busy_lawns.remove([self.line, self.column])

    def planting(self, line, column, center_x, center_y):
        self.line = line
        self.column = column
        self.center_x = center_x
        self.center_y = center_y


class SunFlower(Plant):
    image = pygame.transform.scale(load_image("images/sun1.png"), (90, 90))
    def __init__(self, x, y):
        super().__init__(health=75, cost=50, x=x, y=y)
        self.sprite = pygame.sprite.Sprite()
        self.sprite.image = SunFlower.image
        self.plant_hitbox = SunFlower.image.get_rect(topleft=(x, y))
        self.plant_color = pygame.color.Color((100, 255, 0))
        self.sprite.rect = self.plant_hitbox
        self._ = pygame.sprite.GroupSingle()
        self._.add(self.sprite)
        self.spawn_time = time.time()

    def generate_sun(self):
        super().draw(is_show_hitbox=True)
        if time.time() - self.spawn_time > 10:
            sun = Sun(self.center_x + 20, self.center_y - 10)
            suns.append(sun)
            self.spawn_time = time.time()



class PeeShooter(Plant):
    pass


class Nut(Plant):
    pass


class TorchWood(Plant):
    pass
