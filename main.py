import pygame
from event_check_file import *
from render_file import *
from player_file import *
from wall_file import *

WIDTH = 360
HEIGHT = 480
FPS = 30


pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT), flags=pygame.RESIZABLE | pygame.HWSURFACE)
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()

run = [True]
keys = {100: False, 97: False, 32: False}
player_sprites = pygame.sprite.Group()
wall_sprites = pygame.sprite.Group()
render = Render(screen, player_sprites, wall_sprites)


check = Check(run, keys)
player = Player((0, 0), player_sprites, wall_sprites, keys)
Wall((0, 450), wall_sprites)
Wall((125, 425), wall_sprites)


while run[0]:
    # настройка фпс и сюда же музыка
    clock.tick(FPS)

    # проверка событий, возможно засунуть во второй поток
    check.check_funk(pygame.event.get())

    # рендер всего и вся
    render.render_funk()

    # переворот изображения это чтобы не отрисовывались отдльные части
    pygame.display.flip()

pygame.quit()

