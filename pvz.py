from models.interface.hud import HUD
from models.interface.map import *


if __name__ == '__main__':
    pygame.init()
    size = w, h = 1000, 600
    screen = pygame.display.set_mode(size)
    map = Map()
    hud = HUD()
    field = Field()
    isShowHitbox = True
    clock = pygame.time.Clock()
    running = True
    while running:
        tick = clock.tick()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill((0, 0, 0))
        map.draw(screen)
        hud.draw(screen, is_show_hitbox=isShowHitbox)
        field.draw(screen)
        pygame.display.flip()