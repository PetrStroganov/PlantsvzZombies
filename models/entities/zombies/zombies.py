import pygame
import time
from methods import load_image


class Zombie(pygame.sprite.Sprite):
    def __init__(self, health, line, x, y):
        super().__init__()
        self.health = health
        self.line = line
        self.x = x
        self.y = y
        self.change_x = 0.025
        self.eating = False
        self.sprite = pygame.sprite.Sprite()
        self.sprite.image = BasicZombie.image1
        self.zombie_hitbox = pygame.Rect(self.x, self.y, 80, 130)
        self.zombie_color = pygame.color.Color((255, 0, 0))
        self.sprite.rect = self.zombie_hitbox
        self.alive = True
        self.killed = False
        self.zombie_killed = 0
        self._ = pygame.sprite.GroupSingle()
        self._.add(self.sprite)

    def draw(self, screen: pygame.Surface, plants, is_show_hitbox=True):
        if self.alive:
            self._.draw(screen)
            if not self.eating:
                self.x -= self.change_x
                self.sprite.rect.x = self.x
            if is_show_hitbox:
                pygame.draw.rect(screen, self.zombie_color, self.zombie_hitbox, width=1)
            if self.health <= 0:
                self.alive = False
                self.sprite.kill()
            for plant in plants:
                if self.line == plant.line and pygame.sprite.spritecollide(self.sprite, plant._, False):
                    plant.health -= 0.02
                    self.eating = True
                    if plant.health <= 0:
                        self.eating = False

    def game_over(self):
        if self.x <= 200:
            return True

    def zombies_killed(self, zombie_killed: int):
        self.zombie_killed = zombie_killed
        if not self.killed and not self.alive:
            self.killed = True
            self.zombie_killed += 1
        return self.zombie_killed


class BasicZombie(Zombie):
    image1 = pygame.transform.scale(load_image("images/zom1.png"), (80, 130))
    image2 = pygame.transform.scale(load_image("images/zom2.png"), (80, 130))

    def __init__(self, line, x, y):
        super().__init__(health=12, line=line, x=x, y=y)
        self.animation_time1 = time.time()
        self.animation_time2 = time.time() + 0.25

    def draw(self, screen: pygame.Surface, plants, is_show_hitbox=True):
        super().draw(screen, plants, is_show_hitbox)
        if time.time() - self.animation_time1 > 0.5:
            self.sprite.image = BasicZombie.image2
            self.animation_time1 = time.time()
        if time.time() - self.animation_time2 > 0.5:
            self.sprite.image = BasicZombie.image1
            self.animation_time2 = time.time()


class ConeZombie(Zombie):
    image1 = pygame.transform.scale(load_image("images/cone1.png"), (80, 130))
    image2 = pygame.transform.scale(load_image("images/cone2.png"), (80, 130))

    def __init__(self, line, x, y):
        super().__init__(health=20, line=line, x=x, y=y)
        self.sprite.image = ConeZombie.image1
        self.animation_time1 = time.time()
        self.animation_time2 = time.time() + 0.25

    def draw(self, screen: pygame.Surface, plants, is_show_hitbox=True):
        super().draw(screen, plants, is_show_hitbox)
        if time.time() - self.animation_time1 > 0.5:
            self.sprite.image = ConeZombie.image2
            self.animation_time1 = time.time()
        if time.time() - self.animation_time2 > 0.5:
            self.sprite.image = ConeZombie.image1
            self.animation_time2 = time.time()


class BucketZombie(Zombie):
    image1 = pygame.transform.scale(load_image("images/buck1.png"), (80, 130))
    image2 = pygame.transform.scale(load_image("images/buck2.png"), (90, 130))

    def __init__(self, line, x, y):
        super().__init__(health=25, line=line, x=x, y=y)
        self.sprite.image = BucketZombie.image1
        self.animation_time1 = time.time()
        self.animation_time2 = time.time() + 0.25

    def draw(self, screen: pygame.Surface, plants, is_show_hitbox=True):
        super().draw(screen, plants, is_show_hitbox)
        if time.time() - self.animation_time1 > 0.5:
            self.sprite.image = BucketZombie.image2
            self.animation_time1 = time.time()
        if time.time() - self.animation_time2 > 0.5:
            self.sprite.image = BucketZombie.image1
            self.animation_time2 = time.time()
