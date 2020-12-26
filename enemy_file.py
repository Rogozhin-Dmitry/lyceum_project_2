from pygame import sprite, image, transform, Rect


class Enemy(sprite.Sprite):  # общий класс всех врагов
    def __init__(self, cords, rect_size, damage, player_sprites):
        super().__init__()
        self.rect_size = rect_size
        self.cords = cords
        self.rect = Rect(0, 0, *rect_size)
        self.damage = damage
        self.player_sprites = player_sprites

    def deal_damage(self):
        if sprite.spritecollideany(self, self.player_sprites):
            self.player_sprites.gui_sprites.set_heart(self.player_sprites.hp - 1)


class Spike(sprite.Sprite, Enemy):  # класс шипа
    def __init__(self, cords, rect_size, damage, player_sprites):
        super().__init__(cords, rect_size, damage, player_sprites)
        self.player_img = image.load('spike.png').convert()
        self.image = transform.scale(self.player_img, rect_size)
        self.image.set_colorkey((255, 255, 255))
        self.image_name = 'spike.png'


class Chesnut(sprite.Sprite, Enemy):  # будущий класс для врага каштанчика
    pass
