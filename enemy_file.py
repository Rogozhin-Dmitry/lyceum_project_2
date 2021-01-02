from pygame import sprite, image, transform, Rect, key
from brick import *
import pygame
inf = pygame.display.Info()
x, y = inf.current_w // 30, inf.current_h // 17
if x > y:
    SIZE_OF_RECT = int(y)
else:
    SIZE_OF_RECT = int(x)
WIDTH = SIZE_OF_RECT * 30
HEIGHT = SIZE_OF_RECT * 17


class Enemy(Brick):  # общий класс всех врагов
    def __init__(self, cords, rect_size, image_name, wall_sprites, damage_sprites, mask=False, shift=(0, 0)):
        super().__init__(cords, rect_size, image_name, mask=mask, shift=shift)
        self.wall_sprites = wall_sprites
        self.damage_sprites = damage_sprites
        self.cords = cords
        self.is_target = False
        self.cords_not_round = [self.cords[0] * SIZE_OF_RECT, self.cords[1] * SIZE_OF_RECT]
        self.delay = (0, 0)


class Crash(Enemy):
    def __init__(self, cords, rect_size, image_name, wall_sprites, damage_sprites, mask=False, shift=(0, 0)):
        super().__init__(cords, rect_size, image_name, wall_sprites, damage_sprites, mask=mask, shift=shift)
        self.step = 5
        self.step_1 = self.step / SIZE_OF_RECT
        self.rl = True
        self.count = 0

    def update(self):
        super().update()
        if self.is_target:
            self.target()
        else:
            self.standard()

    def target(self):
        pass

    def standard(self):
        if self.rl:
            self.rect.x += self.step
            if sprite.spritecollideany(self, self.wall_sprites):
                while sprite.spritecollideany(self, self.wall_sprites):
                    self.rect.x -= 1
                self.rl = False
            elif sprite.spritecollideany(self, self.damage_sprites):
                while sprite.spritecollideany(self, self.damage_sprites):
                    self.rect.x -= 1
                self.rl = False
            else:
                self.cords_not_round[0] += 1
                self.shift[0] += self.step_1
                self.delay[0] += self.step_1
        else:
            self.rect.x -= self.step
            if sprite.spritecollideany(self, self.wall_sprites):
                while sprite.spritecollideany(self, self.wall_sprites):
                    self.rect.x += 1
                self.rl = True
            elif sprite.spritecollideany(self, self.damage_sprites):
                while sprite.spritecollideany(self, self.damage_sprites):
                    self.rect.x += 1
                self.rl = True
            else:
                self.cords_not_round[0] -= 1
                self.shift[0] -= self.step_1
                self.delay[0] -= self.step_1
        if self.rect.right >= 0 and self.rect.x <= WIDTH:
            self.rect.x -= SIZE_OF_RECT - self.step
            self.rect.y += self.step
            if sprite.spritecollideany(self, self.wall_sprites):
                while sprite.spritecollideany(self, self.wall_sprites):
                    self.rect.y -= 1
            else:
                self.rect.y -= self.step
                self.rl = not self.rl
            self.rect.x += SIZE_OF_RECT - self.step
        elif self.rect.right < 0:
            self.kill()
            self.rl = True
        elif self.rect.x > WIDTH:
            self.kill()
            self.rl = False


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
