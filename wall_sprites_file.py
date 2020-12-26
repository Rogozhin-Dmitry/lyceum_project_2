from brick import *


class Wal_sprite(sprite.Group):
    def __init__(self, rect_size, decor_sprites, bonus_sprites, particle_sprites, dust_particle_sprites, screen):
        super().__init__()
        self.rect_size = rect_size
        self.decor_sprites = decor_sprites
        self.bonus_sprites = bonus_sprites
        self.particle_sprites = particle_sprites
        self.dust_particle_sprites = dust_particle_sprites
        self.screen = screen
        self.cords = [0, 0]
        self.cords_not_round = [self.cords[0] * rect_size, self.cords[1] * rect_size]
        self.maps = {}
        self.render()

    def load(self, maps):
        self.cords = [11, -25]
        self.cords_not_round = [self.cords[0] * self.rect_size, self.cords[1] * self.rect_size]
        self.maps = maps

    def move(self, param, x_or_y):
        if x_or_y:
            for i in [*self, *self.decor_sprites, *self.bonus_sprites, *self.particle_sprites,
                      *self.dust_particle_sprites]:
                i.rect.y += param
            self.cords_not_round[1] -= param
        else:
            for i in [*self, *self.decor_sprites, *self.bonus_sprites, *self.particle_sprites,
                      *self.dust_particle_sprites]:
                i.rect.x += param
            self.cords_not_round[0] -= param

        if self.cords != [i // self.rect_size for i in self.cords_not_round]:
            self.cords = [i // self.rect_size for i in self.cords_not_round]
            self.render()

    def render(self):
        self.empty()
        self.decor_sprites.empty()
        self.bonus_sprites.empty()
        for i in self.maps:
            if self.cords[0] - 15 <= self.maps[i][0].cords[0] - 15 <= self.cords[0] + 16 and\
                    self.cords[1] - 15 <= self.maps[i][0].cords[1] - 15 <= self.cords[1] + 5:
                self.maps[i][0].rect.x = self.maps[i][0].cords[0] * self.rect_size - self.cords_not_round[0]
                self.maps[i][0].rect.y = self.maps[i][0].cords[1] * self.rect_size - self.cords_not_round[1]
                if self.maps[i][1] == 'wall':
                    self.add(self.maps[i][0])
                elif self.maps[i][1] == 'decor':
                    self.decor_sprites.add(self.maps[i][0])
                elif self.maps[i][1] == 'bonus':
                    self.bonus_sprites.add(self.maps[i][0])
