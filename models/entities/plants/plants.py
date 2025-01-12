import pygame
import time
from models.map.other import Sun, Pea
from methods import load_image


class Plant:
    def __init__(self, health, cost, x, y):
        self.x = x
        self.y = y
        self.health = health
        self.cost = cost
        self.line = 0
        self.column = 0
        self.fire = False

    def draw(self, screen: pygame.Surface, busy_lawns, is_show_hitbox=True):
        if self.health > 0:
            self._.draw(screen)
        else:
            if (self.column, self.line) in busy_lawns:
                busy_lawns.remove((self.column, self.line))
            self.sprite.kill()


class SunFlower(Plant):
    image1 = pygame.transform.scale(load_image("images/sun1.png"), (80, 80))
    image2 = pygame.transform.scale(load_image("images/sun2.png"), (80, 80))

    def __init__(self, x, y):
        super().__init__(health=75, cost=50, x=x, y=y)
        self.sprite = pygame.sprite.Sprite()
        self.sprite.image = SunFlower.image1
        self.plant_hitbox = pygame.rect.Rect(self.x + 5, self.y + 10, 70, 80)
        self.plant_color = pygame.color.Color((100, 255, 0))
        self.sprite.rect = self.plant_hitbox
        self._ = pygame.sprite.GroupSingle()
        self._.add(self.sprite)
        self.spawn_time = time.time()
        self.animation_time1 = time.time()
        self.animation_time2 = time.time() + 0.25

    def draw(self, screen: pygame.Surface, busy_lawns, is_show_hitbox=True):
        super().draw(screen, busy_lawns, is_show_hitbox)
        if is_show_hitbox:
            pygame.draw.rect(screen, self.plant_color, self.plant_hitbox, width=1)
        if time.time() - self.animation_time1 > 0.5:
            self.sprite.image = SunFlower.image2
            self.animation_time1 = time.time()
        if time.time() - self.animation_time2 > 0.5:
            self.sprite.image = SunFlower.image1
            self.animation_time2 = time.time()

    def generate_sun(self, suns):
        if time.time() - self.spawn_time > 10:
            generated_sun = Sun(self.x + 20, self.y - 10)
            suns.append(generated_sun)
            self.spawn_time = time.time()


class PeaShooter(Plant):
    image1 = pygame.transform.scale(load_image("images/pea1.png"), (140, 90))
    image2 = pygame.transform.scale(load_image("images/pea2.png"), (140, 90))
    image3 = pygame.transform.scale(load_image("images/pea3.png"), (140, 90))

    def __init__(self, x, y):
        super().__init__(health=100, cost=100, x=x, y=y)
        self.sprite = pygame.sprite.Sprite()
        self.sprite.image = PeaShooter.image1
        self.plant_hitbox = pygame.rect.Rect(self.x, self.y + 10, 80, 90)
        self.plant_color = pygame.color.Color((100, 255, 0))
        self.sprite.rect = self.plant_hitbox.move(-20, 0)
        self._ = pygame.sprite.GroupSingle()
        self._.add(self.sprite)
        self.shoot_time = time.time() - 4
        self.animation_time3 = time.time()
        self.animation_time2 = time.time() + 0.25
        self.animation_time1 = time.time() + 0.5

    def draw(self, screen: pygame.Surface, busy_lawns, is_show_hitbox=True):
        super().draw(screen, busy_lawns, is_show_hitbox)
        if is_show_hitbox:
            pygame.draw.rect(screen, self.plant_color, self.plant_hitbox, width=1)
        if time.time() - self.animation_time1 > 0.75:
            self.sprite.image = PeaShooter.image1
            self.animation_time1 = time.time()
        if time.time() - self.animation_time2 > 0.75:
            self.sprite.image = PeaShooter.image3
            self.animation_time2 = time.time()
        if time.time() - self.animation_time3 > 0.75:
            self.sprite.image = PeaShooter.image2
            self.animation_time3 = time.time()

    def shoot(self, peas, zombies):
        for zombie in zombies:
            if self.line == zombie.line and time.time() - self.shoot_time > 3:
                generated_pea = Pea(self.x + 20, self.y + 10)
                peas.append(generated_pea)
                self.shoot_time = time.time()


class Nut(Plant):
    image1 = pygame.transform.scale(load_image("images/nut1.png"), (70, 80))
    image2 = pygame.transform.scale(load_image("images/nut2.png"), (70, 80))
    image3 = pygame.transform.scale(load_image("images/nut3.png"), (70, 80))

    def __init__(self, x, y):
        super().__init__(health=300, cost=50, x=x, y=y)
        self.sprite = pygame.sprite.Sprite()
        self.sprite.image = Nut.image1
        self.plant_hitbox = pygame.rect.Rect(self.x + 5, self.y + 10, 70, 80)
        self.plant_color = pygame.color.Color((100, 255, 0))
        self.sprite.rect = self.plant_hitbox
        self._ = pygame.sprite.GroupSingle()
        self._.add(self.sprite)
        self.shoot_time = time.time()
        self.animation_time3 = time.time()
        self.animation_time2 = time.time() + 0.4
        self.animation_time1 = time.time() + 0.8

    def draw(self, screen: pygame.Surface, busy_lawns, is_show_hitbox=True):
        super().draw(screen, busy_lawns, is_show_hitbox)
        if is_show_hitbox:
            pygame.draw.rect(screen, self.plant_color, self.plant_hitbox, width=1)
        if time.time() - self.animation_time1 > 1.2:
            self.sprite.image = Nut.image1
            self.animation_time1 = time.time()
        if time.time() - self.animation_time2 > 1.2:
            self.sprite.image = Nut.image3
            self.animation_time2 = time.time()
        if time.time() - self.animation_time3 > 1.2:
            self.sprite.image = Nut.image2
            self.animation_time3 = time.time()


class TorchWood(Plant):
    image1 = pygame.transform.scale(load_image("images/tree1.png"), (80, 90))
    image2 = pygame.transform.scale(load_image("images/tree2.png"), (80, 90))
    image3 = pygame.transform.scale(load_image("images/tree3.png"), (80, 90))

    def __init__(self, x, y):
        super().__init__(health=150, cost=175, x=x, y=y)
        self.sprite = pygame.sprite.Sprite()
        self.sprite.image = TorchWood.image1
        self.plant_hitbox = pygame.rect.Rect(self.x, self.y + 10, 80, 90)
        self.plant_color = pygame.color.Color((100, 255, 0))
        self.sprite.rect = self.plant_hitbox
        self._ = pygame.sprite.GroupSingle()
        self._.add(self.sprite)
        self.fire = True
        self.shoot_time = time.time()
        self.animation_time3 = time.time()
        self.animation_time2 = time.time() + 0.2
        self.animation_time1 = time.time() + 0.4

    def draw(self, screen: pygame.Surface, busy_lawns, is_show_hitbox=True):
        super().draw(screen, busy_lawns, is_show_hitbox)
        if is_show_hitbox:
            pygame.draw.rect(screen, self.plant_color, self.plant_hitbox, width=1)
        if time.time() - self.animation_time1 > 0.6:
            self.sprite.image = TorchWood.image1
            self.animation_time1 = time.time()
        if time.time() - self.animation_time2 > 0.6:
            self.sprite.image = TorchWood.image3
            self.animation_time2 = time.time()
        if time.time() - self.animation_time3 > 0.6:
            self.sprite.image = TorchWood.image2
            self.animation_time3 = time.time()

