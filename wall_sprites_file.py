from brick import *
from json import load


class Wal_sprite(sprite.Group):
    def __init__(self, size, rect_size, decor_sprites, screen):
        super().__init__()
        self.loaded_walls = [[0] * (size[0] + 2) for _ in range(size[1] + 2)]
        self.size = size
        self.rect_size = rect_size
        self.decor_sprites = decor_sprites
        self.screen = screen
        self.cords_not_round = [13 * rect_size, 13 * rect_size]
        self.cords = [13, 13]
        with open("data_file.json", "r") as read_file:
            data = load(read_file)
            self.maps = {}
            for i in data:
                x, y = tuple([int(j) for j in i.split(';')])
                if data[i]['type'] == 'wall':
                    obj = Brick([x * self.rect_size, y * self.rect_size], (
                        round(self.rect_size * data[i]['size'][0]), round(self.rect_size * data[i]['size'][1])),
                                'tiles\\grass\\' + data[i]['name'])
                else:
                    obj = Brick([x * self.rect_size, y * self.rect_size], (
                        round(self.rect_size * data[i]['size'][0]), round(self.rect_size * data[i]['size'][1])),
                                'tiles\\decor\\' + data[i]['name'])
                self.maps[tuple([int(j) for j in i.split(';')])] = (obj, data[i]['type'])
        self.render()

    def move(self, param, x_or_y):
        if x_or_y:
            for i in [*self, *self.decor_sprites]:
                i.rect.y += param
            self.cords_not_round[1] -= param
        else:
            for i in [*self, *self.decor_sprites]:
                i.rect.x += param
            self.cords_not_round[0] -= param

        if self.cords != [i // self.rect_size for i in self.cords_not_round]:
            self.cords = [i // self.rect_size for i in self.cords_not_round]
            print(self.cords)

    def render(self):
        for i in self.maps:
            # if self.cords[0] - 5 <= i[0] <= self.cords[0] + 5 and self.cords[1] - 25 <= i[1] <= self.cords[1] + 25:
            if self.maps[i][1] == 'wall':
                self.add(self.maps[i][0])
            else:
                self.decor_sprites.add(self.maps[i][0])
