from pygame import sprite, image, transform


class Wall(sprite.Sprite):
    def __init__(self, cords, sprites):
        super().__init__()
        self.cords = cords
        self.sprite_group = sprites
        self.player_img = image.load('test_player.png').convert()
        self.image = transform.scale(self.player_img, (125, 25))
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = cords
        self.sprite_group.add(self)
