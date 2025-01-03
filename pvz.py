from models.interface.hud import HUD
from models.interface.map import *
from models.cursor import Cursor
from models.map.other import *

EXIT, MAIN_SCREEN = 0, 1
busy_lawns = []
suns = []


def game(screen):
    global mouse_x, mouse_y
    map = Map()
    hud = HUD()
    field = Field()

    isShowHitbox = True
    cursor = Cursor()
    pygame.mouse.set_visible(False)
    running = True
    suns_count = 250
    font = pygame.font.SysFont(None, 40)
    falling_time = time.time()
    seed = None
    while running:
        # Обрабатываем события
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return EXIT
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F1:
                    isShowHitbox = not isShowHitbox
            if event.type == pygame.MOUSEBUTTONDOWN:
                clicked_pos = event.pos
            if event.type == pygame.MOUSEMOTION:
                cursor.move(*event.pos)
        screen.fill((100, 100, 100))
        map.draw(screen, is_show_hitbox=isShowHitbox)
        hud.draw(screen, is_show_hitbox=isShowHitbox)
        field.draw(screen, is_show_hitbox=isShowHitbox)
        if time.time() - falling_time >= 1:
            falling_sun = FallingSun()
            suns.append(falling_sun)
            falling_time = time.time()
        for sun in suns:
            sun.draw(screen)
            if sun.is_clicked(clicked_pos):
                if not sun.picked:
                    sun.picked = True
                    suns_count += 25
                    suns.remove(sun)
                    break
        cursor.draw(screen)
        suns_text = font.render(str(suns_count), True, (0, 0, 0))
        screen.blit(suns_text, (45, 82))
        pygame.display.flip()