from pygame import sprite, image, transform, key, Surface, draw
from random import randint, choice


def up_collision(obj_1, obj_2):
    return (obj_2.rect.x < obj_1.rect.x < obj_2.rect.x + obj_2.rect.w or obj_2.rect.x
            < obj_1.rect.x + obj_1.rect.w < obj_2.rect.x + obj_2.rect.w or obj_2.rect.x == obj_1.rect.x
            or obj_2.rect.x + obj_2.rect.w == obj_1.rect.x + obj_1.rect.w) and \
           (obj_2.rect.y < obj_1.rect.y < obj_2.rect.y + obj_2.rect.w)


def down_collision(obj_1, obj_2):
    return (obj_2.rect.x < obj_1.rect.x < obj_2.rect.x + obj_2.rect.w or obj_2.rect.x
            < obj_1.rect.x + obj_1.rect.w < obj_2.rect.x + obj_2.rect.w or obj_2.rect.x == obj_1.rect.x
            or obj_2.rect.x + obj_2.rect.w == obj_1.rect.x + obj_1.rect.w) and \
           (obj_2.rect.y < obj_1.rect.y + obj_1.rect.h < obj_2.rect.y + obj_2.rect.w)


class Player(sprite.Sprite):
    def __init__(self, cords, sprites, wall_sprites, bonus_sprites, gui_sprites, particle_sprites, rect_size):
        super().__init__()
        self.rect_size = rect_size
        self.sprite_group = sprites
        self.bonus_sprites = bonus_sprites
        self.wall_sprites = wall_sprites
        self.gui_sprites = gui_sprites
        self.particle_sprites = particle_sprites
        self.player_img_left_run = []
        self.player_img_right_run = []
        self.player_img_left = transform.scale(image.load('player\\player.png').convert(),
                                               (rect_size - 5, rect_size * 2 - 5))
        self.player_img_right = transform.flip(self.player_img_left, True, False)
        for i in range(6):
            self.player_img_left_run.append(transform.scale(image.load('player\\' + str(i + 1) + '.png').convert(),
                                                            (rect_size - 5, rect_size * 2 - 5)))
            self.player_img_right_run.append(transform.flip(self.player_img_left_run[-1], True, False))
        self.image = self.player_img_left
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = cords
        self.sprite_group.add(self)

        self.step = 5
        self.left_scroll = rect_size * 12
        self.right_scroll = rect_size * 18
        self.up_scroll = rect_size * 8
        self.down_scroll = rect_size * 14
        self.g = 1  # изменить в финальной версии

        self.jump = False
        self.start_jump_tick = 0
        self.jump_speed = 0
        self.count = 0
        self.rl = False
        self.timer = 0
        self.last_timer = 0
        self.jump_speed_last = self.jump_speed

    def update(self):  # метод вызываемы при обновлении (каждый кадр),
        # убью если загрузите какими-либо долгими вычислениями, долгими считаются больше 1/60 секунды
        super().update()

        keys = key.get_pressed()
        if keys[100]:
            if self.rl:
                self.rl = False
                self.count = 0
            if self.timer - self.last_timer >= 5:
                self.image = self.player_img_right_run[self.count % 6]
                self.image.set_colorkey((255, 255, 255))
                self.count += 1
                self.last_timer = self.timer
            # проверка на стены
            self.rect.x += self.step
            if sprite.spritecollideany(self, self.wall_sprites):
                while sprite.spritecollideany(self, self.wall_sprites):
                    self.rect.x -= 1

            while self.right_scroll < self.rect.x:
                self.wall_sprites.move(-self.step, 0)
                self.rect.x -= self.step

        if keys[97]:
            if not self.rl:
                self.rl = True
                self.count = 0
            if self.timer - self.last_timer >= 5:
                self.image = self.player_img_left_run[self.count % 6]
                self.image.set_colorkey((255, 255, 255))
                self.count += 1
                self.last_timer = self.timer

            # проверка на стены
            self.rect.x -= self.step
            if sprite.spritecollideany(self, self.wall_sprites):
                while sprite.spritecollideany(self, self.wall_sprites):
                    self.rect.x += 1

            while self.left_scroll > self.rect.x:
                self.wall_sprites.move(self.step, 0)
                self.rect.x += self.step

        if not keys[100] and not keys[97]:
            if self.rl:
                self.image = self.player_img_left
                self.image.set_colorkey((255, 255, 255))
            else:
                self.image = self.player_img_right
                self.image.set_colorkey((255, 255, 255))
            self.last_timer = 0

        if keys[32] and not self.jump:
            self.rect.y += 1
            if sprite.spritecollideany(self, self.wall_sprites):  # проверка что персоонаж на полу
                self.jump = True
                self.jump_speed = -17
            self.rect.y -= 1

        self.rect.y += self.jump_speed + self.g // 2

        if sprite.spritecollideany(self, self.wall_sprites, collided=up_collision):
            while sprite.spritecollideany(self, self.wall_sprites, collided=up_collision):
                self.rect.y += 1
            self.jump_speed = self.jump_speed

        if sprite.spritecollideany(self, self.wall_sprites, collided=down_collision):
            while sprite.spritecollideany(self, self.wall_sprites, collided=down_collision):
                self.rect.y -= 1
            self.jump_speed = 0

        while self.rect.y + self.rect.h > self.down_scroll:  # TODO плавное передвижение камеры
            self.rect.y -= 1
            self.wall_sprites.move(-1, 1)

        while self.rect.y < self.up_scroll:
            self.rect.y += 1
            self.wall_sprites.move(1, 1)

        if self.jump:
            self.jump_speed += self.g
            if self.jump_speed >= 0:
                self.jump = False
                self.jump_speed = 0
        else:
            self.jump_speed += self.g
            if self.jump_speed >= 30:
                self.jump_speed = 30

        self.timer += 1

        spr = sprite.spritecollideany(self, self.bonus_sprites)
        if spr:
            if spr.image_name == 'tiles\\bonus\\heart_bonus.png':
                self.gui_sprites.set_hearts(self.gui_sprites.hp + 1)
            elif spr.image_name == 'tiles\\bonus\\bomb_bonus.png':
                self.gui_sprites.set_bombs(self.gui_sprites.bomb + 1)
            cords = spr.rect.center
            del self.wall_sprites.maps[tuple(spr.cords)]
            spr.kill()
            del spr

            for i in range(10):
                cords = randint(cords[0] - 5, cords[0] + 5),  randint(cords[1] - 5, cords[1] + 5)
                spr = sprite.Sprite()
                r = randint(9, 15)
                spr.image = Surface([r, r])
                draw.circle(spr.image, (120, 255, 255), (r // 2, r // 2), r // 2)
                spr.image.set_colorkey((0, 0, 0))
                spr.rect = spr.image.get_rect()
                spr.rect.center = cords
                spr.x, spr.y = cords
                spr.down = cords[1] + self.rect_size * 0.5
                spr.shift_up = 0.3
                spr.shift, spr.shift_down = randint(-20, 20) / 10, -4

                self.particle_sprites.add(spr)

        # if not (self.jump_speed == self.jump_speed_last) and (self.jump_speed == 1   and self.jump_speed_last) or \
        #         (self.jump_speed == -1 and self.jump_speed_last):  # срабатывает при падении с зажатием пробела
        if not (self.jump_speed == self.jump_speed_last) and (self.jump_speed == 1 and self.jump_speed_last):
            cords = self.rect.center[0], self.rect.y + self.rect.h - 15
            for i in range((self.jump_speed_last - self.jump_speed) // 2):
                spr = sprite.Sprite()
                r = randint(5, 9)
                spr.image = Surface([r, r])
                draw.circle(spr.image, (5, 5, 5), (r // 2, r // 2), r // 2)
                spr.image.set_colorkey((0, 0, 0))
                spr.rect = spr.image.get_rect()
                spr.rect.center = cords
                spr.rect.y = cords[1]
                spr.x, spr.y = cords
                spr.down = cords[1] + 15
                spr.shift_up = 0.1
                spr.shift, spr.shift_down = randint(-20, 20) / 20, -1

                self.particle_sprites.add(spr)
            print('персоонаж на земле, ура, частички, частички, частички, частички')
        self.jump_speed_last = self.jump_speed
