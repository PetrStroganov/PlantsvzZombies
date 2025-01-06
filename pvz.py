from models.entities.zombies.zombies import *
from models.entities.plants.plants import *
from models.interface.hud import HUD
from models.interface.map import *
from models.cursor import Cursor
from models.map.other import *
from methods import load_image
import sys

EXIT, MAIN_SCREEN, GAME_OVER = 0, 1, 2
busy_lawns = []
suns = []
plants = []
zombies = []
zombie_killed = 0
zombie_delay = 10
game_active = True


def game(screen):
    global busy_lawns, suns, plants, zombies, zombie_killed, zombie_delay, game_active

    plants_vs_zombies_map = Map()
    hud = HUD()
    field = Field()
    isShowHitbox = True
    cursor = Cursor()
    pygame.mouse.set_visible(False)
    running = True
    suns_count = 250
    font = pygame.font.SysFont(None, 40)
    falling_time = time.time()
    pygame.mixer.music.load("models/sounds/grasswalk.mp3")
    plant_sound = pygame.mixer.Sound("models/sounds/seed.mp3")
    pygame.mixer.music.play(-1)
    seed = None
    drag_plant_image = None
    dragging = False
    drag_x, drag_y = -100, -100
    zombie_spawn_time = time.time()
    font = pygame.font.Font(None, 36)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return EXIT
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F1:
                    isShowHitbox = not isShowHitbox
            if event.type == pygame.MOUSEBUTTONDOWN:
                clicked_pos = event.pos
                drag_x, drag_y = -100, -100
                for sun in suns:
                    if sun.is_clicked(clicked_pos):
                        if not sun.picked:
                            sun.picked = True
                            suns_count += 25
                            suns.remove(sun)
                            break
                if not dragging:
                    if 30 <= clicked_pos[0] <= 110 and 120 <= clicked_pos[1] <= 230:
                        dragging = True
                        seed = "SunFlower"
                        drag_plant_image = pygame.transform.scale(load_image("images/sun2.png"), (90, 90))
                        drag_plant_image.set_alpha(128)
                        plant_sound.play()
                    if 30 <= clicked_pos[0] <= 110 and 240 <= clicked_pos[1] <= 350:
                        dragging = True
                        seed = "PeeShooter"
                        drag_plant_image = pygame.transform.scale(load_image("images/pea1.png"), (170, 90))
                        drag_plant_image.set_alpha(128)
                        plant_sound.play()
                    if 30 <= clicked_pos[0] <= 110 and 360 <= clicked_pos[1] <= 470:
                        dragging = True
                        seed = "Nut"
                        drag_plant_image = pygame.transform.scale(load_image("images/nut1.png"), (70, 80))
                        drag_plant_image.set_alpha(128)
                        plant_sound.play()
                    if 30 <= clicked_pos[0] <= 110 and 480 <= clicked_pos[1] <= 590:
                        dragging = True
                        seed = "TorchWood"
                        drag_plant_image = pygame.transform.scale(load_image("images/tree3.png"), (80, 90))
                        drag_plant_image.set_alpha(128)
                        plant_sound.play()
            if event.type == pygame.MOUSEBUTTONUP:
                if dragging:
                    dragging = False
                    if 250 <= drag_x + 40 <= 960 and 75 <= drag_y + 50 <= 575:
                        x_plant = lawn_x(drag_x + 40)[0]
                        y_plant = lawn_y(drag_y + 50)[0]
                        if seed == "SunFlower" and (
                        lawn_x(drag_x + 40)[1], lawn_y(drag_y + 50)[1]) not in busy_lawns and suns_count >= 50:
                            suns_count -= 50
                            busy_lawns.append((lawn_x(drag_x + 40)[1], lawn_y(drag_y + 50)[1]))
                            plants.append(SunFlower(x_plant, y_plant))
                            plant_sound.play()
            if event.type == pygame.MOUSEMOTION:
                cursor.move(*event.pos)
                if dragging:
                    drag_x = event.pos[0] - 40
                    drag_y = event.pos[1] - 50
        screen.fill((100, 100, 100))
        plants_vs_zombies_map.draw(screen, is_show_hitbox=isShowHitbox)
        hud.draw(screen, is_show_hitbox=isShowHitbox)
        field.draw(screen, is_show_hitbox=isShowHitbox)
        if time.time() - falling_time >= 10:
            falling_sun = FallingSun()
            suns.append(falling_sun)
            falling_time = time.time()
        for plant in plants:
            plant.draw(screen, is_show_hitbox=isShowHitbox)
            if isinstance(plant, SunFlower):
                new_sun = plant.generate_sun()
                if new_sun:
                    suns.append(new_sun)
        for sun in suns:
            sun.draw(screen, is_show_hitbox=isShowHitbox)
        cursor.draw(screen)
        if dragging and drag_plant_image is not None:
            screen.blit(drag_plant_image, (drag_x, drag_y))

        if time.time() - zombie_spawn_time >= zombie_delay:
            line = random.randint(1, 5)
            x = 1000
            y = 100 + (line-1) * 100
            zombie_type = random.choice([BasicZombie, ConeZombie, BucketZombie])
            zombies.append(zombie_type(line, x, y))
            zombie_spawn_time = time.time()

        for zombie in zombies:
            zombie.draw(screen, is_show_hitbox=isShowHitbox)
            zombie_killed, zombie_delay, game_active = zombie.update(plants, zombie_killed, zombie_delay, game_active)
            if not game_active:
              return GAME_OVER
        zombies[:] = [zombie for zombie in zombies if zombie.health > 0]

        suns_text = font.render(str(suns_count), True, (0, 0, 0))
        screen.blit(suns_text, (45, 82))
        pygame.display.flip()

def game_over(screen):
    global busy_lawns, suns, plants, zombies, zombie_killed, zombie_delay, game_active
    cursor = Cursor()
    pygame.mouse.set_visible(False)
    font = pygame.font.Font(None, 72)
    text = font.render("Game Over", True, (255, 0, 0))
    text_rect = text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 50))

    button_font = pygame.font.Font(None, 36)
    button_text = button_font.render("Play Again", True, (255, 255, 255))
    button_rect = button_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 50))
    button_color = (100, 100, 100)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return EXIT
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if button_rect.collidepoint(mouse_pos):
                    busy_lawns = []
                    suns = []
                    plants = []
                    zombies = []
                    zombie_killed = 0
                    zombie_delay = 10
                    game_active = True
                    return MAIN_SCREEN
            if event.type == pygame.MOUSEMOTION:
                cursor.move(*event.pos)
        screen.fill((0, 0, 0))
        screen.blit(text, text_rect)
        pygame.draw.rect(screen, button_color, button_rect.inflate(20,10))
        screen.blit(button_text, button_rect)
        cursor.draw(screen)
        pygame.display.flip()

