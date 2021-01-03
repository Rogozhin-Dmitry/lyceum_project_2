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
    def __init__(self, cords, rect_size, image_name, wall_sprites, damage_sprites, can_be_broken,
                 mask=False,
                 shift=(0, 0)):
        super().__init__(cords, rect_size, image_name, can_be_broken, mask=mask, shift=shift)
        self.wall_sprites = wall_sprites
        self.damage_sprites = damage_sprites
        self.cords = cords
        self.is_target = False
        self.can_target = False
        self.cords_not_round = [self.cords[0] * SIZE_OF_RECT, self.cords[1] * SIZE_OF_RECT]
        self.delay = (0, 0)


class Boss(Enemy):
    def __init__(self, cords, rect_size, image_name, wall_sprites, damage_sprites, can_be_broken, player, bomb_sprites,
                 mask=False,
                 shift=(0, 0)):
        super().__init__(cords, rect_size, image_name, wall_sprites, damage_sprites, can_be_broken, mask=mask,
                         shift=shift)
        self.step = 5
        self.step_1 = self.step / SIZE_OF_RECT
        self.rl = True
        self.down = True
        self.count = 0
        self.is_lifting = False
        self.all_way_down = 0
        self.player = player
        self.bomb_sprites = bomb_sprites
        self.all_way_straight = 0
        self.is_standing = False
        self.life = 10
        self.can_be_broken = False

    def update(self):
        super().update()
        if self.is_standing:
            self.count = self.count + 1
            if self.count == 100:
                self.is_standing = False
        elif not self.is_lifting:
            self.count = self.count + 1
            if self.count == 300:
                self.count = 0
                self.is_lifting = True
            if self.count % 60 == 0 and self.count != 0:
                self.throw_bomb()
            if self.rl:
                self.rect.x = self.rect.x + self.step
                self.all_way_straight = self.all_way_straight + self.step
                if sprite.spritecollideany(self, self.wall_sprites):
                    while sprite.spritecollideany(self, self.wall_sprites):
                        self.rect.x = self.rect.x - 1
                    self.rl = False
                elif sprite.spritecollideany(self, self.damage_sprites):
                    while sprite.spritecollideany(self, self.damage_sprites):
                        self.rect.x = self.rect.x - 1
                    self.rl = False
                elif self.all_way_straight > 750:
                    self.rl = False
                else:
                    self.cords_not_round[0] += 1
                    self.shift[0] += self.step_1
                    self.delay[0] += self.step_1
            else:
                self.rect.x = self.rect.x - self.step
                self.all_way_straight = self.all_way_straight - self.step
                if sprite.spritecollideany(self, self.wall_sprites):
                    while sprite.spritecollideany(self, self.wall_sprites):
                        self.rect.x = self.rect.x + 1
                    self.rl = True
                    self.all_way_straight = 0
                elif sprite.spritecollideany(self, self.damage_sprites):
                    while sprite.spritecollideany(self, self.damage_sprites):
                        self.rect.x = self.rect.x + 1
                    self.rl = True
                    self.all_way_straight = 0
                elif self.all_way_straight < -750:
                    self.rl = True
                else:
                    self.cords_not_round[0] -= 1
                    self.shift[0] -= self.step_1
                    self.delay[0] -= self.step_1
        else:
            if self.down:
                self.rect.y = self.rect.y + self.step
                self.all_way_down = self.all_way_down + self.step
                if sprite.spritecollideany(self, self.wall_sprites):
                    while sprite.spritecollideany(self, self.wall_sprites):
                        self.rect.y = self.rect.y - 1
                        self.all_way_down = self.all_way_down - 1
                    self.down = False
                    self.is_standing = True
                elif sprite.spritecollideany(self, self.damage_sprites):
                    while sprite.spritecollideany(self, self.damage_sprites):
                        self.rect.y = self.rect.y - 1
                        self.all_way_down = self.all_way_down - 1
                    self.down = False
                    self.is_standing = True
                else:
                    self.cords_not_round[1] += 1
                    self.shift[1] += self.step_1
                    self.delay[1] += self.step_1
            else:
                self.rect.y = self.rect.y - self.step
                self.all_way_down = self.all_way_down - self.step
                if sprite.spritecollideany(self, self.wall_sprites):
                    while sprite.spritecollideany(self, self.wall_sprites):
                        self.rect.y = self.rect.y + 1
                    self.down = True
                    self.is_lifting = False
                    self.all_way_down = 0
                elif sprite.spritecollideany(self, self.damage_sprites):
                    while sprite.spritecollideany(self, self.damage_sprites):
                        self.rect.y = self.rect.y + 1
                    self.down = True
                    self.is_lifting = False
                    self.all_way_down = 0
                elif self.all_way_down <= 0:
                    self.all_way_down = 0
                    self.down = True
                    self.is_lifting = False
                else:
                    self.cords_not_round[1] -= 1
                    self.shift[1] -= self.step_1
                    self.delay[1] -= self.step_1

    def throw_bomb(self):
        bomb = Bomb(self.rect.center, (self.rect_size[0] // 2, self.rect_size[1] // 2), self.wall_sprites, self.player)
        bomb.change_mode_to_boss()
        self.bomb_sprites.add(bomb)


class Crash(Enemy):

    def __init__(self, cords, rect_size, image_name, wall_sprites, damage_sprites, can_be_broken, mask=False,
                 shift=(0, 0)):
        super().__init__(cords, rect_size, image_name, wall_sprites, damage_sprites, can_be_broken, mask=mask,
                         shift=shift)
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
        if self.rect.right >= 0 and self.rect.x <= WIDTH:
            if not self.rl:
                self.rect.x -= SIZE_OF_RECT - self.step * 2
            else:
                self.rect.x += SIZE_OF_RECT - self.step * 2
            rl = self.rl
            self.rect.y += self.step
            if sprite.spritecollideany(self, self.wall_sprites):
                while sprite.spritecollideany(self, self.wall_sprites):
                    self.rect.y -= 1
            else:
                self.rect.y -= self.step
                self.rl = not self.rl
            if not rl:
                self.rect.x += SIZE_OF_RECT - self.step * 2
            else:
                self.rect.x -= SIZE_OF_RECT - self.step * 2
        elif self.rect.right < 0:
            self.kill()
            self.rl = True
        elif self.rect.x > WIDTH:
            self.kill()
            self.rl = False

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


class Fly(Enemy):
    def __init__(self, cords, rect_size, image_name, wall_sprites, damage_sprites, can_be_broken, mask=False,
                 shift=(0, 0)):
        super().__init__(cords, rect_size, image_name, wall_sprites, damage_sprites, can_be_broken, mask=mask,
                         shift=shift)
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
        if self.rect.right < 0:
            self.kill()
            self.rl = True
        elif self.rect.x > WIDTH:
            self.kill()
            self.rl = False

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
