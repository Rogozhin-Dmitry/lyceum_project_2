from pygame import font, display, transform, image
inf = display.Info()
x, y = inf.current_w // 30, inf.current_h // 17
if x > y:
    SIZE_OF_RECT = int(y)
else:
    SIZE_OF_RECT = int(x)
WIDTH = SIZE_OF_RECT * 30
HEIGHT = SIZE_OF_RECT * 17


class Render:
    def __init__(self, screen, player_sprites, wall_sprites, decor_sprites, bonus_sprites, gui_sprites,
                 dust_particle_sprites, particle_sprites, saves_sprites, damage_sprites, enemies_sprites, bomb_sprites):
        self.screen = screen
        self.player_sprites = player_sprites
        self.wall_sprites = wall_sprites
        self.decor_sprites = decor_sprites
        self.gui_sprites = gui_sprites
        self.bonus_sprites = bonus_sprites
        self.particle_sprites = particle_sprites
        self.dust_particle_sprites = dust_particle_sprites
        self.saves_sprites = saves_sprites
        self.damage_sprites = damage_sprites
        self.enemies_sprites = enemies_sprites
        self.bomb_sprites = bomb_sprites
        font_sh = font.Font('fonts\\f1.ttf', 150)
        self.game_over_text = font_sh.render('Game Over', True, (25, 25, 25))
        self.game_over_text_rect = self.game_over_text.get_rect(centerx=WIDTH // 2, centery=HEIGHT // 2)
        font_sh = font.Font('fonts\\f1.ttf', 50)
        self.game_over_text_1 = font_sh.render('Нажмите любую кнопку, чтобы выйти', True, (25, 25, 25))
        self.game_over_text_rect_1 = self.game_over_text.get_rect(centerx=WIDTH // 2, centery=HEIGHT - SIZE_OF_RECT)
        self.render_timer_2 = 0
        self.last_render_timer_2 = 0
        self.game_bg_image = transform.scale(image.load('fons\\bg_with_lights.jpg').convert(), (WIDTH, HEIGHT))

    def render_funk(self):
        #self.screen.blit(self.game_bg_image, (0, 0))
        self.screen.fill((0, 255, 255))
        self.player_sprites.update()
        self.wall_sprites.update()
        self.decor_sprites.update()
        self.saves_sprites.update()
        self.damage_sprites.update()
        self.enemies_sprites.update()
        self.bomb_sprites.update()
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
        self.saves_sprites.draw(self.screen)
        self.bonus_sprites.draw(self.screen)
        self.decor_sprites.draw(self.screen)
        self.dust_particle_sprites.draw(self.screen)
        self.damage_sprites.draw(self.screen)
        self.bomb_sprites.draw(self.screen)
        self.enemies_sprites.draw(self.screen)
        self.player_sprites.draw(self.screen)
        self.particle_sprites.draw(self.screen)
        self.gui_sprites.draw(self.screen)

    def freeze_render_funk(self):
        self.screen.fill((0, 255, 255))
        self.wall_sprites.update()
        self.decor_sprites.update()
        self.saves_sprites.update()
        self.damage_sprites.update()
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
        self.saves_sprites.draw(self.screen)
        self.bonus_sprites.draw(self.screen)
        self.decor_sprites.draw(self.screen)
        self.dust_particle_sprites.draw(self.screen)
        self.damage_sprites.draw(self.screen)
        self.enemies_sprites.draw(self.screen)
        self.particle_sprites.draw(self.screen)
        self.gui_sprites.draw(self.screen)

    def game_over_render_funk(self):
        self.screen.fill((0, 255, 255))
        self.wall_sprites.update()
        self.decor_sprites.update()
        self.saves_sprites.update()
        self.damage_sprites.update()
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
        self.saves_sprites.draw(self.screen)
        self.bonus_sprites.draw(self.screen)
        self.decor_sprites.draw(self.screen)
        self.dust_particle_sprites.draw(self.screen)
        self.damage_sprites.draw(self.screen)
        self.enemies_sprites.draw(self.screen)
        self.particle_sprites.draw(self.screen)
        self.gui_sprites.draw(self.screen)
        self.screen.blit(self.game_over_text, self.game_over_text_rect)
        if self.render_timer_2 - self.last_render_timer_2 <= 25:
            self.screen.blit(self.game_over_text_1, self.game_over_text_rect_1)
        elif self.render_timer_2 - self.last_render_timer_2 >= 50:
            self.last_render_timer_2 = self.render_timer_2

        self.render_timer_2 += 1

    def boss_fight_render_funk(self):
        pass
