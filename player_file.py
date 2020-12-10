from pygame import sprite, image, transform, key, time


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
    def __init__(self, cords, sprites, wall_sprites, rect_size):
        super().__init__()
        self.rect_size = rect_size
        self.sprite_group = sprites
        self.wall_sprites = wall_sprites
        self.player_img_left_run = []
        self.player_img_right_run = []
        self.player_img_left = transform.scale(image.load('player\\player.png').convert(),
                                               (rect_size - 2, rect_size * 2 - 5))
        self.player_img_right = transform.flip(self.player_img_left, True, False)
        for i in range(6):
            self.player_img_left_run.append(transform.scale(image.load('player\\' + str(i + 1) + '.png').convert(),
                                                            (rect_size - 2, rect_size * 2 - 5)))
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
