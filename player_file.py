from pygame import sprite, image, transform, time


class Player(sprite.Sprite):
    def __init__(self, cords, sprites, wall_sprites, keys):
        super().__init__()
        self.cords = cords
        self.sprite_group = sprites
        self.wall_sprites = wall_sprites
        self.keys = keys
        self.player_img = image.load('test_player.png').convert()
        self.image = transform.scale(self.player_img, (45, 121))
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = cords
        self.sprite_group.add(self)
        self.step = 5
        self.jump = False
        self.start_jump_tick = 0
        self.jump_time = 600  # указывать в тиках (60 тиков ~ 1 секунда)

    def update(self):  # метод вызываемы при обновлении (каждый кадр),
        # убью если загрузите какими-либо долгими вычислениями, долгими считаются больше 1/60 секунды
        super().update()
        if self.keys[100]:
            # проверка на стены
            self.rect.x += self.step
            if sprite.spritecollideany(self, self.wall_sprites):
                self.rect.x -= self.step
        if self.keys[97]:
            # проверка на стены
            self.rect.x -= self.step
            if sprite.spritecollideany(self, self.wall_sprites):
                self.rect.x += self.step
        if self.keys[32] and not self.jump:
            self.rect.y += self.step
            if sprite.spritecollideany(self, self.wall_sprites):
                self.jump = True
                self.start_jump_tick = time.get_ticks()
            self.rect.y -= self.step

        if self.jump:
            now = time.get_ticks()
            if now - self.start_jump_tick < self.jump_time:
                self.rect.y -= self.step
                if sprite.spritecollideany(self, self.wall_sprites):
                    self.rect.y += self.step
            else:
                self.jump = False
        else:
            self.rect.y += self.step
            if sprite.spritecollideany(self, self.wall_sprites):
                self.rect.y -= self.step



