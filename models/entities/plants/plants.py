import pygame
from pvz import busy_lawns
from methods import load_image, lawn_x, lawn_y


class Plant:
    def __init__(self, health, cost):
        self.health = health
        self.cost = cost
        self.line = 0
        self.column = 0
        self._ = pygame.sprite.GroupSingle()
        self._.add(self.sprite)

    def draw(self, screen: pygame.Surface):
        if self.health > 0:
            self._.draw(screen)
        else:
            busy_lawns.remove([self.line, self.column])



class SunFlower(Plant):
    pass


class PeeShooter(Plant):
    pass


class Nut(Plant):
    pass


class TorchWood(Plant):
    pass


