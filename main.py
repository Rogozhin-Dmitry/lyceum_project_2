import pygame
from pygame import mixer
from shutil import copy
import sys
import os
import json
import threading

pygame.init()
pygame.mixer.init()
from player_file import *
from wall_sprites_file import *
from render_file import *
from gui_file import *
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
        for ss_ev_activity in pygame.event.get():
            # проверка для закрытия окна
            if ss_ev_activity.type == pygame.QUIT or ss_ev_activity.type == 26:
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
        data[obj_1]['can_be_broken'] = obj[0].can_be_broken
        if obj[0].shift != (0, 0):
            data[obj_1]['shift'] = [round(sh, 3) for sh in obj[0].shift]
    for each_sprite in saves_sprites:
        data['cords'] = [each_sprite.cords[0] + 1, each_sprite.cords[1] - 2]
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
    bomb_sprites.empty()
    hp = 10
    bombs = 10
    with open(name, "r") as read_file:
        data = json.load(read_file)
        maps = {}
        for obj_1 in data:
            if obj_1 not in ['cords', 'hp', 'bombs']:
                x_1, y_1 = tuple([int(xy) for xy in obj_1.split(';')])
                if data[obj_1]['type'] == 'wall':
                    obj = Brick([x_1, y_1], (
                        round(SIZE_OF_RECT * data[obj_1]['size'][0]), round(SIZE_OF_RECT * data[obj_1]['size'][1])),
                                'tiles\\grass\\' + data[obj_1]['name'], data[obj_1]['can_be_broken'])
                elif data[obj_1]['type'] == 'decor':
                    obj = Brick([x_1, y_1], (
                        round(SIZE_OF_RECT * data[obj_1]['size'][0]), round(SIZE_OF_RECT * data[obj_1]['size'][1])),
                                'tiles\\decor\\' + data[obj_1]['name'], data[obj_1]['can_be_broken'])
                elif data[obj_1]['type'] == 'bonus':
                    obj = Brick([x_1, y_1], (
                        round(SIZE_OF_RECT * data[obj_1]['size'][0]), round(SIZE_OF_RECT * data[obj_1]['size'][1])),
                                'tiles\\bonus\\' + data[obj_1]['name'], data[obj_1]['can_be_broken'])
                elif data[obj_1]['type'] == 'save':
                    obj = SavePoint([x_1, y_1], (
                        round(SIZE_OF_RECT * data[obj_1]['size'][0]), round(SIZE_OF_RECT * data[obj_1]['size'][1])))
                elif data[obj_1]['type'] == 'damage':
                    obj = Brick([x_1, y_1], (
                        round(SIZE_OF_RECT * data[obj_1]['size'][0]), round(SIZE_OF_RECT * data[obj_1]['size'][1])),
                                'tiles\\damage\\' + data[obj_1]['name'], data[obj_1]['can_be_broken'],
                                shift=data[obj_1]['shift'])
                elif data[obj_1]['type'] == 'enemy':
                    if data[obj_1]['name'] == 'crash.png':
                        obj = Crash([x_1, y_1], (round(SIZE_OF_RECT * data[obj_1]['size'][0]),
                                                 round(SIZE_OF_RECT * data[obj_1]['size'][1])),
                                    'tiles\\enemy\\' + data[obj_1]['name'], wall_sprites, damage_sprites,
                                    data[obj_1]['can_be_broken'], shift=data[obj_1]['shift'])
                    elif data[obj_1]['name'] == 'fly.png':
                        obj = Fly([x_1, y_1], (round(SIZE_OF_RECT * data[obj_1]['size'][0]),
                                               round(SIZE_OF_RECT * data[obj_1]['size'][1])),
                                  'tiles\\enemy\\' + data[obj_1]['name'], wall_sprites, damage_sprites,
                                  data[obj_1]['can_be_broken'], shift=data[obj_1]['shift'])
                    elif data[obj_1]['name'] == 'boss.png':
                        obj = Boss([x_1, y_1], (round(SIZE_OF_RECT * data[obj_1]['size'][0]),
                                                round(SIZE_OF_RECT * data[obj_1]['size'][1])),
                                   'tiles\\enemy\\' + data[obj_1]['name'], wall_sprites, damage_sprites,
                                   data[obj_1]['can_be_broken'], player, bomb_sprites, shift=data[obj_1]['shift'])
                obj.delay = [x_1 + data[obj_1]['size'][0] + obj.shift[0] - 15,
                             y_1 + data[obj_1]['size'][1] + obj.shift[1] - 15]
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


def name_tag():
    if not pygame.mixer.get_busy() or pygame.mixer.music.get_volume() != Music_Volume * 10 / 100:
        pygame.mixer.music.set_volume(Music_Volume * 10 / 100)
    font_n = pygame.font.Font('fonts\\f1.ttf', 150)
    txt_surf = font_n.render('Adventure of Kyo', True, (25, 25, 25))
    txt_surf_rect = txt_surf.get_rect(centerx=SIZE_OF_RECT * 15, centery=SIZE_OF_RECT * 9)
    alpha_surf = Surface(txt_surf.get_size(), pygame.SRCALPHA)
    timer = 0
    last_timer = 0
    while True:
        # Держим цикл на правильной скорости
        clock.tick(255)
        # Ввод процесса (события)
        for ev_activity in pygame.event.get():
            # проверка для закрытия окна
            if ev_activity.type == pygame.QUIT:
                return 'exit'
            elif ev_activity.type == pygame.KEYDOWN:
                return 'menu'

        if timer - last_timer >= 2:
            alpha_surf.fill((255, 255, 255, max(255 - 2, 0)))
            txt_surf.blit(alpha_surf, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
            last_timer = timer

        screen.fill((30, 30, 30))
        screen.blit(txt_surf, txt_surf_rect)
        # переворот изображения, это чтобы не отрисовывались отдльные части
        pygame.display.flip()
        timer += 1
        if timer >= 275:
            return 'menu'


def main():
    while True:
        # Держим цикл на правильной скорости
        clock.tick(FPS)
        # Ввод процесса (события)
        for ev_activity in pygame.event.get():
            # проверка для закрытия окна
            if ev_activity.type == pygame.QUIT:
                return 'exit'
            if ev_activity.type == pygame.KEYDOWN and ev_activity.key == pygame.K_ESCAPE:
                return 'esc_menu'
            if ev_activity.type == 30:
                return 'freeze'
            if ev_activity.type == 31:
                return 'game_over'
            if ev_activity.type == 50:
                klonk_sound.play()
            if ev_activity.type == 51:
                anti_klonk.play()
            if ev_activity.type == 52:
                hopp.play()
            if ev_activity.type == 53:
                incoming_damage_sound.play()
        render.render_funk()
        # переворот изображения, это чтобы не отрисовывались отдльные части
        pygame.display.flip()


def freeze():
    timer = 0
    while True:
        # Держим цикл на правильной скорости
        clock.tick(FPS)
        # Ввод процесса (события)
        for fr_ev_activity in pygame.event.get():
            # проверка для закрытия окна
            if fr_ev_activity.type == pygame.QUIT:
                return 'exit'

        render.freeze_render_funk()
        # переворот изображения, это чтобы не отрисовывались отдльные части
        pygame.display.flip()
        timer += 1
        if timer >= 240:
            return 'save'


def game_over():
    timer = 0
    can_exit = False
    while True:
        # Держим цикл на правильной скорости
        clock.tick(FPS)
        # Ввод процесса (события)
        for go_ev_activity in pygame.event.get():
            # проверка для закрытия окна
            if go_ev_activity.type == pygame.QUIT:
                return 'exit'
            elif go_ev_activity.type == pygame.KEYDOWN and can_exit:
                return 'menu'

        render.game_over_render_funk()
        # переворот изображения, это чтобы не отрисовывались отдльные части
        pygame.display.flip()
        timer += 1
        if timer >= 50:
            can_exit = True


def menu():
    if not pygame.mixer.get_busy() or pygame.mixer.music.get_volume() != Music_Volume * 10 / 100:
        pygame.mixer.music.set_volume(Music_Volume * 10 / 100)
    while True:
        # Держим цикл на правильной скорости
        clock.tick(FPS)
        # Ввод процесса (события)
        for menu_ev_activity in pygame.event.get():
            # проверка для закрытия окна
            if menu_ev_activity.type == pygame.QUIT:
                return 'exit'
            elif menu_ev_activity.type == pygame.MOUSEBUTTONDOWN:
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
        for esc_ev_activity in pygame.event.get():
            # проверка для закрытия окна
            if esc_ev_activity.type == pygame.QUIT:
                return 'exit'
            if esc_ev_activity.type == pygame.MOUSEBUTTONDOWN:
                for but in esc_menu_buttons_sprites:
                    if but.is_clicked():
                        if but.type == 'settings':
                            for ob in settings_buttons_sprites:
                                if ob.type == 'menu':
                                    ob.type = 'esc_menu'
                        return but.type
            if esc_ev_activity.type == pygame.KEYDOWN and esc_ev_activity.key == pygame.K_ESCAPE:
                return 'main'

        screen.blit(settings_background_image, (0, 0))
        screen.blit(settings_decoration_image, (SIZE_OF_RECT * 9, SIZE_OF_RECT * 17 // 15))

        esc_menu_buttons_sprites.draw(screen)
        # переворот изображения, это чтобы не отрисовывались отдльные части
        pygame.display.flip()


def settings_processor(obj):
    global type_of_btn, sound_open, cursor_position, music_vloume_en_edit, effects_volume_en_edit
    if obj.type == 'music_volume':
        music_vloume_en_edit = True
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
            if obj_1.type == 'effects_volume':
                obj_1.kill()
        cursor_position = 0
        cursor.rect.right = settings_buttons_sprites.sprites()[cursor_position].rect.x - 5
        cursor.rect.centery = settings_buttons_sprites.sprites()[cursor_position].rect.centery

    elif obj.type == 'effects_volume':
        effects_volume_en_edit = True
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
            if obj_1.type == 'music_volume':
                obj_1.kill()
            if obj_1.type == 'effects_volume':
                obj_1.kill()
                text_but = font_sh.render('Громкость эффектов', True, (245, 245, 245))
                settings_buttons_sprites.add(
                    Button(text_but,
                           text_but.get_rect(centerx=SIZE_OF_RECT * 15,
                                             y=SIZE_OF_RECT * 17 // 15 + SIZE_OF_RECT * 3),
                           'effects_volume'))
        cursor_position = 0
        cursor.rect.right = \
            settings_buttons_sprites.sprites()[cursor_position].rect.x - 5
        cursor.rect.centery = settings_buttons_sprites.sprites()[cursor_position].rect.centery
    elif obj.type == 'close':
        for obj_1 in settings_buttons_sprites:
            if obj_1.type == 'close':
                settings_buttons_sprites.empty()
                count_2 = 1
                for name, returner in [("Громкость музыки", 'music_volume'),
                                       ("Громкость эффектов", 'effects_volume'),
                                       ("Назад", 'esc_menu')]:
                    btn_text = font_sh.render(name, True, (245, 245, 245))
                    settings_buttons_sprites.add(
                        Button(btn_text,
                               btn_text.get_rect(centerx=SIZE_OF_RECT * 15,
                                                 y=SIZE_OF_RECT * 17 // 15 + SIZE_OF_RECT * (2 + count_2)), returner))
                    effects_volume_en_edit, music_vloume_en_edit = False, False
                    count_2 += 1
                break
        sound_open = False
        cursor_position = 0
        cursor.rect.right = \
            settings_buttons_sprites.sprites()[cursor_position].rect.x - 5
        cursor.rect.centery = settings_buttons_sprites.sprites()[cursor_position].rect.centery


def settings():
    global cursor_position, Music_Volume, type_of_btn, sound_open, Effects_Volume, music_vloume_en_edit, \
        effects_volume_en_edit, mixer_sounds
    cursor_position = 0
    cursor.rect.right = settings_buttons_sprites.sprites()[cursor_position].rect.x - 5
    cursor.rect.centery = settings_buttons_sprites.sprites()[cursor_position].rect.centery
    type_of_btn = ''
    sound_open = False
    while True:
        # Держим цикл на правильной скорости
        clock.tick(FPS)
        # Ввод процесса (события)
        for settings_ev_activity in pygame.event.get():
            # проверка для закрытия окна
            if settings_ev_activity.type == pygame.QUIT:
                return 'exit'
            elif settings_ev_activity.type == pygame.MOUSEBUTTONDOWN:
                for obj in settings_buttons_sprites:
                    if obj.is_clicked():
                        if obj.type == 'menu' or obj.type == 'esc_menu':
                            if curr_song == "menu_song":
                                return 'menu'
                            else:
                                return obj.type
                        settings_processor(obj)
                if sound_open:
                    for obj_1 in settings_buttons_sprites_sound:
                        if obj_1.rect.x <= pygame.mouse.get_pos()[0] <= obj_1.rect.x + obj_1.rect.w and (
                                obj_1.rect.y <= pygame.mouse.get_pos()[1] <= obj_1.rect.y + obj_1.rect.h) \
                                and music_vloume_en_edit:
                            if obj_1.type == '+':
                                if Music_Volume != 10:
                                    Music_Volume += 1
                            elif obj_1.type == '-':
                                if Music_Volume != 0:
                                    Music_Volume -= 1
                            pygame.mixer.music.set_volume(Music_Volume * 10 / 100)
                        elif obj_1.rect.x <= pygame.mouse.get_pos()[0] <= obj_1.rect.x + obj_1.rect.w and (
                                obj_1.rect.y <= pygame.mouse.get_pos()[1] <= obj_1.rect.y + obj_1.rect.h) \
                                and effects_volume_en_edit:
                            if obj_1.type == '+':
                                if Effects_Volume != 10:
                                    Effects_Volume += 1
                            elif obj_1.type == '-':
                                if Effects_Volume != 0:
                                    Effects_Volume -= 1
                            for eff in mixer_sounds:
                                eff.set_volume(Effects_Volume * 10 / 100)

            elif settings_ev_activity.type == pygame.KEYDOWN:
                if settings_ev_activity.key == pygame.K_DOWN:
                    if cursor_position + 1 < len(settings_buttons_sprites.sprites()):
                        cursor_position += 1
                    else:
                        cursor_position = 0
                elif settings_ev_activity.key == pygame.K_UP:
                    if cursor_position - 1 >= 0:
                        cursor_position -= 1
                    else:
                        cursor_position = len(settings_buttons_sprites.sprites()) - 1
                elif settings_ev_activity.key == pygame.K_RETURN:
                    obj = settings_buttons_sprites.sprites()[cursor_position]
                    if obj.type == 'menu' or obj.type == 'esc_menu':
                        if curr_song == "menu_song":
                            return 'menu'
                        else:
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
            for obj_1 in range(Music_Volume if music_vloume_en_edit else Effects_Volume):
                pygame.draw.rect(screen, (255, 255, 255), (int(SIZE_OF_RECT * 13.3) + obj_1 * small_size_1 * 2,
                                                           SIZE_OF_RECT * 17 // 13 + SIZE_OF_RECT * 4,
                                                           small_size_2, small_size_1))
            for obj_1 in range(Music_Volume if music_vloume_en_edit else Effects_Volume, 10):
                pygame.draw.rect(screen, (120, 120, 120), (int(SIZE_OF_RECT * 13.3) + obj_1 * small_size_1 * 2,
                                                           SIZE_OF_RECT * 17 // 13 + SIZE_OF_RECT * 4,
                                                           small_size_2, small_size_1))
            settings_buttons_sprites_sound.draw(screen)
        # переворот изображения, это чтобы не отрисовывались отдльные части
        pygame.display.flip()


def new_game():
    global dif
    diff_select_open = False
    diff_btn = pygame.sprite.Group()
    for elem in standard_diff_btns:
        diff_btn.add(elem)
    while True:
        # Держим цикл на правильной скорости
        clock.tick(FPS)
        # Ввод процесса (события)
        for ng_ev_activity in pygame.event.get():
            # проверка для закрытия окна
            if ng_ev_activity.type == pygame.QUIT:
                return 'exit'
            if ng_ev_activity.type == pygame.MOUSEBUTTONDOWN:
                for but in diff_btn:
                    if but.is_clicked():
                        if but.type == 'diff_select':
                            diff_btn.empty()
                            for name, returner in [('1', -25), ('2', 0), ('3', 25), ('_', 25 * (dif - 1))]:
                                one_btn = font_sh.render(name, True, (245, 245, 245))
                                y1_params = SIZE_OF_RECT * 17 // 15 + SIZE_OF_RECT * 4
                                diff_btn.add(Button(one_btn, one_btn.get_rect(centerx=SIZE_OF_RECT * 15 + returner,
                                                                              y=y1_params), name))
                            count_1 = 1
                            for name, returner in [("Сложность", ''), ("Назад", 'back')]:
                                one_btn = font_sh.render(name, True, (245, 245, 245))
                                diff_btn.add(
                                    Button(one_btn,
                                           one_btn.get_rect(centerx=SIZE_OF_RECT * 15,
                                                            y=SIZE_OF_RECT * 17 // 15 + SIZE_OF_RECT * (2 + count_1)),
                                           returner))
                                count_1 += 2
                            diff_select_open = True
                        else:
                            if diff_select_open:
                                if but.type == '1':
                                    for but_1 in diff_btn:
                                        if but_1.type == '_':
                                            but_1.rect.centerx = SIZE_OF_RECT * 15 - 25
                                        dif = 0
                                elif but.type == '2':
                                    for but_1 in diff_btn:
                                        if but_1.type == '_':
                                            but_1.rect.centerx = SIZE_OF_RECT * 15
                                        dif = 1
                                elif but.type == '3':
                                    for but_1 in diff_btn:
                                        if but_1.type == '_':
                                            but_1.rect.centerx = SIZE_OF_RECT * 15 + 25
                                        dif = 2
                                elif but.type == 'back':
                                    diff_select_open = False
                                    diff_btn.empty()
                                    for elem in standard_diff_btns:
                                        diff_btn.add(elem)
                            else:
                                if but.type == 'new_game':
                                    return 'dif ' + str(dif)
                                elif but.type == 'menu':
                                    return 'menu'
        screen.blit(dif_set_image, (0, 0))
        diff_btn.draw(screen)
        pygame.display.flip()


def load_func():
    closed_mass = [f"saves\\{f_name}" for f_name in os.listdir(path=f"{os.getcwd()}\\saves")]
    closed_mass.remove('saves\\new_game')
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
        for load_ev_activity in pygame.event.get():
            # проверка для закрытия окна
            if load_ev_activity.type == pygame.QUIT:
                return 'exit'
            elif load_ev_activity.type == pygame.MOUSEBUTTONDOWN:
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
x, y = inf.current_w / 30, inf.current_h / 17
if x > y:
    SIZE_OF_RECT = int(y)
else:
    SIZE_OF_RECT = int(x)
WIDTH = inf.current_w
HEIGHT = inf.current_h
FPS = 60
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN | pygame.DOUBLEBUF | pygame.HWSURFACE)
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
bomb_sprites = pygame.sprite.Group()
wall_sprites = Wal_sprite(SIZE_OF_RECT, decor_sprites, bonus_sprites, particle_sprites, dust_particle_sprites,
                          saves_sprites, damage_sprites, enemies_sprites, bomb_sprites, screen)
player_sprites = pygame.sprite.Group()
gui_sprites = Gui(SIZE_OF_RECT)
render = Render(screen, player_sprites, wall_sprites, decor_sprites, bonus_sprites, gui_sprites,
                dust_particle_sprites, particle_sprites, saves_sprites, damage_sprites, enemies_sprites, bomb_sprites)

player = Player((SIZE_OF_RECT * 14, SIZE_OF_RECT * 8), player_sprites, wall_sprites, bonus_sprites, gui_sprites,
                particle_sprites, dust_particle_sprites, saves_sprites, damage_sprites, enemies_sprites, bomb_sprites,
                SIZE_OF_RECT)
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
dif = 0
standard_diff_btns = pygame.sprite.Group()
count = 1
for i, j in [("Начать", 'new_game'), ("Сложность", 'diff_select'), ("Выход в меню", 'menu')]:
    text = font_sh.render(i, True, (245, 245, 245))
    standard_diff_btns.add(Button(text, text.get_rect(centerx=SIZE_OF_RECT * 15,
                                                      y=SIZE_OF_RECT * 17 // 15 + SIZE_OF_RECT * (2 + count)), j))
    count += 1

#  settings funk
settings_background_image = pygame.transform.scale(pygame.image.load('fons\\option_background.png').convert(),
                                                   (WIDTH, HEIGHT))
settings_decoration_image = pygame.transform.scale(pygame.image.load('fons\\menu_illustration.png').convert(),
                                                   (SIZE_OF_RECT * 12, SIZE_OF_RECT * 3))
settings_decoration_image.set_colorkey((0, 0, 0))
Music_Volume = 3
Effects_Volume = 3
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

# music and effects settings
music_vloume_en_edit = False
effects_volume_en_edit = False
pygame.mixer.music.load('music&effects/music/menu/Florian Christl - Close Your Eyes.mp3')
klonk_sound = mixer.Sound('music&effects/effects/klonk.wav')
anti_klonk = mixer.Sound('music&effects/effects/miss_sound_cutted.wav')
hopp = mixer.Sound('music&effects/effects/ez_jump_st_boosted.wav')
incoming_damage_sound = mixer.Sound('music&effects/effects/incoming_damage.wav')
curr_song = 'menu_song'
mixer_sounds = [klonk_sound, anti_klonk, hopp, incoming_damage_sound]

count = 1
for i, j in [ ("Громкость музыки", 'music_volume'), ("Громкость эффектов", 'effects_volume'), ("Назад", 'esc_menu')]:
    text = font_sh.render(i, True, (245, 245, 245))
    settings_buttons_sprites.add(Button(text, text.get_rect(centerx=SIZE_OF_RECT * 15,
                                                            y=SIZE_OF_RECT * 17 // 15 + SIZE_OF_RECT * (2 + count)), j))
    count += 1

cursor_position = 0
cursor = pygame.sprite.Sprite()
cursor.image = pygame.transform.scale(pygame.image.load('fons\\cursor.png').convert(), (SIZE_OF_RECT, SIZE_OF_RECT))
pygame.mixer.music.play()
cursor.image.set_colorkey((255, 255, 255))
cursor.rect = cursor.image.get_rect()
cursor.rect.x = settings_buttons_sprites.sprites()[cursor_position].rect.x - settings_buttons_sprites.sprites()[
    0].rect.w // 2 - 5
cursor.rect.y = settings_buttons_sprites.sprites()[cursor_position].rect.y
cursor_sprites = pygame.sprite.Group(cursor)

name_tag()
result = menu()
name_of_save = ''
last_result = ''
while True:
    if result == 'new_game':
        name_of_save = new_game()
        if name_of_save.startswith('dif'):
            mass = [f"saves\\{fname}" for fname in os.listdir(path=f"{os.getcwd()}\\saves")]
            mass.remove('saves\\new_game')
            if len(mass) <= 8: result = 'new'
        else:
            result = name_of_save
    elif result == 'new':
        mass = [f"saves\\{fname}" for fname in os.listdir(path=f"{os.getcwd()}\\saves")]
        mass.remove('saves\\new_game')
        mass.sort()
        name_of_save = 'saves\\data_file_' + str(int(mass[-1].split('.')[0][-1]) + 1) + '.json'
        copy('saves\\new_game\\' + str(dif) + '.json', name_of_save)
        result = 'load'
    elif result == 'load':
        t1 = threading.Thread(target=screen_saver)
        t2 = threading.Thread(target=load_1, args=name_of_save)
        t1.start()
        t2.start()
        t2.join()
        t1.join()
        result = 'main'
        mixer.music.stop()
        mixer.music.unload()
        mixer.music.load('music&effects/music/world/To The Abyss.mp3')
        curr_song = 'world_song'
        mixer.music.play()
    elif result == 'load_game':
        name_of_save = load_func()
        if not name_of_save == 'menu':
            result = 'load'
        else:
            result = name_of_save
    elif result == 'menu':
        if mixer.music.get_busy():
            if curr_song == 'world_song':
                mixer.music.stop()
                mixer.music.unload()
                mixer.music.load('music&effects/music/menu/Florian Christl - Close Your Eyes.mp3')
                mixer.music.play()
                curr_song = 'menu_song'
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
    elif result == 'freeze':
        result = freeze()
    elif result == 'game_over':
        result = game_over()
