from pygame import sprite, image, transform, Rect


class Brick(sprite.Sprite):
    def __init__(self, cords, rect_size, image_name, mask=False, shift=(0, 0)):
        super().__init__()
        self.rect_size = rect_size
        self.cords = cords
        self.player_img = image.load(image_name).convert()
        self.image = transform.scale(self.player_img, rect_size)
        self.image.set_colorkey((255, 255, 255))
        self.rect = Rect(0, 0, *rect_size)
        self.image_name = image_name
        self.shift = shift
