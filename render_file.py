class Render:
    def __init__(self, screen, player_sprites, wall_sprites):
        self.screen = screen
        self.player_sprites = player_sprites
        self.wall_sprites = wall_sprites

    def render_funk(self):
        self.screen.fill((0, 255, 0))
        self.player_sprites.update()
        self.player_sprites.draw(self.screen)
        self.wall_sprites.draw(self.screen)
