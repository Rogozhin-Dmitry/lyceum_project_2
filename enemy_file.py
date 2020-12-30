from pygame import sprite, image, transform, Rect, key
from brick import *
import pygame


class Enemy(Brick):  # общий класс всех врагов
    def __init__(self, cords, rect_size, image_name, wall_sprites, damage_sprites, mask=False, shift=(0, 0)):
        super().__init__(cords, rect_size, image_name, mask=mask, shift=shift)
        self.wall_sprites = wall_sprites
        self.damage_sprites = damage_sprites
        self.timer = 0
        self.last_timer = 0
        self.step = 5
        self.rl = True
        self.count = 0
        self.init()

    def init(self):
        pass


class Crash(Enemy):
    def init(self):
        pass

    def update(self):
        super().update()

        if self.rl:
            self.rect.x += self.step
            if sprite.spritecollideany(self, self.wall_sprites):
                while sprite.spritecollideany(self, self.wall_sprites):
                    self.rect.x -= 1
                self.rl = False
            if sprite.spritecollideany(self, self.damage_sprites):
                while sprite.spritecollideany(self, self.damage_sprites):
                    self.rect.x -= 1
                self.rl = False
        else:
            self.rect.x -= self.step
            if sprite.spritecollideany(self, self.wall_sprites):
                while sprite.spritecollideany(self, self.wall_sprites):
                    self.rect.x += 1
                self.rl = True
            if sprite.spritecollideany(self, self.damage_sprites):
                while sprite.spritecollideany(self, self.damage_sprites):
                    self.rect.x += 1
                self.rl = True
        self.rect.y += self.step
        if sprite.spritecollideany(self, self.wall_sprites):
            while sprite.spritecollideany(self, self.wall_sprites):
                self.rect.y -= 1
        else:
            self.rect.y -= self.step
            if self.rl:
                self.rl = False
            else:
                self.rl = True


# Заготовки врагов, чтобы не забыть
# class ChesBoy(Enemy):
#     def __init__(self, cords, rect_size):
#         super().__init__(cords, rect_size)
#         self.damage = 1
#         self.step = 2
#         self.type = 'chesboy'
#         self.img_left = transform.scale(image.load('enemies\\chesboy.png').convert(), rect_size)
#         self.img_right = transform.flip(self.img_left, True, False)
#         self.image = transform.scale(image.load('enemies\\chesboy.png').convert(), rect_size)
#         self.image.set_colorkey((255, 255, 255))
#
#     def update(self):
#         self.rect.x = self.rect.x + self.step
#
#
# class Fly(Enemy):
#     def __init__(self, cords, rect_size):
#         super().__init__(cords, rect_size)
#         self.damage = 1
#         self.step = 2
#         self.type = 'fly'
#
#     def update(self):
#         pass
