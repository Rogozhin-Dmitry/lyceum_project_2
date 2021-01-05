from brick import *


class Wal_sprite(sprite.Group):
    def __init__(self, rect_size, decor_sprites, bonus_sprites, particle_sprites, dust_particle_sprites,
                 saves_sprites, damage_sprites, enemies_sprites, bomb_sprites, screen):
        super().__init__()
        self.rect_size = rect_size
        self.decor_sprites = decor_sprites
        self.bonus_sprites = bonus_sprites
        self.particle_sprites = particle_sprites
        self.saves_sprites = saves_sprites
        self.dust_particle_sprites = dust_particle_sprites
        self.damage_sprites = damage_sprites
        self.enemies_sprites = enemies_sprites
        self.bomb_sprites = bomb_sprites
        self.screen = screen
        self.cords = [0, 0]
        self.cords_not_round = [self.cords[0] * rect_size, self.cords[1] * rect_size]
        self.maps = {}

    def load(self, maps, cords):
        self.cords = [cords[0] - 14, cords[1] - 7]
        self.cords_not_round = [self.cords[0] * self.rect_size, self.cords[1] * self.rect_size]
        self.maps = maps
        self.render()

    def move(self, param, x_or_y):
        if x_or_y:
            for i in [*self, *self.decor_sprites, *self.bonus_sprites, *self.particle_sprites,
                      *self.dust_particle_sprites, *self.saves_sprites, *self.damage_sprites, *self.enemies_sprites,
                      *self.bomb_sprites]:
                i.rect.y += param
            self.cords_not_round[1] -= param
        else:
            for i in [*self, *self.decor_sprites, *self.bonus_sprites, *self.particle_sprites,
                      *self.dust_particle_sprites, *self.saves_sprites, *self.damage_sprites, *self.enemies_sprites,
                      *self.bomb_sprites]:
                i.rect.x += param
            self.cords_not_round[0] -= param

        if self.cords != [i // self.rect_size for i in self.cords_not_round]:
            self.cords = [i // self.rect_size for i in self.cords_not_round]
            self.render()

    def render(self):
        self.empty()
        self.decor_sprites.empty()
        self.bonus_sprites.empty()
        self.saves_sprites.empty()
        self.damage_sprites.empty()
        self.enemies_sprites.empty()
        for i in self.maps:
            if (self.cords[0] - 15 <= self.maps[i][0].cords[0] or self.maps[i][0].delay[0] <= self.cords[0] + 17) and \
                    (self.cords[1] - 15 <= self.maps[i][0].cords[1] or self.maps[i][0].delay[1] <= self.cords[1] + 5):
                self.maps[i][0].rect.x = self.maps[i][0].cords[0] * self.rect_size - self.cords_not_round[0] \
                                         + self.maps[i][0].shift[0] * self.rect_size
                self.maps[i][0].rect.y = self.maps[i][0].cords[1] * self.rect_size - self.cords_not_round[1] + \
                                         self.maps[i][0].shift[1] * self.rect_size
                if self.maps[i][1] == 'wall':
                    self.add(self.maps[i][0])
                elif self.maps[i][1] == 'decor':
                    self.decor_sprites.add(self.maps[i][0])
                elif self.maps[i][1] == 'bonus':
                    self.bonus_sprites.add(self.maps[i][0])
                elif self.maps[i][1] == 'save':
                    self.saves_sprites.add(self.maps[i][0])
                elif self.maps[i][1] == 'damage':
                    self.damage_sprites.add(self.maps[i][0])
                elif self.maps[i][1] == 'enemy':
                    self.enemies_sprites.add(self.maps[i][0])
