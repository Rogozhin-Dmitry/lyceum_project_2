from pygame import sprite, image, transform, Rect, display

inf = display.Info()
x, y = inf.current_w // 30, inf.current_h // 17
if x > y:
    SIZE_OF_RECT = int(y)
else:
    SIZE_OF_RECT = int(x)


class Brick(sprite.Sprite):
    def __init__(self, cords, rect_size, image_name, can_be_broken, mask=False, shift=(0, 0)):
        super().__init__()
        self.rect_size = rect_size
        self.cords = cords
        self.player_img = image.load(image_name).convert()
        self.image = transform.scale(self.player_img, rect_size)
        self.image.set_colorkey((255, 255, 255))
        self.rect = Rect(0, 0, *rect_size)
        self.image_name = image_name
        self.shift = shift
        self.can_be_broken = can_be_broken


class SavePoint(sprite.Sprite):
    def __init__(self, cords, rect_size):
        super().__init__()
        self.cords = cords
        self.image = image.load('tiles\\save_point\\1.png').convert()
        self.image = transform.scale(self.image, rect_size)
        self.image.set_colorkey((255, 255, 255))
        self.rect = Rect(0, 0, *rect_size)
        self.rect_size = rect_size
        self.image_name = 'save_point'
        self.player_is_sitting = False
        self.animation = []
        self.animation_with_player = []
        self.can_be_broken = True
        self.count = 0
        self.timer = 0
        self.shift = (0, 0)
        for i in range(4):
            self.animation.append(
                transform.scale(image.load('tiles\\save_point\\' + str(i + 1) + '.png').convert(), rect_size))
        for i in range(4):
            self.animation_with_player.append(
                transform.scale(image.load('tiles\\save_point\\with_player' + str(i + 1) + '.png').convert(),
                                rect_size))

    def update(self):
        self.timer = self.timer + 1
        if self.timer == 10:
            self.count = self.count + 1
            self.timer = 0
        if self.count % 4 == 0:
            self.count = 0
        if not self.player_is_sitting:
            self.image = self.animation[self.count % 4]
        else:
            self.image = self.animation_with_player[self.count % 4]
        self.image.set_colorkey((255, 255, 255))


class Bomb(Brick):  # общий класс всех врагов
    def __init__(self, cords, rect_size, wall_sprites, player):
        super().__init__(cords, rect_size, 'tiles\\bomb\\bomb.png', False)
        self.player = player
        self.wall_sprites = wall_sprites
        self.rl = False
        self.rect.center = cords
        self.count = 1
        self.vx, self.vy = 3, 4
        self.ax, self.ay = 1, 1
        self.timer = 0
        self.last_timer = 0
        self.stay = False
        self.boom = transform.scale(image.load('tiles\\bomb\\boom.png').convert(), (self.player.rect_size,
                                                                                    self.player.rect_size))
        self.boss_bomb = transform.scale(image.load('tiles\\bomb\\boss_bomb.png').convert(),
                                         (round(self.player.rect_size),
                                          round(self.player.rect_size)))
        self.boss_boom = transform.scale(image.load('tiles\\bomb\\boss_boom.png').convert(),
                                         (round(1.5 * self.player.rect_size),
                                          round(1.5 * self.player.rect_size)))
        self.boss_boom.set_colorkey((255, 255, 255))
        self.boss_bomb.set_colorkey((255, 255, 255))
        self.boom.set_colorkey((255, 255, 255))
        self.boss_mode = False

    def change_mode_to_boss(self):
        self.image = self.boss_bomb
        self.boss_mode = True

    def update(self):
        if not self.stay:
            self.move()
        else:
            if self.timer - self.last_timer >= 30:
                self.kill()
                for spr in [*self.wall_sprites, *self.wall_sprites.bonus_sprites, *self.wall_sprites.saves_sprites,
                            *self.wall_sprites.damage_sprites, *self.wall_sprites.enemies_sprites]:
                    if sprite.collide_rect(self, spr) and spr.can_be_broken:
                        del self.wall_sprites.maps[tuple(spr.cords)]
                        spr.kill()

                if sprite.collide_rect(self, self.player):
                    self.player.gui_sprites.set_hearts(self.player.gui_sprites.hp - 1)

        self.timer += 1

    def move(self):
        if self.timer - self.last_timer >= 5:
            self.vy += self.ay
            self.last_timer = self.timer
        if not self.rl and not self.boss_bomb:
            self.rect.x += int(self.vx)
        elif not self.boss_bomb:
            self.rect.x -= int(self.vx)
        self.rect.y += int(self.vy)
        if sprite.spritecollideany(self, self.wall_sprites):
            self.vy = -self.vy // 2
            self.rect.y += int(self.vy)
            self.vx -= self.ax
            if self.vx <= 0.5:
                self.stay = True
                self.last_timer = self.timer

                cords = self.rect.center
                if not self.boss_mode:
                    self.image = self.boom
                else:
                    self.image = self.boss_boom
                self.rect = self.image.get_rect()
                self.rect.center = cords
        if self.rect.bottom <= 0:
            self.kill()
