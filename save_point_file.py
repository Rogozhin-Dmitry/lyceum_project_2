from pygame import sprite, image, transform, Rect


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
        self.count = 0
        self.timer = 0
        self.shift = (0, 0)
        for i in range(4):
            self.animation.append(
                transform.scale(image.load('tiles\\save_point\\' + str(i + 1) + '.png').convert(), rect_size))
        for i in range(4):
            self.animation_with_player.append(
                transform.scale(image.load('tiles\\save_point\\with_player' + str(i + 1) + '.png').convert(), rect_size))

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
