import pygame
from player_file import *
from wall_sprites_file import *
from render_file import *
import sys
from gui_file import *
import threading
import json


class Button(pygame.sprite.Sprite):
    def __init__(self, button_image, button_rect, button_type):
        super().__init__()
        self.image = button_image
        self.image.set_colorkey((255, 255, 255))
        self.rect = button_rect
        self.type = button_type

    def is_clicked(self):
        return self.rect.x <= pygame.mouse.get_pos()[0] <= self.rect.x + self.rect.w and \
               (self.rect.y <= pygame.mouse.get_pos()[1] <= self.rect.y + self.rect.h)


def load():
    counter = 0
    while True:
        # Держим цикл на правильной скорости
        clock.tick(FPS // 16)
        # Ввод процесса (события)
        for event in pygame.event.get():
            # проверка для закрытия окна
            if event.type == pygame.QUIT or event.type == 26:
                return None
        screen.blit(background_image, (0, 0))
        screen.blit(text_loading[counter % len(text_loading)], (1650, 1000))
        # переворот изображения, это чтобы не отрисовывались отдльные части
        pygame.display.flip()
        counter += 1


def load_1(*args):
    global map_dict
    with open(args[0], "r") as read_file:
        data = json.load(read_file)
        maps = {}
        for obj_1 in data:
            x_1, y_1 = tuple([int(j) for j in obj_1.split(';')])
            if data[obj_1]['type'] == 'wall':
                obj = Brick([x_1, y_1], (
                    round(SIZE_OF_RECT * data[obj_1]['size'][0]), round(SIZE_OF_RECT * data[obj_1]['size'][1])),
                            'tiles\\grass\\' + data[obj_1]['name'])
            elif data[obj_1]['type'] == 'decor':
                obj = Brick([x_1, y_1], (
                    round(SIZE_OF_RECT * data[obj_1]['size'][0]), round(SIZE_OF_RECT * data[obj_1]['size'][1])),
                            'tiles\\decor\\' + data[obj_1]['name'])
            elif data[obj_1]['type'] == 'bonus':
                obj = Brick([x_1, y_1], (
                    round(SIZE_OF_RECT * data[obj_1]['size'][0]), round(SIZE_OF_RECT * data[obj_1]['size'][1])),
                            'tiles\\bonus\\' + data[obj_1]['name'])
            maps[tuple([int(cord) for cord in obj_1.split(';')])] = (obj, data[obj_1]['type'])
    pygame.event.post(pygame.event.Event(26, {}))
    map_dict = maps


def main():
    while True:
        # Держим цикл на правильной скорости
        clock.tick(FPS)
        # Ввод процесса (события)
        for event in pygame.event.get():
            # проверка для закрытия окна
            if event.type == pygame.QUIT:
                return 'exit'
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return 'esc_menu'

        render.render_funk()

        # переворот изображения, это чтобы не отрисовывались отдльные части
        pygame.display.flip()


def menu():
    while True:
        # Держим цикл на правильной скорости
        clock.tick(FPS)
        # Ввод процесса (события)
        for event in pygame.event.get():
            # проверка для закрытия окна
            if event.type == pygame.QUIT:
                return 'exit'
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for but in menu_buttons_sprites:
                    if but.is_clicked():
                        return but.type

        screen.blit(menu_background_image, (0, 0))
        screen.blit(menu_decoration_image, (SIZE_OF_RECT // 4, SIZE_OF_RECT // 4))

        menu_buttons_sprites.draw(screen)
        # переворот изображения, это чтобы не отрисовывались отдльные части
        pygame.display.flip()


def esc_menu():
    while True:
        # Держим цикл на правильной скорости
        clock.tick(FPS)
        # Ввод процесса (события)
        for event in pygame.event.get():
            # проверка для закрытия окна
            if event.type == pygame.QUIT:
                return 'exit'
            if event.type == pygame.MOUSEBUTTONDOWN:
                for but in esc_menu_buttons_sprites:
                    if but.is_clicked():
                        return but.type
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return 'main'

        screen.blit(settings_background_image, (0, 0))
        screen.blit(settings_decoration_image, (SIZE_OF_RECT * 9, SIZE_OF_RECT * 17 // 15))

        esc_menu_buttons_sprites.draw(screen)
        # переворот изображения, это чтобы не отрисовывались отдльные части
        pygame.display.flip()


def settings():
    global cursor_position
    cursor_position = 0
    cursor.rect.x = settings_buttons_sprites.sprites()[cursor_position].rect.x - settings_buttons_sprites.sprites()[
        0].rect.w // 2 - 5
    cursor.rect.y = settings_buttons_sprites.sprites()[cursor_position].rect.y
    while True:
        # Держим цикл на правильной скорости
        clock.tick(FPS)
        # Ввод процесса (события)
        for event in pygame.event.get():
            # проверка для закрытия окна
            if event.type == pygame.QUIT:
                return 'exit'
            elif event.type == pygame.MOUSEBUTTONDOWN:
                keys = pygame.key.get_pressed()
                for i in settings_buttons_sprites:
                    if i.is_clicked() or keys[pygame.K_RETURN]:
                        if i.type == 'menu':
                            return 'menu'
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    if cursor_position + 1 < len(settings_buttons_sprites.sprites()):
                        cursor_position += 1
                    else:
                        cursor_position = 0
                elif event.key == pygame.K_UP:
                    if cursor_position - 1 >= 0:
                        cursor_position -= 1
                    else:
                        cursor_position = len(settings_buttons_sprites.sprites()) - 1
                cursor.rect.x =\
                    settings_buttons_sprites.sprites()[cursor_position].rect.x - settings_buttons_sprites.sprites()[
                                    0].rect.w // 2 - 5
                cursor.rect.y = settings_buttons_sprites.sprites()[cursor_position].rect.y

        screen.blit(settings_background_image, (0, 0))
        screen.blit(settings_decoration_image, (SIZE_OF_RECT * 9, SIZE_OF_RECT * 17 // 15))

        settings_buttons_sprites.draw(screen)
        cursor_sprites.draw(screen)

        # переворот изображения, это чтобы не отрисовывались отдльные части
        pygame.display.flip()


def load_func():
    # Тимоша, дерзай))
    return 'data_file.json'


pygame.init()
pygame.mixer.init()

inf = pygame.display.Info()
x, y = inf.current_w // 30, inf.current_h // 17
if x > y:
    SIZE_OF_RECT = int(y)
else:
    SIZE_OF_RECT = int(x)
# SIZE_OF_RECT //= 2
WIDTH = SIZE_OF_RECT * 30
HEIGHT = SIZE_OF_RECT * 17
WIDTH_SHIFT = inf.current_w - WIDTH
HEIGHT_SHIFT = inf.current_h - HEIGHT
FPS = 60
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN | pygame.DOUBLEBUF | pygame.HWSURFACE)
# screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.DOUBLEBUF | pygame.HWSURFACE)
clock = pygame.time.Clock()

#  общие константы
font_sh = pygame.font.Font('fonts\\f1.ttf', 36)

#  load func
background_image = transform.scale(image.load('fons\\load_background.png').convert(), (WIDTH, HEIGHT))
text_loading = [font_sh.render("Загрузка...", True, (20, 23, 61)),
                font_sh.render("Загрузка..", True, (20, 23, 61)),
                font_sh.render("Загрузка.", True, (20, 23, 61))]

#  main func
decor_sprites = pygame.sprite.Group()
bonus_sprites = pygame.sprite.Group()
particle_sprites = pygame.sprite.Group()
dust_particle_sprites = pygame.sprite.Group()
wall_sprites = Wal_sprite(SIZE_OF_RECT, decor_sprites, bonus_sprites, particle_sprites, dust_particle_sprites,
                          screen)
player_sprites = pygame.sprite.Group()
gui_sprites = Gui(SIZE_OF_RECT)
gui_sprites.set_hearts(6)
render = Render(screen, player_sprites, wall_sprites, decor_sprites, bonus_sprites, gui_sprites,
                dust_particle_sprites, particle_sprites)

Player((SIZE_OF_RECT * 14, SIZE_OF_RECT * 8), player_sprites, wall_sprites, bonus_sprites, gui_sprites,
       particle_sprites, dust_particle_sprites, SIZE_OF_RECT)
map_dict = []

# menu func
menu_background_image = pygame.transform.scale(pygame.image.load('fons\\menu_background.png').convert(),
                                               (WIDTH, HEIGHT))
menu_decoration_image = pygame.transform.scale(pygame.image.load('fons\\menu_illustration.png').convert(),
                                               (SIZE_OF_RECT * 8, SIZE_OF_RECT * 2))
menu_decoration_image.set_colorkey((0, 0, 0))

menu_buttons_sprites = pygame.sprite.Group()
count = 0
for i, j in [("Новая игра", 'new_game'), ("Загрузить игру", 'load_game'), ("Настройки", 'settings'),
             ("Выход", 'exit')]:
    text = font_sh.render(i, True, (245, 245, 245))
    menu_buttons_sprites.add(Button(text, text.get_rect(x=SIZE_OF_RECT // 4,
                                                        y=SIZE_OF_RECT // 4 + SIZE_OF_RECT * (2 + count)), j))
    count += 1
# esc_menu func
esc_menu_buttons_sprites = pygame.sprite.Group()
count = 1
for i, j in [("Продолжить", 'main'), ("Загрузить игру", 'load_game'), ("Настройки", 'settings'),
             ("Выход в меню", 'menu')]:
    text = font_sh.render(i, True, (245, 245, 245))
    esc_menu_buttons_sprites.add(Button(text, text.get_rect(centerx=SIZE_OF_RECT * 15,
                                                            y=SIZE_OF_RECT * 17 // 15 + SIZE_OF_RECT * (2 + count)), j))
    count += 1

#  settings funk
settings_background_image = pygame.transform.scale(pygame.image.load('fons\\option_background.png').convert(),
                                                   (WIDTH, HEIGHT))
settings_decoration_image = pygame.transform.scale(pygame.image.load('fons\\menu_illustration.png').convert(),
                                                   (SIZE_OF_RECT * 12, SIZE_OF_RECT * 3))
settings_decoration_image.set_colorkey((0, 0, 0))

settings_buttons_sprites = pygame.sprite.Group()
count = 1
for i, j in [("Звук", 'settings'), ("Назад", 'menu'), ("Ещё пункт, длинный пункт", 'exit')]:
    text = font_sh.render(i, True, (245, 245, 245))
    settings_buttons_sprites.add(Button(text, text.get_rect(centerx=SIZE_OF_RECT * 15,
                                                            y=SIZE_OF_RECT * 17 // 15 + SIZE_OF_RECT * (2 + count)), j))
    count += 1

cursor_position = 0
cursor = pygame.sprite.Sprite()
cursor.image = pygame.transform.scale(pygame.image.load('fons\\cursor.png').convert(), (SIZE_OF_RECT, SIZE_OF_RECT))
cursor.image.set_colorkey((255, 255, 255))
cursor.rect = cursor.image.get_rect()
cursor.rect.x = settings_buttons_sprites.sprites()[cursor_position].rect.x - settings_buttons_sprites.sprites()[
    0].rect.w // 2 - 5
cursor.rect.y = settings_buttons_sprites.sprites()[cursor_position].rect.y
cursor_sprites = pygame.sprite.Group(cursor)

result = menu()
while True:
    if result == 'new_game':
        result = 'exit'
    elif result == 'load_game':
        result = load_func()
        if not result == 'menu':
            q = [True]
            t1 = threading.Thread(target=load)
            t2 = threading.Thread(target=load_1, args=(result, q))
            t1.start()
            t2.start()
            t2.join()
            t1.join()
            result = 'main'
            wall_sprites.load(map_dict)
    elif result == 'menu':
        result = menu()
    elif result == 'settings':
        result = settings()
    elif result == 'main':
        result = main()
    elif result == 'esc_menu':
        result = esc_menu()
    elif result == 'exit':
        pygame.quit()
        sys.exit()
