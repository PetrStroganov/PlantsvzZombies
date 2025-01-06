import pygame

from methods import load_image


class Zombie(pygame.sprite.Sprite):
    def __init__(self, health, line, x, y, image_width, image_height):
        super().__init__()
        self.health = health
        self.line = line
        self.x = x
        self.y = y
        self.change_x = 0.2
        self.angle = 0
        self.images = []
        self.current_frame = 0
        self.animation_speed = 5
        self.frame_count = 0
        self.image = None
        self.rect = None
        self.image_width = image_width
        self.image_height = image_height
        self.zombie_hitbox = pygame.Rect(self.x, self.y, 80, 100)
        self.zombie_color = pygame.color.Color(
            (255, 0, 0))
        self.sprite = pygame.sprite.Sprite()
        self._ = pygame.sprite.GroupSingle()
        self._.add(self.sprite)
        self.update_rect()
        self.eating = False

    def scale_image(self, image, target_width, target_height):
        """Масштабирование изображения."""
        return pygame.transform.scale(image, (target_width, target_height))

    def update_rect(self):
        if self.image:
            offset_x = self.image.get_width() // 2
            offset_y = self.image.get_height() // 2
            self.zombie_hitbox = pygame.Rect(self.x - 40, self.y - 50, 80,
                                             100)
            self.rect = self.image.get_rect(center=(self.x, self.y))
            self.sprite.rect = self.zombie_hitbox

    def update_image(self):
        if self.images:
            self.image = self.images[
                self.current_frame // self.animation_speed]
            self.update_rect()

    def draw(self, screen: pygame.Surface, is_show_hitbox=True):
        if self.health > 0:
            self._.draw(screen)
            if is_show_hitbox:
                pygame.draw.rect(screen, self.zombie_color, self.zombie_hitbox,
                                 width=1)

    def update(self, plants, zombie_killed, zombie_delay, game):

        if not self.eating:
            self.x -= self.change_x
        self.frame_count += 1
        if self.frame_count >= self.animation_speed:
            self.frame_count = 0
            self.current_frame = (self.current_frame + 1) % (
                        len(self.images) * self.animation_speed)

        self.update_image()

        if self.health <= 0:
            self.kill()
            zombie_killed += 1
            if zombie_delay > 5:
                zombie_delay -= 0.5
            return zombie_killed, zombie_delay, game


        self.eating = False
        self.angle = 0


        for plant in plants:
            if self.line == plant.line and pygame.sprite.collide_rect(self,
                                                                      plant):
                plant.health -= 0.2
                self.eating = True
                self.angle = 15
                break

        if self.x <= 200:
            game = False
        return zombie_killed, zombie_delay, game


class BasicZombie(Zombie):
    def __init__(self, line, x, y):
        image1 = load_image("images/zom1.png")
        image2 = load_image("images/zom2.png")
        target_width = 60
        target_height = int((60 / 767) * 1116)
        super().__init__(health=12, line=line, x=x, y=y,
                         image_width=target_width, image_height=target_height)
        self.images.append(
            self.scale_image(image1, target_width, target_height))
        for _ in range(3):
            self.images.append(
                self.scale_image(image1, target_width, target_height))
        for _ in range(3):
            self.images.append(
                self.scale_image(image2, target_width, target_height))
        self.update_image()
        self.sprite.image = self.image


class ConeZombie(Zombie):
    def __init__(self, line, x, y):
        image1 = load_image("images/cone1.png")
        image2 = load_image("images/cone2.png")
        target_width = 60
        target_height = int((60 / 766) * 1458)
        super().__init__(health=20, line=line, x=x, y=y,
                         image_width=target_width, image_height=target_height)
        self.images.append(
            self.scale_image(image1, target_width, target_height))
        for _ in range(3):
            self.images.append(
                self.scale_image(image1, target_width, target_height))
        for _ in range(3):
            self.images.append(
                self.scale_image(image2, target_width, target_height))
        self.update_image()
        self.sprite.image = self.image


class BucketZombie(Zombie):
    def __init__(self, line, x, y):
        image1 = load_image("images/buck1.png")
        image2 = load_image("images/buck2.png")
        target_width = 60
        target_height = int((60 / 786) * 1325)
        super().__init__(health=25, line=line, x=x, y=y,
                         image_width=target_width, image_height=target_height)
        self.images.append(
            self.scale_image(image1, target_width, target_height))
        for _ in range(3):
            self.images.append(
                self.scale_image(image1, target_width, target_height))
        for _ in range(3):
            self.images.append(
                self.scale_image(image2, target_width, target_height))
        self.update_image()
        self.sprite.image = self.image