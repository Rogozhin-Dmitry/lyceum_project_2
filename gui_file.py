from pygame import sprite, transform, image


class Gui(sprite.Group):
    def __init__(self, rect_size):
        super().__init__()
        self.heart_sprites = sprite.Group()
        self.rect_size = rect_size
        self.hp = 5
        self.set_hearts(self.hp)

    def set_hearts(self, num):
        self.heart_sprites.empty()
        for i in range(num):
            spr = sprite.Sprite()
            spr.image = transform.scale(image.load('GUI\\heart.png').convert(), (self.rect_size, self.rect_size))
            spr.image.set_colorkey((255, 255, 255))
            spr.rect = spr.image.get_rect()
            spr.rect.center = (int(self.rect_size * 1.5) * (i + 1), self.rect_size)
            self.heart_sprites.add(spr)
        self.hp = num

    def draw(self, surface):
        super().draw(surface)
        self.heart_sprites.draw(surface)
