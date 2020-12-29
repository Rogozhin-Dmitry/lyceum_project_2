from pygame import sprite, image, transform, Rect


class Enemy(sprite.Sprite):  # общий класс всех врагов
    def __init__(self, cords, rect_size):
        super().__init__()
        self.rect_size = rect_size
        self.cords = cords
        self.rect = Rect(0, 0, *rect_size)
        self.type = type
        self.count = 0
        self.timer = 0
        self.last_timer = 0


# Заготовки врагов, чтобы не забыть

class ChesBoy(Enemy):
    def __init__(self, cords, rect_size):
        super().__init__(cords, rect_size)
        self.damage = 1
        self.step = 2
        self.type = 'chesboy'
        self.img_left = transform.scale(image.load('enemies\\chesboy.png').convert(), rect_size)
        self.img_right = transform.flip(self.img_left, True, False)
        self.image = transform.scale(image.load('enemies\\chesboy.png').convert(), rect_size)
        self.image.set_colorkey((255, 255, 255))

    def update(self):
        self.rect.x = self.rect.x + self.step


class Fly(Enemy):
    def __init__(self, cords, rect_size):
        super().__init__(cords, rect_size)
        self.damage = 1
        self.step = 2
        self.type = 'fly'

    def update(self):
        pass
