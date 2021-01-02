import pygame
pygame.init()
from player_file import *
from wall_sprites_file import *
from render_file import *
import sys
import os
from gui_file import *
import threading
import json
from save_point_file import SavePoint
from enemy_file import *


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


def screen_saver():
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


# with_player1
def save_1(*name):
    name = ''.join(name)
    global map_dict
    data = {}
    for obj in map_dict:
        obj_1 = ';'.join([str(xy) for xy in obj])
        obj = map_dict[obj]
        data[obj_1] = {}
        data[obj_1]['name'] = obj[0].image_name.split('\\')[-1]
        data[obj_1]['type'] = obj[1]
        data[obj_1]['size'] = [round(xy / SIZE_OF_RECT, 3) for xy in obj[0].rect_size]
        if obj[0].shift != (0, 0):
            data[obj_1]['shift'] = [round(sh, 3) for sh in obj[0].shift]
    data['cords'] = wall_sprites.cords
    data['hp'] = gui_sprites.hp
    data['bombs'] = gui_sprites.bomb
    with open(name, "w") as write_file:
        json.dump(data, write_file)
    pygame.event.post(pygame.event.Event(26, {}))


def load_1(*name):
    name = ''.join(name)
    global map_dict
    particle_sprites.empty()
    dust_particle_sprites.empty()
    with open(name, "r") as read_file:
        data = json.load(read_file)
        maps = {}
        for obj_1 in data:
            if obj_1 not in ['cords', 'hp', 'bombs']:
                x_1, y_1 = tuple([int(xy) for xy in obj_1.split(';')])
                if data[obj_1]['type'] == 'wall':
                    obj = Brick([x_1, y_1], (
                        round(SIZE_OF_RECT * data[obj_1]['size'][0]), round(SIZE_OF_RECT * data[obj_1]['size'][1])),
                                'tiles\\grass\\' + data[obj_1]['name'])
                elif data[obj_1]['type'] == 'decor':
                    obj = Brick([x_1, y_1], (
                        round(SIZE_OF_RECT * data[obj_1]['size'][0]), round(SIZE_OF_RECT * data[obj_1]['size'][1])),
                                'tiles\\decaor\\' + data[obj_1]['name'])
                elif data[obj_1]['type'] == 'bonus':
                    obj = Brick([x_1, y_1], (
                        round(SIZE_OF_RECT * data[obj_1]['size'][0]), round(SIZE_OF_RECT * data[obj_1]['size'][1])),
                                'tiles\\bonus\\' + data[obj_1]['name'])
                elif data[obj_1]['type'] == 'save':
                    obj = SavePoint([x_1, y_1], (
                        round(SIZE_OF_RECT * data[obj_1]['size'][0]), round(SIZE_OF_RECT * data[obj_1]['size'][1])))
                elif data[obj_1]['type'] == 'damage':
                    obj = Brick([x_1, y_1], (
                        round(SIZE_OF_RECT * data[obj_1]['size'][0]), round(SIZE_OF_RECT * data[obj_1]['size'][1])),
                                'tiles\\damage\\' + data[obj_1]['name'], shift=data[obj_1]['shift'])
                elif data[obj_1]['type'] == 'enemy':
                    if data[obj_1]['name'] == 'crash.png':
                        obj = Crash([x_1, y_1], (round(SIZE_OF_RECT * data[obj_1]['size'][0]),
                                                 round(SIZE_OF_RECT * data[obj_1]['size'][1])),
                                    'tiles\\enemy\\' + data[obj_1]['name'], wall_sprites, damage_sprites,
                                    shift=data[obj_1]['shift'])
                obj.delay = [x_1 + data[obj_1]['size'][0] + obj.shift[0] - 15,
                             y_1 + data[obj_1]['size'][1] + obj.shift[0] - 15]
                maps[tuple([int(cord) for cord in obj_1.split(';')])] = (obj, data[obj_1]['type'])
            elif obj_1 == 'cords':
                cords = data[obj_1]
            elif obj_1 == 'hp':
                hp = data[obj_1]
            elif obj_1 == 'bombs':
                bombs = data[obj_1]
    map_dict = maps
    player.rect.x, player.rect.y = (SIZE_OF_RECT * 14, SIZE_OF_RECT * 8)
    wall_sprites.load(map_dict, cords)
    gui_sprites.set_hearts(hp)
    gui_sprites.set_bombs(bombs)
    pygame.event.post(pygame.event.Event(26, {}))


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
            if event.type == 30:
                return 'main_1'
            if event.type == 31:
                return 'main_2'

        render.render_funk()

        # переворот изображения, это чтобы не отрисовывались отдльные части
        pygame.display.flip()


def main_1():
    timer = 0
    while True:
        # Держим цикл на правильной скорости
        clock.tick(FPS)
        # Ввод процесса (события)
        for event in pygame.event.get():
            # проверка для закрытия окна
            if event.type == pygame.QUIT:
                return 'exit'

        render.render_funk_1()
        # переворот изображения, это чтобы не отрисовывались отдльные части
        pygame.display.flip()
        timer += 1
        if timer >= 240:
            return 'save'


def main_2():
    timer = 0
    can_exit = False
    print('ok')
    while True:
        # Держим цикл на правильной скорости
        clock.tick(FPS)
        # Ввод процесса (события)
        for event in pygame.event.get():
            # проверка для закрытия окна
            if event.type == pygame.QUIT:
                return 'exit'
            elif event.type == pygame.KEYDOWN and can_exit:
                return 'menu'

        render.render_funk_2()
        # переворот изображения, это чтобы не отрисовывались отдльные части
        pygame.display.flip()
        timer += 1
        if timer >= 50:
            can_exit = True


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
                        if but.type == 'settings':
                            for ob in settings_buttons_sprites:
                                if ob.type == 'menu':
                                    ob.type = 'esc_menu'
                        return but.type
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return 'main'

        screen.blit(settings_background_image, (0, 0))
        screen.blit(settings_decoration_image, (SIZE_OF_RECT * 9, SIZE_OF_RECT * 17 // 15))

        esc_menu_buttons_sprites.draw(screen)
        # переворот изображения, это чтобы не отрисовывались отдльные части
        pygame.display.flip()


def settings_processor(obj):
    global type_of_btn, sound_open, cursor_position
    if obj.type == 'sound':
        sound_open = True
        for obj_1 in settings_buttons_sprites:
            if obj_1.type == 'menu' or obj_1.type == 'esc_menu':
                obj_1.kill()
                type_of_btn = obj_1.type
                text_but = font_sh.render('Готово', True, (245, 245, 245))
                settings_buttons_sprites.add(
                    Button(text_but, text_but.get_rect(centerx=SIZE_OF_RECT * 15,
                                                       y=SIZE_OF_RECT * 17 // 15 + SIZE_OF_RECT * 5), 'close'))
                break
        cursor_position = 0
        cursor.rect.right = \
            settings_buttons_sprites.sprites()[cursor_position].rect.x - 5
        cursor.rect.centery = settings_buttons_sprites.sprites()[cursor_position].rect.centery
    elif obj.type == 'close':
        for obj_1 in settings_buttons_sprites:
            if obj_1.type == 'close':
                obj_1.kill()
                text_but = font_sh.render('Назад', True, (245, 245, 245))
                settings_buttons_sprites.add(
                    Button(text_but,
                           text_but.get_rect(centerx=SIZE_OF_RECT * 15,
                                             y=SIZE_OF_RECT * 17 // 15 + SIZE_OF_RECT * 4),
                           type_of_btn))
                break
        sound_open = False
        cursor_position = 0
        cursor.rect.right = \
            settings_buttons_sprites.sprites()[cursor_position].rect.x - 5
        cursor.rect.centery = settings_buttons_sprites.sprites()[cursor_position].rect.centery


def settings():
    global cursor_position, sound_count, type_of_btn, sound_open
    cursor_position = 0
    cursor.rect.right = settings_buttons_sprites.sprites()[cursor_position].rect.x - 5
    cursor.rect.centery = settings_buttons_sprites.sprites()[cursor_position].rect.centery
    type_of_btn = ''
    sound_open = False
    while True:
        # Держим цикл на правильной скорости
        clock.tick(FPS)
        # Ввод процесса (события)
        for event in pygame.event.get():
            # проверка для закрытия окна
            if event.type == pygame.QUIT:
                return 'exit'
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for obj in settings_buttons_sprites:
                    if obj.is_clicked():
                        if obj.type == 'menu' or obj.type == 'esc_menu':
                            return obj.type
                        settings_processor(obj)
                if sound_open:
                    for obj_1 in settings_buttons_sprites_sound:
                        if obj_1.rect.x <= pygame.mouse.get_pos()[0] <= obj_1.rect.x + obj_1.rect.w and (
                                obj_1.rect.y <= pygame.mouse.get_pos()[1] <= obj_1.rect.y + obj_1.rect.h):
                            if obj_1.type == '+':
                                if sound_count != 10:
                                    sound_count += 1
                            elif obj_1.type == '-':
                                if sound_count != 0:
                                    sound_count -= 1
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
                elif event.key == pygame.K_RETURN:
                    obj = settings_buttons_sprites.sprites()[cursor_position]
                    if obj.type == 'menu' or obj.type == 'esc_menu':
                        return obj.type
                    settings_processor(obj)

                cursor.rect.right = \
                    settings_buttons_sprites.sprites()[cursor_position].rect.x - 5
                cursor.rect.centery = settings_buttons_sprites.sprites()[cursor_position].rect.centery

        screen.blit(settings_background_image, (0, 0))
        screen.blit(settings_decoration_image, (SIZE_OF_RECT * 9, SIZE_OF_RECT * 17 // 15))

        settings_buttons_sprites.draw(screen)
        cursor_sprites.draw(screen)
        if sound_open:
            for obj_1 in range(sound_count):
                pygame.draw.rect(screen, (255, 255, 255), (int(SIZE_OF_RECT * 13.3) + obj_1 * small_size_1 * 2,
                                                           SIZE_OF_RECT * 17 // 13 + SIZE_OF_RECT * 4,
                                                           small_size_2, small_size_1))
            for obj_1 in range(sound_count, 10):
                pygame.draw.rect(screen, (120, 120, 120), (int(SIZE_OF_RECT * 13.3) + obj_1 * small_size_1 * 2,
                                                           SIZE_OF_RECT * 17 // 13 + SIZE_OF_RECT * 4,
                                                           small_size_2, small_size_1))
            settings_buttons_sprites_sound.draw(screen)
        # переворот изображения, это чтобы не отрисовывались отдльные части
        pygame.display.flip()


def new_game():
    while True:
        # Держим цикл на правильной скорости
        clock.tick(FPS)
        # Ввод процесса (события)
        for event in pygame.event.get():
            # проверка для закрытия окна
            if event.type == pygame.QUIT:
                return 'exit'
            if event.type == pygame.MOUSEBUTTONDOWN:
                for but in diff_btns:
                    if but.is_clicked():
                        if but.type == 'settings':
                            for ob in diff_btns:
                                if ob.type == 'menu':
                                    ob.type = 'esc_menu'
                        return but.type
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return 'main'

        screen.blit(dif_set_image, (0, 0))
        diff_btns.draw(screen)
        pygame.display.flip()


def load_func():
    closed_mass = [f"saves\\{fname}" for fname in os.listdir(path=f"{os.getcwd()}\\saves")]
    saves_names = []
    for elem in closed_mass:
        saves_names.append(f"Точка сохранения №{closed_mass.index(elem) + 1}")
    load_btn_sprites = pygame.sprite.Group()
    load_count = 0
    for load_i, load_j in [*[(saves_names[closed_mass.index(el)], el) for el in closed_mass], ("Выход", 'menu')]:
        saves_text = font_sh.render(load_i, True, (245, 245, 245))
        load_btn_sprites.add(Button(saves_text, saves_text.get_rect(x=SIZE_OF_RECT // 4,
                                                                    y=SIZE_OF_RECT // 4 + SIZE_OF_RECT * (
                                                                            2 + load_count)), load_j))
        load_count += 1
    while True:
        # Держим цикл на правильной скорости
        clock.tick(FPS)
        # Ввод процесса (события)
        for event in pygame.event.get():
            # проверка для закрытия окна
            if event.type == pygame.QUIT:
                return 'exit'
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for but in load_btn_sprites:
                    if but.is_clicked():
                        return but.type

        screen.blit(menu_background_image, (0, 0))
        screen.blit(menu_decoration_image, (SIZE_OF_RECT // 4, SIZE_OF_RECT // 4))
        load_btn_sprites.draw(screen)
        # переворот изображения, это чтобы не отрисовывались отдльные части
        pygame.display.flip()


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

#  screen_saver func
background_image = transform.scale(image.load('fons\\load_background.png').convert(), (WIDTH, HEIGHT))
text_loading = [font_sh.render("Загрузка...", True, (20, 23, 61)),
                font_sh.render("Загрузка..", True, (20, 23, 61)),
                font_sh.render("Загрузка.", True, (20, 23, 61))]

#  main func
decor_sprites = pygame.sprite.Group()
bonus_sprites = pygame.sprite.Group()
saves_sprites = pygame.sprite.Group()
particle_sprites = pygame.sprite.Group()
dust_particle_sprites = pygame.sprite.Group()
damage_sprites = pygame.sprite.Group()
enemies_sprites = pygame.sprite.Group()
wall_sprites = Wal_sprite(SIZE_OF_RECT, decor_sprites, bonus_sprites, particle_sprites, dust_particle_sprites,
                          saves_sprites, damage_sprites, enemies_sprites, screen)
player_sprites = pygame.sprite.Group()
gui_sprites = Gui(SIZE_OF_RECT)
gui_sprites.set_hearts(6)
render = Render(screen, player_sprites, wall_sprites, decor_sprites, bonus_sprites, gui_sprites,
                dust_particle_sprites, particle_sprites, saves_sprites, damage_sprites, enemies_sprites)

player = Player((SIZE_OF_RECT * 14, SIZE_OF_RECT * 8), player_sprites, wall_sprites, bonus_sprites, gui_sprites,
                particle_sprites, dust_particle_sprites, saves_sprites, damage_sprites, enemies_sprites, SIZE_OF_RECT)
map_dict = []

# menu func
menu_background_image = pygame.transform.scale(pygame.image.load('fons\\menu_background.png').convert(),
                                               (WIDTH, HEIGHT))
menu_decoration_image = pygame.transform.scale(pygame.image.load('fons\\menu_illustration.png').convert(),
                                               (SIZE_OF_RECT * 8, SIZE_OF_RECT * 2))
dif_set_image = pygame.transform.scale(pygame.image.load('fons\\bg_diff_selector.png').convert(),
                                       (WIDTH, HEIGHT))
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
# new_game func
diff_btns = pygame.sprite.Group()
count = 1
for i, j in [("Начать", 'main'), ("Сложность", 'load_game'), ("Доп", 'settings'),
             ("Выход в меню", 'menu')]:
    text = font_sh.render(i, True, (245, 245, 245))
    diff_btns.add(Button(text, text.get_rect(centerx=SIZE_OF_RECT * 15,
                                             y=SIZE_OF_RECT * 17 // 15 + SIZE_OF_RECT * (2 + count)), j))
    count += 1

#  settings funk
settings_background_image = pygame.transform.scale(pygame.image.load('fons\\option_background.png').convert(),
                                                   (WIDTH, HEIGHT))
settings_decoration_image = pygame.transform.scale(pygame.image.load('fons\\menu_illustration.png').convert(),
                                                   (SIZE_OF_RECT * 12, SIZE_OF_RECT * 3))
settings_decoration_image.set_colorkey((0, 0, 0))
sound_count = 5
type_of_btn = ''
sound_open = False
small_size_2 = SIZE_OF_RECT // 8
small_size_1 = SIZE_OF_RECT // 5
settings_buttons_sprites = pygame.sprite.Group()
settings_buttons_sprites_sound = pygame.sprite.Group()

spr = sprite.Sprite()
spr.image = pygame.Surface((SIZE_OF_RECT // 2, SIZE_OF_RECT // 2))
spr.rect = spr.image.get_rect()
spr.rect.x = int(SIZE_OF_RECT * 13.3) + 10 * small_size_1 * 2 - small_size_1 // 2
spr.rect.centery = SIZE_OF_RECT * 17 // 13 + SIZE_OF_RECT * 4 + small_size_1 // 2
pygame.draw.rect(spr.image, (255, 255, 255), (0, SIZE_OF_RECT // 6, SIZE_OF_RECT, SIZE_OF_RECT // 6))
pygame.draw.rect(spr.image, (255, 255, 255), (SIZE_OF_RECT // 6, 0, SIZE_OF_RECT // 6, SIZE_OF_RECT))
spr.type = '+'
settings_buttons_sprites_sound.add(spr)

spr = sprite.Sprite()
spr.image = pygame.Surface((SIZE_OF_RECT // 2, SIZE_OF_RECT // 2))
spr.rect = spr.image.get_rect()
spr.rect.x = int(SIZE_OF_RECT * 13.3) - SIZE_OF_RECT // 3 * 2
spr.rect.centery = SIZE_OF_RECT * 17 // 13 + SIZE_OF_RECT * 4 + small_size_1 // 2
pygame.draw.rect(spr.image, (255, 255, 255), (0, SIZE_OF_RECT // 6, SIZE_OF_RECT, SIZE_OF_RECT // 6))
spr.type = '-'
settings_buttons_sprites_sound.add(spr)

count = 1
for i, j in [("Звук", 'sound'), ("Назад", 'menu')]:
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
name_of_save = ''
while True:
    if result == 'new_game':
        result = new_game()
    elif result == 'load_game':
        name_of_save = load_func()
        if not name_of_save == 'menu':
            t1 = threading.Thread(target=screen_saver)
            t2 = threading.Thread(target=load_1, args=name_of_save)
            t1.start()
            t2.start()
            t2.join()
            t1.join()
            result = 'main'
        else:
            result = name_of_save
    elif result == 'menu':
        result = menu()
    elif result == 'settings':
        result = settings()
        for i in settings_buttons_sprites:
            if i.type == 'esc_menu':
                i.type = 'menu'
    elif result == 'main':
        result = main()
    elif result == 'esc_menu':
        result = esc_menu()
    elif result == 'exit':
        pygame.quit()
        sys.exit()
    elif result == 'save':
        t1 = threading.Thread(target=screen_saver)
        t2 = threading.Thread(target=save_1, args=name_of_save)
        t1.start()
        t2.start()
        t2.join()
        t1.join()
        result = 'menu'
    elif result == 'main_1':
        result = main_1()
    elif result == 'main_2':
        result = main_2()
