import pygame
from player_file import *
from wall_sprites_file import *
from render_file import *

pygame.init()
pygame.mixer.init()

inf = pygame.display.Info()
x, y = inf.current_w // 30, inf.current_h // 17
if x > y:
    SIZE_OF_RECT = int(y)
else:
    SIZE_OF_RECT = int(x)
WIDTH = SIZE_OF_RECT * 30
HEIGHT = SIZE_OF_RECT * 17
FPS = 60
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN | pygame.DOUBLEBUF | pygame.HWSURFACE)
clock = pygame.time.Clock()

decor_sprites = pygame.sprite.Group()
wall_sprites = Wal_sprite((30, 17), SIZE_OF_RECT, decor_sprites, screen)
player_sprites = pygame.sprite.Group()
render = Render(screen, player_sprites, wall_sprites, decor_sprites)

player = Player((SIZE_OF_RECT * 14, SIZE_OF_RECT * 8), player_sprites, wall_sprites, SIZE_OF_RECT)


running = True
while running:
    # Держим цикл на правильной скорости
    clock.tick(FPS)
    # Ввод процесса (события)
    for event in pygame.event.get():
        # проверка для закрытия окна
        if event.type == pygame.QUIT:
            running = False

    render.render_funk()
    # переворот изображения, это чтобы не отрисовывались отдльные части
    pygame.display.flip()

pygame.quit()

