class Render:
    def __init__(self, screen, player_sprites, wall_sprites, decor_sprites):
        self.screen = screen
        self.player_sprites = player_sprites
        self.wall_sprites = wall_sprites
        self.decor_sprites = decor_sprites

    def render_funk(self):
        self.screen.fill((0, 255, 255))
        self.player_sprites.update()
        self.wall_sprites.update()
        self.decor_sprites.update()

        self.wall_sprites.draw(self.screen)
        self.decor_sprites.draw(self.screen)
        self.player_sprites.draw(self.screen)