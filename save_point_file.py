from pygame import sprite, image, transform, Rect


class SavePoint(sprite.Sprite):
    def __init__(self, cords, rect_size):
        super().__init__()
        self.cords = cords
        self.image = image.load('save_point\\1.png').convert()
        self.image = transform.scale(self.image, 2 * rect_size)
        self.image.set_colorkey((255, 255, 255))
        self.rect = Rect(0, 0, *rect_size)
        self.image_name = 'save_point'
        self.player_is_sitting = False
        self.animation = []
        self.count = 0
        for i in range(3):
            self.animation.append(transform.scale(image.load('save_point\\' + str(i + 1) + '.png').convert(),
                                                  2 * rect_size))

    def update(self):
        pass
