import pygame
from event_check_file import *
from render_file import *

WIDTH = 360
HEIGHT = 480
FPS = 30


pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT), flags=pygame.RESIZABLE | pygame.HWSURFACE)
render = render(screen)
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()

while True:
    # настройка фпс и сюда же музыка
    clock.tick(FPS)

    # проверка событий, возможно засунуть во второй поток
    if check_funk(pygame.event.get()):
        break

    render.render_funk()

    # переворот изображения это чтобы не отрисовывались отдльные части
    pygame.display.flip()

pygame.quit()

