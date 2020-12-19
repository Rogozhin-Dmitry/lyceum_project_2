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
        self.cords = [11, -25]
        self.cords_not_round = [self.cords[0] * rect_size, self.cords[1] * rect_size]
        with open("data_file.json", "r") as read_file:
            data = load(read_file)
            self.maps = {}
            for i in data:
                x, y = tuple([int(j) for j in i.split(';')])
                if data[i]['type'] == 'wall':
                    obj = Brick([x, y], (
                        round(self.rect_size * data[i]['size'][0]), round(self.rect_size * data[i]['size'][1])),
                                'tiles\\grass\\' + data[i]['name'])
                else:
                    obj = Brick([x, y], (
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
            self.render()

    def render(self):
        self.empty()
        for i in self.maps:
            if self.cords[0] - 10 <= self.maps[i][0].cords[0] - 15 <= self.cords[0] + 10 and\
                    self.cords[1] - 10 <= self.maps[i][0].cords[1] - 15 <= self.cords[1]:
                if self.maps[i][1] == 'wall':
                    self.maps[i][0].rect.x = self.maps[i][0].cords[0] * self.rect_size - self.cords_not_round[0]
                    self.maps[i][0].rect.y = self.maps[i][0].cords[1] * self.rect_size - self.cords_not_round[1]
                    self.add(self.maps[i][0])
                else:
                    self.decor_sprites.add(self.maps[i][0])
