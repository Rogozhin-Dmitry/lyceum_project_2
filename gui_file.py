from pygame import sprite, transform, image, font, event


class Gui(sprite.Group):
    def __init__(self, rect_size):
        super().__init__()
        self.heart_sprites = sprite.Group()
        self.bomb_sprites = sprite.Group()
        self.rect_size = rect_size
        self.hp = 5
        self.bomb = 5
        self.font = font.Font('fonts\\f1.ttf', self.rect_size)
        self.heart = transform.scale(image.load('GUI\\heart.png').convert(), (self.rect_size, self.rect_size))
        self.heart_pass = transform.scale(image.load('GUI\\heart_pass.png').convert(), (self.rect_size, self.rect_size))
        self.max_hp = 10
        self.max_bomb = 50

        self.set_hearts(self.hp)
        self.set_bombs(self.bomb)

    def set_hearts(self, num):
        if 0 < num <= self.max_hp:
            self.hp = num
            self.heart_sprites.empty()
            for i in range(self.max_hp):
                spr = sprite.Sprite()
                if i < self.hp:
                    spr.image = self.heart
                else:
                    spr.image = self.heart_pass
                spr.image.set_colorkey((255, 255, 255))
                spr.rect = spr.image.get_rect()
                spr.rect.center = (int(self.rect_size * 1.5) * (i + 1), self.rect_size)
                self.heart_sprites.add(spr)
        elif num <= 0:
            event.post(event.Event(31, {}))

    def set_bombs(self, num):
        if 0 <= num <= self.max_bomb:
            self.bomb = num
            self.bomb_sprites.empty()
            spr = sprite.Sprite()
            spr.image = transform.scale(image.load('GUI\\carrot_bomb.png').convert(), (self.rect_size, self.rect_size))
            spr.image.set_colorkey((255, 255, 255))
            spr.rect = spr.image.get_rect()
            spr.rect.center = (int(self.rect_size * 1.5), self.rect_size * 2.5)
            self.bomb_sprites.add(spr)
            spr = sprite.Sprite()
            spr.image = self.font.render(str(self.bomb), True, (0, 0, 0))
            spr.image.set_colorkey((255, 255, 255))
            spr.rect = spr.image.get_rect()
            spr.rect.center = (int(self.rect_size * 1.5) * 2, self.rect_size * 2.5)
            self.bomb_sprites.add(spr)

    def draw(self, surface):
        super().draw(surface)
        self.heart_sprites.draw(surface)
        self.bomb_sprites.draw(surface)
