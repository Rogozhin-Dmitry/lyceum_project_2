class Render:
    def __init__(self, screen, player_sprites, wall_sprites, decor_sprites, bonus_sprites, gui_sprites,
                 dust_particle_sprites, particle_sprites):
        self.screen = screen
        self.player_sprites = player_sprites
        self.wall_sprites = wall_sprites
        self.decor_sprites = decor_sprites
        self.gui_sprites = gui_sprites
        self.bonus_sprites = bonus_sprites
        self.particle_sprites = particle_sprites
        self.dust_particle_sprites = dust_particle_sprites

    def render_funk(self):
        self.screen.fill((0, 255, 255))
        self.player_sprites.update()
        self.wall_sprites.update()
        self.decor_sprites.update()
        for i in [*self.particle_sprites, *self.dust_particle_sprites]:
            i.x += i.shift
            i.y += i.shift_down
            i.shift_down += i.shift_up
            i.rect.x = i.x
            i.rect.y = i.y
            if i.down < i.rect.y + i.rect.h:
                i.kill()
                del i

        self.wall_sprites.draw(self.screen)
        self.bonus_sprites.draw(self.screen)
        self.decor_sprites.draw(self.screen)
        self.dust_particle_sprites.draw(self.screen)
        self.player_sprites.draw(self.screen)
        self.particle_sprites.draw(self.screen)
        self.gui_sprites.draw(self.screen)
