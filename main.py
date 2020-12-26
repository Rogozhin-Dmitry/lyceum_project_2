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
    count = 0
    while q[0]:
        # Держим цикл на правильной скорости
        clock.tick(FPS // 16)
        # Ввод процесса (события)
        for event in pygame.event.get():
            # проверка для закрытия окна
            if event.type == pygame.QUIT:
                return None
        screen.blit(background_image, (0, 0))
        screen.blit(text_loading[count % len(text_loading)], (1650, 1000))
        # переворот изображения, это чтобы не отрисовывались отдльные части
        pygame.display.flip()
        count += 1


def load_1(*args):
    global q, map_dict
    with open(args[0], "r") as read_file:
        data = json.load(read_file)
        maps = {}
        for i in data:
            x_1, y_1 = tuple([int(j) for j in i.split(';')])
            if data[i]['type'] == 'wall':
                obj = Brick([x_1, y_1], (
                    round(SIZE_OF_RECT * data[i]['size'][0]), round(SIZE_OF_RECT * data[i]['size'][1])),
                            'tiles\\grass\\' + data[i]['name'])
            elif data[i]['type'] == 'decor':
                obj = Brick([x_1, y_1], (
                    round(SIZE_OF_RECT * data[i]['size'][0]), round(SIZE_OF_RECT * data[i]['size'][1])),
                            'tiles\\decor\\' + data[i]['name'])
            elif data[i]['type'] == 'bonus':
                obj = Brick([x_1, y_1], (
                    round(SIZE_OF_RECT * data[i]['size'][0]), round(SIZE_OF_RECT * data[i]['size'][1])),
                            'tiles\\bonus\\' + data[i]['name'])
            maps[tuple([int(j) for j in i.split(';')])] = (obj, data[i]['type'])
    q[0] = False
    map_dict = maps
    return 'main'


def main(map_dict_1):
    wall_sprites.load(map_dict_1)
    while True:
        # Держим цикл на правильной скорости
        clock.tick(FPS)
        # Ввод процесса (события)
        for event in pygame.event.get():
            # проверка для закрытия окна
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return None

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
                for i in menu_buttons_sprites:
                    if i.is_clicked():
                        return i.type

        screen.blit(menu_background_image, (0, 0))
        screen.blit(menu_decoration_image, (SIZE_OF_RECT // 4, SIZE_OF_RECT // 4))

        menu_buttons_sprites.draw(screen)
        # переворот изображения, это чтобы не отрисовывались отдльные части
        pygame.display.flip()


def settings():
    background_image = pygame.transform.scale(pygame.image.load('fons\\option_background.png').convert(),
                                              (WIDTH, HEIGHT))
    decoration_image = pygame.transform.scale(pygame.image.load('fons\\menu_illustration.png').convert(),
                                              (SIZE_OF_RECT * 12, SIZE_OF_RECT * 3))
    decoration_image.set_colorkey((0, 0, 0))

    buttons_sprites = pygame.sprite.Group()
    font = pygame.font.Font('fonts\\f1.ttf', SIZE_OF_RECT)
    count = 1
    for i, j in [("Звук", 'settings'), ("Назад", 'exit'), ("Ещё пункт, длинный пункт", 'exit')]:
        text = font.render(i, True, (245, 245, 245))
        buttons_sprites.add(Button(text, text.get_rect(centerx=SIZE_OF_RECT * 15,
                                                       y=SIZE_OF_RECT * 17 // 15 + SIZE_OF_RECT * (2 + count)), j))
        count += 1

    cursor_position = 0
    cursor = pygame.sprite.Sprite()
    cursor.image = pygame.transform.scale(pygame.image.load('fons\\cursor.png').convert(), (SIZE_OF_RECT, SIZE_OF_RECT))
    cursor.image.set_colorkey((255, 255, 255))
    cursor.rect = cursor.image.get_rect()
    cursor.rect.x = buttons_sprites.sprites()[cursor_position].rect.x - buttons_sprites.sprites()[0].rect.w // 2 - 5
    cursor.rect.y = buttons_sprites.sprites()[cursor_position].rect.y
    cursor_sprites = pygame.sprite.Group(cursor)

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
                for i in buttons_sprites:
                    if i.is_clicked() or keys[pygame.K_RETURN]:
                        if i.type == 'exit':
                            return None
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    if cursor_position + 1 < len(buttons_sprites.sprites()):
                        cursor_position += 1
                    else:
                        cursor_position = 0
                elif event.key == pygame.K_UP:
                    if cursor_position - 1 >= 0:
                        cursor_position -= 1
                    else:
                        cursor_position = len(buttons_sprites.sprites()) - 1
                cursor.rect.x = buttons_sprites.sprites()[cursor_position].rect.x - buttons_sprites.sprites()[
                    0].rect.w // 2 - 5
                cursor.rect.y = buttons_sprites.sprites()[cursor_position].rect.y

        screen.blit(background_image, (0, 0))
        screen.blit(decoration_image, (SIZE_OF_RECT * 9, SIZE_OF_RECT * 17 // 15))

        buttons_sprites.draw(screen)
        cursor_sprites.draw(screen)

        # переворот изображения, это чтобы не отрисовывались отдльные части
        pygame.display.flip()


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

# func
menu_background_image = pygame.transform.scale(pygame.image.load('fons\\menu_background.png').convert(), (WIDTH, HEIGHT))
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

result = menu()
while True:
    if result == 'new_game':
        q = [True]
        t1 = threading.Thread(target=load)
        t2 = threading.Thread(target=load_1, args=('data_file_3.json', q))
        t1.start()
        t2.start()
        t1.join()
        t2.join()
        main(map_dict)
        pygame.quit()
        sys.exit()
    elif result.startswith('load_game'):
        name = 'data_file_3.json'
        q = [True]
        t1 = threading.Thread(target=load)
        t2 = threading.Thread(target=load_1, args=(name, q))
        t1.start()
        t2.start()
        t1.join()
        t2.join()
        result = 'main'
    elif result == 'settings':
        settings()
    elif result == 'main':
        main(map_dict)
    elif result == 'exit':
        pygame.quit()
        sys.exit()
