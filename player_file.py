from pygame import key, Surface, draw
from random import randint
import pygame
from brick import *


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
    def __init__(self, cords, sprites, wall_sprites, bonus_sprites, gui_sprites, particle_sprites,
                 dust_particle_sprites, saves_sprites, damage_sprites, enemies_sprites, bomb_sprites, rect_size):
        super().__init__()
        self.rect_size = rect_size
        self.sprite_group = sprites
        self.bonus_sprites = bonus_sprites
        self.wall_sprites = wall_sprites
        self.gui_sprites = gui_sprites
        self.particle_sprites = particle_sprites
        self.dust_particle_sprites = dust_particle_sprites
        self.saves_sprites = saves_sprites
        self.damage_sprites = damage_sprites
        self.enemies_sprites = enemies_sprites
        self.bomb_sprites = bomb_sprites
        self.player_img_left_run = []
        self.player_img_right_run = []
        self.player_clear_img = pygame.Surface((rect_size - 5, rect_size * 2 - 5))
        pygame.draw.rect(self.player_clear_img, (255, 255, 255), (0, 0, rect_size - 5, rect_size * 2 - 5))

        self.player_img_left = transform.scale(image.load('player\\player.png').convert(),
                                               (rect_size - 5, rect_size * 2 - 5))
        self.player_img_right = transform.flip(self.player_img_left, True, False)
        for i in range(6):
            self.player_img_left_run.append(transform.scale(image.load('player\\' + str(i + 1) + '.png').convert(),
                                                            (rect_size - 5, rect_size * 2 - 5)))
            self.player_img_right_run.append(transform.flip(self.player_img_left_run[-1], True, False))
        self.image = self.player_img_left
        self.image.set_colorkey((255, 255, 255))
        self.bun_image_left = transform.scale(image.load('player\\mini_bun\\1.png').convert(),
                                              (rect_size - 5, rect_size - 5))
        self.bun_image_right = transform.flip(self.bun_image_left, True, False)
        self.bun_image_left_run = []
        self.bun_image_right_run = []
        for i in range(3):
            self.bun_image_left_run.append(transform.scale(
                image.load('player\\mini_bun\\' + str(i + 1) + '.png').convert(), (rect_size - 5, rect_size - 5)))
            self.bun_image_right_run.append(transform.flip(self.bun_image_left_run[i], True, False))
        self.player_hit_img_right = []
        self.player_hit_img_left = []
        for i in range(4):
            self.player_hit_img_right.append(
                transform.scale(image.load('player\\hit\\' + str(i + 1) + '.png').convert(),
                                (rect_size * 2 - 10, rect_size * 2 - 5)))
            self.player_hit_img_left.append(transform.flip(self.player_hit_img_right[-1], True, False))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = cords
        self.sprite_group.add(self)
        self.rect_size = rect_size

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
        self.put_bomb = True
        self.bunny_mode = False
        self.mode_changed = False
        self.hit_mode = False
        self.last_timer_damage = -121
        self.hit_timer = 0
        self.hit_animation_timer = 0
        self.hit_animation_timer_event = 15 // len(self.player_hit_img_left) + 1
        self.hit_event = True
        self.hit_animation_count = 0
        self.hit_rect = Rect(0, 0, 0, 0)

        self.test_damage = True  # TODO удалить это

    def update(self):  # метод вызываемы при обновлении (каждый кадр),
        # убью если загрузите какими-либо долгими вычислениями, долгими считаются больше 1/60 секунды
        super().update()

        keys = key.get_pressed()

        if sprite.spritecollideany(self, self.saves_sprites) and keys[pygame.K_e]:
            pygame.event.post(pygame.event.Event(30, {}))
            for save in self.saves_sprites.sprites():
                if sprite.collide_rect(self, save):
                    save.player_is_sitting = True

        if keys[pygame.K_c] and not self.mode_changed:
            if not self.bunny_mode:
                last_x = self.rect.x
                last_y = self.rect.y
                self.bunny_mode = True
                self.image = self.bun_image_left
                self.rect = self.image.get_rect()
                self.rect.x = last_x
                self.rect.y = last_y + self.rect_size
            else:
                last_x = self.rect.x
                last_y = self.rect.y
                self.bunny_mode = False
                self.image = self.player_img_left
                self.rect = self.image.get_rect()
                self.rect.x = last_x
                self.rect.y = last_y - self.rect_size
                if sprite.spritecollideany(self, self.wall_sprites):
                    self.bunny_mode = True
                    self.image = self.bun_image_left
                    self.rect = self.image.get_rect()
                    self.rect.y = last_y
                    self.rect.x = last_x

            self.mode_changed = True
        elif not keys[pygame.K_c]:
            self.mode_changed = False

        if (keys[100] or keys[pygame.K_RIGHT]) and not self.hit_mode:
            if self.rl:
                self.rl = False
                self.count = 0
            if self.timer - self.last_timer >= 5:
                if not self.bunny_mode:
                    self.image = self.player_img_right_run[self.count % 6]
                else:
                    self.image = self.bun_image_right_run[self.count % 3]
                self.image.set_colorkey((255, 255, 255))
                self.count += 1
                self.last_timer = self.timer
            # проверка на стены
            self.rect.x += self.step
            if sprite.spritecollideany(self, self.wall_sprites):
                while sprite.spritecollideany(self, self.wall_sprites):
                    self.rect.x -= 1

            spr = sprite.spritecollideany(self, self.damage_sprites)
            if spr:
                if spr.image_name == 'tiles\\damage\\spike.png':
                    while sprite.spritecollideany(self, self.damage_sprites):
                        self.rect.x -= 1

            while self.right_scroll < self.rect.x:
                self.wall_sprites.move(-self.step, 0)
                self.rect.x -= self.step

        if (keys[97] or keys[pygame.K_LEFT]) and not self.hit_mode:
            if not self.rl:
                self.rl = True
                self.count = 0
            if self.timer - self.last_timer >= 5:
                if not self.bunny_mode:
                    self.image = self.player_img_left_run[self.count % 6]
                else:
                    self.image = self.bun_image_left_run[self.count % 3]
                self.image.set_colorkey((255, 255, 255))
                self.count += 1
                self.last_timer = self.timer

            # проверка на стены
            self.rect.x -= self.step
            if sprite.spritecollideany(self, self.wall_sprites):
                while sprite.spritecollideany(self, self.wall_sprites):
                    self.rect.x += 1

            spr = sprite.spritecollideany(self, self.damage_sprites)
            if spr:
                if spr.image_name == 'tiles\\damage\\spike.png':
                    while sprite.spritecollideany(self, self.damage_sprites):
                        self.rect.x += 1

            while self.left_scroll > self.rect.x:
                self.wall_sprites.move(self.step, 0)
                self.rect.x += self.step

        if not keys[100] and not keys[97] and not keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT] \
                and not self.hit_mode:
            if self.rl:
                if not self.bunny_mode:
                    self.image = self.player_img_left
                else:
                    self.image = self.bun_image_left
                self.image.set_colorkey((255, 255, 255))
            else:
                if not self.bunny_mode:
                    self.image = self.player_img_right
                else:
                    self.image = self.bun_image_right
                self.image.set_colorkey((255, 255, 255))
            self.last_timer = 0

        if (keys[32] or keys[pygame.K_z]) and not self.jump and not self.hit_mode:
            self.rect.y += 1
            if sprite.spritecollideany(self, self.wall_sprites):  # проверка что персоонаж на полу
                self.jump = True
                self.jump_speed = -17
            self.rect.y -= 1

        if keys[pygame.K_k] and self.test_damage:  # тестовая система жизней
            self.gui_sprites.set_hearts(self.gui_sprites.hp - 1)
            self.test_damage = False
        elif not keys[pygame.K_k]:
            self.test_damage = True

        if keys[pygame.K_q] and self.timer - self.hit_timer > 15 and self.hit_event:
            self.rect.y += 1
            if sprite.spritecollideany(self, self.wall_sprites):  # проверка что персоонаж на полу
                self.rect.y -= 1
                if not self.rl:
                    self.hit_rect = Rect(self.rect.right, self.rect.y, self.rect.w, self.rect.h)
                    self.image = self.player_hit_img_left[0]
                    self.hit_animation_count = 0
                else:
                    self.hit_rect = Rect(self.rect.x - self.rect.w, self.rect.y, self.rect.w, self.rect.h)
                    self.image = self.player_hit_img_right[0]
                    self.hit_animation_count = 0
                    self.rect.x -= self.rect.w
                for i in self.wall_sprites:
                    if Rect.colliderect(self.hit_rect, i):
                        if self.rl:
                            self.rect.x += self.rect.w
                            self.image = self.player_img_left
                        else:
                            self.image = self.player_img_right
                        self.image.set_colorkey((255, 255, 255))
                        self.last_timer = 0
                        return None
                self.image.set_colorkey((255, 255, 255))
                self.hit_timer = self.timer
                self.hit_event = False
                self.hit_mode = True
            else:
                self.rect.y -= 1
        elif self.hit_mode and self.timer - self.hit_timer < 15:
            for i in self.enemies_sprites:
                if Rect.colliderect(self.hit_rect, i.rect):
                    del self.wall_sprites.maps[tuple(i.cords)]
                    i.kill()
                    del i
            if self.timer - self.hit_animation_timer >= self.hit_animation_timer_event:
                if not self.rl:
                    self.image = self.player_hit_img_left[self.hit_animation_count]
                else:
                    self.image = self.player_hit_img_right[self.hit_animation_count]
                self.image.set_colorkey((255, 255, 255))
                self.hit_animation_count += 1
                self.hit_animation_timer = self.timer
        elif self.hit_mode and self.timer - self.hit_timer > 15:
            self.hit_mode = False
            for i in self.enemies_sprites:
                if Rect.colliderect(self.hit_rect, i.rect):
                    del self.wall_sprites.maps[tuple(i.cords)]
                    i.kill()
                    del i
            if self.rl:
                self.rect.x += self.rect.w
                self.image = self.player_img_left
            else:
                self.image = self.player_img_right
            self.image.set_colorkey((255, 255, 255))
            self.last_timer = 0
        elif not keys[pygame.K_q]:
            self.hit_event = True

        if keys[pygame.K_l] and self.put_bomb:
            if self.gui_sprites.bomb != 0:
                bomb = Bomb(self.rect.center, (self.rect_size, self.rect_size), self.wall_sprites, self)
                bomb.rl = self.rl
                self.bomb_sprites.add(bomb)
                self.gui_sprites.set_bombs(self.gui_sprites.bomb - 1)
                self.put_bomb = False
        elif not keys[pygame.K_l]:
            self.put_bomb = True


        if not self.hit_mode:
            self.rect.y += self.jump_speed + self.g // 2

            if sprite.spritecollideany(self, self.wall_sprites, collided=up_collision):
                while sprite.spritecollideany(self, self.wall_sprites, collided=up_collision):
                    self.rect.y += 1
                self.jump_speed = self.jump_speed
            if sprite.spritecollideany(self, self.damage_sprites, collided=up_collision):
                while sprite.spritecollideany(self, self.damage_sprites, collided=up_collision):
                    self.rect.y += 1
                self.jump_speed = self.jump_speed
            if sprite.spritecollideany(self, self.wall_sprites, collided=down_collision):
                while sprite.spritecollideany(self, self.wall_sprites, collided=down_collision):
                    self.rect.y -= 1
                self.jump_speed = 0

            while self.rect.y + self.rect.h > self.down_scroll:
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

        if not self.hit_mode:
            if sprite.spritecollideany(self, self.damage_sprites, collided=down_collision):
                while sprite.spritecollideany(self, self.damage_sprites, collided=down_collision):
                    self.rect.y -= 1
                self.jump_speed = 0
                if self.timer - self.last_timer_damage >= 120:
                    self.gui_sprites.set_hearts(self.gui_sprites.hp - 1)
                    self.last_timer_damage = self.timer

            if 15 < self.timer - self.last_timer_damage <= 30 or 45 < self.timer - self.last_timer_damage <= 60 \
                    or 75 < self.timer - self.last_timer_damage <= 90 or 105 < self.timer - self.last_timer_damage <= 120 \
                    and not self.hit_mode:
                self.image = self.player_clear_img
                self.image.set_colorkey((255, 255, 255))

            spr = sprite.spritecollideany(self, self.bonus_sprites)
            if spr:
                if spr.image_name == 'tiles\\bonus\\heart_bonus.png':
                    self.gui_sprites.max_hp = self.gui_sprites.max_hp + 1
                    self.gui_sprites.set_hearts(self.gui_sprites.max_hp)
                elif spr.image_name == 'tiles\\bonus\\bomb_bonus.png':
                    self.gui_sprites.max_bomb = self.gui_sprites.max_bomb + 1
                    self.gui_sprites.set_bombs(self.gui_sprites.max_bomb)
                cords = spr.rect.center
                del self.wall_sprites.maps[tuple(spr.cords)]
                spr.kill()
                del spr

                for i in range(10):
                    cords = randint(cords[0] - 5, cords[0] + 5), randint(cords[1] - 5, cords[1] + 5)
                    spr = sprite.Sprite()
                    r = randint(9, 15)
                    spr.image = Surface([r, r])
                    draw.circle(spr.image, (120, 235, 255), (r // 2, r // 2), r // 2)
                    spr.image.set_colorkey((0, 0, 0))
                    spr.rect = spr.image.get_rect()
                    spr.rect.center = cords
                    spr.x, spr.y = cords
                    spr.down = cords[1] + self.rect_size * 0.5
                    spr.shift_up = 0.3
                    spr.shift, spr.shift_down = randint(-20, 20) / 10, -4

                    self.particle_sprites.add(spr)

            if not (self.jump_speed == self.jump_speed_last) and (self.jump_speed == 1 and self.jump_speed_last):
                cords = self.rect.center[0], self.rect.y + self.rect.h - 15
                for i in range((self.jump_speed_last - self.jump_speed) // 2):
                    spr = sprite.Sprite()
                    r = randint(5, 9)
                    spr.image = Surface([r, r])
                    draw.circle(spr.image, (150, 75, 0), (r // 2, r // 2), r // 2)
                    spr.image.set_colorkey((0, 0, 0))
                    spr.rect = spr.image.get_rect()
                    spr.rect.center = cords
                    spr.rect.y = cords[1]
                    spr.x, spr.y = cords
                    spr.down = cords[1] + 15
                    spr.shift_up = 0.1
                    spr.shift, spr.shift_down = randint(-50, 50) / 20, -1
                    self.dust_particle_sprites.add(spr)
            self.jump_speed_last = self.jump_speed

            for i in self.enemies_sprites:
                if ((i.rect.center[0] - self.rect.center[0]) ** 2 + (i.rect.center[1] - self.rect.center[1]) ** 2) ** 0.5 \
                        < self.rect_size * 3:
                    if sprite.collide_rect(self, i):
                        if self.timer - self.last_timer_damage >= 120:
                            self.gui_sprites.set_hearts(self.gui_sprites.hp - 1)
                            self.last_timer_damage = self.timer

        self.timer += 1
