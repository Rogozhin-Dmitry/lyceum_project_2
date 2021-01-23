from brick import *
from pygame import Surface, draw, display, event

inf = display.Info()
x, y = inf.current_w / 30, inf.current_h / 17
if x > y:
    SIZE_OF_RECT = int(y)
else:
    SIZE_OF_RECT = int(x)
WIDTH = inf.current_w
HEIGHT = inf.current_h


def down_collision(obj_1, obj_2):
    return (obj_2.rect.x < obj_1.rect.x < obj_2.rect.x + obj_2.rect.w or obj_2.rect.x
            < obj_1.rect.x + obj_1.rect.w < obj_2.rect.x + obj_2.rect.w or obj_2.rect.x == obj_1.rect.x
            or obj_2.rect.x + obj_2.rect.w == obj_1.rect.x + obj_1.rect.w) and \
           (obj_2.rect.y < obj_1.rect.y + obj_1.rect.h < obj_2.rect.y + obj_2.rect.w)


class Enemy(Brick):  # общий класс всех врагов
    def __init__(self, cords, rect_size, image_name, wall_sprites, damage_sprites, can_be_broken, shift=(0, 0)):
        super().__init__(cords, rect_size, image_name, can_be_broken, shift=shift)
        self.wall_sprites = wall_sprites
        self.damage_sprites = damage_sprites
        self.cords = cords
        self.is_target = False
        self.can_target = False
        self.is_boss = False
        self.cords_not_round = [self.cords[0] * SIZE_OF_RECT, self.cords[1] * SIZE_OF_RECT]
        self.delay = (0, 0)


class Boss(Enemy):
    def __init__(self, cords, rect_size, image_name, wall_sprites, damage_sprites, can_be_broken, player, bomb_sprites,
                 shift=(0, 0)):
        super().__init__(cords, rect_size, image_name, wall_sprites, damage_sprites, can_be_broken, shift=shift)
        self.step = 5
        self.is_boss = True
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
        self.hp = 5
        self.can_be_broken = False
        self.invulnerable = False
        self.clear_img = Surface(rect_size)
        draw.rect(self.clear_img, (255, 255, 255), (0, 0, rect_size[0], rect_size[1]))
        self.clear_img.set_colorkey((255, 255, 255))
        self.invulnerable_count = 0
        self.true_image = self.image
        self.animation = [self.image]
        for i in range(2):
            new_animation = image.load('tiles\\enemy\\boss_animation\\' + str(i + 1) + '.png').convert()
            self.animation.append(transform.scale(new_animation, rect_size))
        new_animation = image.load('tiles\\enemy\\boss_animation\\1.png').convert()
        self.animation.append(transform.scale(new_animation, rect_size))
        self.animation.append(self.image)

    def update(self):
        super().update()
        self.image = self.animation[(self.count // 10) % 5]
        self.image.set_colorkey((255, 255, 255))
        if self.invulnerable:
            self.invulnerable_count = self.invulnerable_count + 1
            if 15 < self.invulnerable_count <= 30 or 45 < self.invulnerable_count <= 60 \
                    or 75 < self.invulnerable_count <= 90 or \
                    105 < self.invulnerable_count < 120:
                self.image = self.clear_img
            elif self.invulnerable_count == 120:
                self.invulnerable = False
                self.image = self.true_image
                self.invulnerable_count = 0
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
                elif self.all_way_straight > 2000:
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
                elif self.all_way_straight < -2000:
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
        self.bomb_sprites.add(Boss_Bomb(self.rect.center, (self.rect_size[0] // 2, self.rect_size[1] // 2),
                                        self.wall_sprites, self.player))

    def get_damage(self):
        if not self.invulnerable:
            event.post(event.Event(50, {}))
            self.hp = self.hp - 1
            self.invulnerable = True
        else:
            event.post(event.Event(51, {}))


class Crash(Enemy):
    def __init__(self, cords, rect_size, image_name, wall_sprites, damage_sprites, can_be_broken,
                 shift=(0, 0)):
        super().__init__(cords, rect_size, image_name, wall_sprites, damage_sprites, can_be_broken, shift=shift)
        self.step = 5
        self.step_1 = self.step / SIZE_OF_RECT
        self.rl = True
        self.count = 0
        self.image_run = [self.image]
        for i in range(19):
            self.image_run.append(transform.scale(
                image.load('tiles\\enemy\\crash_animation\\' + str(i + 1) + '.png').convert(), rect_size))
        self.last_timer = 0
        self.timer = 0

    def update(self):
        super().update()
        if self.is_target:
            self.target()
        else:
            self.standard()
            if self.timer - self.last_timer >= 2:
                self.image = self.image_run[self.count % 20]
                self.image.set_colorkey((255, 255, 255))
                self.count += 1
                self.last_timer = self.timer
        if self.rect.right >= 0 and self.rect.x <= WIDTH:
            if not self.rl:
                self.rect.x -= SIZE_OF_RECT - self.step * 2
            else:
                self.rect.x += SIZE_OF_RECT - self.step * 2
            rl = self.rl
            self.rect.y += self.step
            if sprite.spritecollideany(self, self.wall_sprites, collided=down_collision):
                while sprite.spritecollideany(self, self.wall_sprites, collided=down_collision):
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
        self.timer += 1

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
    def __init__(self, cords, rect_size, image_name, wall_sprites, damage_sprites, can_be_broken,
                 shift=(0, 0)):
        super().__init__(cords, rect_size, image_name, wall_sprites, damage_sprites, can_be_broken,
                         shift=shift)
        self.step = 5
        self.step_1 = self.step / SIZE_OF_RECT
        self.rl = True
        self.count = 0
        self.all_way_straight = 0
        self.image_run = [self.image]
        for i in range(4):
            self.image_run.append(transform.scale(
                image.load('tiles\\enemy\\fly_animation\\' + str(i + 1) + '.png').convert(), rect_size))
        self.last_timer = 0
        self.timer = 0

    def update(self):
        super().update()
        if self.is_target:
            self.target()
        else:
            self.standard()
            if self.timer - self.last_timer >= 20:
                self.image = self.image_run[self.count % 5]
                self.image.set_colorkey((255, 255, 255))
                self.count += 1
                self.last_timer = self.timer
        if self.rect.right < 0:
            self.kill()
            self.rl = True
        elif self.rect.x > WIDTH:
            self.kill()
            self.rl = False
        self.timer += 1

    def target(self):
        pass

    def standard(self):
        if self.rl:
            self.rect.x += self.step
            self.all_way_straight = self.all_way_straight + self.step
            if sprite.spritecollideany(self, self.wall_sprites):
                while sprite.spritecollideany(self, self.wall_sprites):
                    self.rect.x -= 1
                self.rl = False
            elif sprite.spritecollideany(self, self.damage_sprites):
                while sprite.spritecollideany(self, self.damage_sprites):
                    self.rect.x -= 1
                self.rl = False
            elif self.all_way_straight > 750:
                self.rl = False
            else:
                self.cords_not_round[0] += 1
                self.shift[0] += self.step_1
                self.delay[0] += self.step_1
        else:
            self.rect.x -= self.step
            self.all_way_straight = self.all_way_straight - self.step
            if sprite.spritecollideany(self, self.wall_sprites):
                while sprite.spritecollideany(self, self.wall_sprites):
                    self.rect.x += 1
                self.rl = True
            elif sprite.spritecollideany(self, self.damage_sprites):
                while sprite.spritecollideany(self, self.damage_sprites):
                    self.rect.x += 1
                self.rl = True
            elif self.all_way_straight < -750:
                self.rl = True
            else:
                self.cords_not_round[0] -= 1
                self.shift[0] -= self.step_1
                self.delay[0] -= self.step_1
