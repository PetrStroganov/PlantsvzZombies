from models.entities.plants.plants import *
from models.interface.hud import HUD
from models.interface.map import *
from models.cursor import Cursor
from models.map.other import *

EXIT, MAIN_SCREEN = 0, 1
busy_lawns = []
suns = []
plants = []


def game(screen):
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
        suns_text = font.render(str(suns_count), True, (0, 0, 0))
        screen.blit(suns_text, (45, 82))
        pygame.display.flip()
