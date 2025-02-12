from models.entities.zombies.zombies import *
from models.entities.plants.plants import *
from models.interface.hud import HUD
from models.interface.map import *
from cursor import Cursor
from models.map.other import *
from methods import load_image

EXIT, MAIN_SCREEN, GAME_OVER, GAME_WIN = 0, 1, 2, 3


def game(screen):
    busy_lawns = []
    suns = []
    plants = []
    zombies = []
    peas = []
    zombie_killed = int(0)
    plants_vs_zombies_map = Map()
    hud = HUD()
    field = Field()
    isShowHitbox = True
    cursor = Cursor()
    pygame.mouse.set_visible(False)
    running = True
    suns_count = 250
    font = pygame.font.SysFont(None, 40)
    font1 = pygame.font.SysFont(None, 30)
    falling_time = time.time()
    zombie_spawn_time = time.time()
    game_start = time.time()
    pygame.mixer.music.load("models/sounds/grasswalk.mp3")
    plant_sound = pygame.mixer.Sound("models/sounds/seed.mp3")
    pygame.mixer.music.play(-1)
    seed = None
    drag_plant_image = None
    dragging = False
    drag_x, drag_y = -100, -100
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
                        seed = "PeaShooter"
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
                            plant = SunFlower(x_plant, y_plant)
                            plant.column, plant.line = lawn_x(drag_x + 40)[1], lawn_y(drag_y + 50)[1]
                            plants.append(plant)
                            plant_sound.play()
                        elif seed == "PeaShooter" and (
                        lawn_x(drag_x + 40)[1], lawn_y(drag_y + 50)[1]) not in busy_lawns and suns_count >= 100:
                            suns_count -= 100
                            busy_lawns.append((lawn_x(drag_x + 40)[1], lawn_y(drag_y + 50)[1]))
                            plant = PeaShooter(x_plant, y_plant)
                            plant.column, plant.line = lawn_x(drag_x + 40)[1], lawn_y(drag_y + 50)[1]
                            plants.append(plant)
                            plant_sound.play()
                        elif seed == "Nut" and (
                        lawn_x(drag_x + 40)[1], lawn_y(drag_y + 50)[1]) not in busy_lawns and suns_count >= 50:
                            suns_count -= 50
                            busy_lawns.append((lawn_x(drag_x + 40)[1], lawn_y(drag_y + 50)[1]))
                            plant = Nut(x_plant, y_plant)
                            plant.column, plant.line = lawn_x(drag_x + 40)[1], lawn_y(drag_y + 50)[1]
                            plants.append(plant)
                            plant_sound.play()
                        elif seed == "TorchWood" and (
                        lawn_x(drag_x + 40)[1], lawn_y(drag_y + 50)[1]) not in busy_lawns and suns_count >= 175:
                            suns_count -= 175
                            busy_lawns.append((lawn_x(drag_x + 40)[1], lawn_y(drag_y + 50)[1]))
                            plant = TorchWood(x_plant, y_plant)
                            plant.column, plant.line = lawn_x(drag_x + 40)[1], lawn_y(drag_y + 50)[1]
                            plants.append(plant)
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
            plant.draw(screen, busy_lawns, is_show_hitbox=isShowHitbox)
            if isinstance(plant, SunFlower):
                new_sun = plant.generate_sun(suns)
                if new_sun:
                    suns.append(new_sun)
            if isinstance(plant, PeaShooter):
                new_pea = plant.shoot(peas, zombies)
                if new_pea:
                    peas.append(new_pea)
        for pea in peas:
            pea.check_shoot(zombies)
            pea.draw(screen, plants, isShowHitbox)
        if dragging and drag_plant_image is not None:
            screen.blit(drag_plant_image, (drag_x, drag_y))
        if time.time() - zombie_spawn_time >= 10:
            chance = random.randint(1, 100)
            y, line = lawn_y(random.randint(76, 574))
            if chance <= 60:
                zombie = BasicZombie(line=line, x=1000, y=y - 30)
            elif 60 < chance < 90:
                zombie = ConeZombie(line=line, x=1000, y=y - 30)
            else:
                zombie = BucketZombie(line=line, x=1000, y=y - 30)
            zombies.append(zombie)
            zombie_spawn_time = time.time()
        for zombie in zombies:
            zombie.draw(screen, plants, is_show_hitbox=isShowHitbox)
            zombie_killed = zombie.zombies_killed(zombie_killed)
            if zombie.game_over():
                return GAME_OVER
        for sun in suns:
            sun.draw(screen, is_show_hitbox=isShowHitbox)
        # zombies[:] = [zombie for zombie in zombies if zombie.health > 0]
        # plants[:] = [plant for plant in plants if plant.health > 0]
        suns_text = font.render(str(suns_count), True, (0, 0, 0))
        screen.blit(suns_text, (45, 82))
        zombies_killed_text1 = font1.render(str(zombie_killed), True, (0, 0, 0))
        screen.blit(zombies_killed_text1, (900, 50))
        zombies_killed_text2 = font1.render("убито зомбе", True, (0, 0, 0))
        screen.blit(zombies_killed_text2, (850, 20))
        if time.time() - game_start >= 20:
            speed_text = font.render("зомби ускорились", True, (220, 20, 60), (0, 0, 0))
            screen.blit(speed_text, (400, 30))
            for zombie in zombies:
                zombie.change_x = 0.075
        cursor.draw(screen)
        pygame.display.flip()
        if zombie_killed >= 15:
            return GAME_WIN

def game_win(screen):
    cursor = Cursor()
    pygame.mouse.set_visible(False)
    font = pygame.font.Font(None, 72)
    text = font.render("You Win!", True, (0, 255, 0))
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
                    return MAIN_SCREEN
            if event.type == pygame.MOUSEMOTION:
                cursor.move(*event.pos)

        screen.fill((0, 0, 0))
        screen.blit(text, text_rect)
        pygame.draw.rect(screen, button_color, button_rect.inflate(20, 10))
        screen.blit(button_text, button_rect)
        cursor.draw(screen)
        pygame.display.flip()

def game_over(screen):
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
                    return MAIN_SCREEN
            if event.type == pygame.MOUSEMOTION:
                cursor.move(*event.pos)
        screen.fill((0, 0, 0))
        screen.blit(text, text_rect)
        pygame.draw.rect(screen, button_color, button_rect.inflate(20, 10))
        screen.blit(button_text, button_rect)
        cursor.draw(screen)
        pygame.display.flip()


def menu(screen):
    cursor = Cursor()
    pygame.mouse.set_visible(False)

    background = load_image("images/background.jpg")
    background = pygame.transform.scale(background, (screen.get_width(), screen.get_height()))

    button_font = pygame.font.Font(None, 48)
    button_text = button_font.render("Start Game", True, (255, 255, 255))
    button_rect = button_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
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

        screen.blit(background, (0, 0))
        pygame.draw.rect(screen, button_color, button_rect.inflate(20, 10))
        screen.blit(button_text, button_rect)
        cursor.draw(screen)
        pygame.display.flip()