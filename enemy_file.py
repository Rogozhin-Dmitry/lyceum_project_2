from pygame import sprite, image, transform, Rect


class Enemy(sprite.Sprite):  # общий класс всех врагов
    def __init__(self, cords, rect_size, damage, type):
        super().__init__()
        self.rect_size = rect_size
        self.cords = cords
        self.rect = Rect(0, 0, *rect_size)
        self.damage = damage
        self.type = type

    def deal_damage(self):
        if sprite.spritecollideany(self, self.player_sprites):
            self.player_sprites.gui_sprites.set_heart(self.player_sprites.hp - 1)


# Заготовки врагов, чтобы не забыть

class Chesnut(sprite.Sprite,
              Enemy):
    def __init__(self, cords, rect_size, damage, type):
        super().__init__()

    # будущий класс для врага каштанчика, ходит пока не встретит препятствие (пропасть или стену), при встрече поворачивает обратно
    def update(self):
        def __init__(self, cords, rect_size, damage, type):
            super().__init__()

    pass


class Fly(sprite.Sprite,
          Enemy):  # тоже самое что каштанчик, но в воздухе. Пропасть препятствием не считает, но имеет ограничение по дальности - 10 блоков
    pass
