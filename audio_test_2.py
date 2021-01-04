import pygame as pg
import sys

pg.init()
sc = pg.display.set_mode((400, 300))

pygame.mixer.music.load('music&effects/music/menu/Florian Christl - Close Your Eyes.mp3')
pygame.mixer.music.play()

sound1 = pg.mixer.Sound('music&effects/music/boss_fight/NGAHHH!! (from Undertale).mp3')
sound2 = pg.mixer.Sound('music&effects/effects/klonk.mp3')

while 1:
    for i in pg.event.get():
        if i.type == pg.QUIT:
            sys.exit()

        elif i.type == pg.KEYDOWN:
            if i.key == pg.K_1:
                pg.mixer.music.pause()
                # pygame.mixer.music.stop()
            elif i.key == pg.K_2:
                pg.mixer.music.unpause()
                # pygame.mixer.music.play()
                pg.mixer.music.set_volume(0.5)
            elif i.key == pg.K_3:
                pg.mixer.music.unpause()
                # pygame.mixer.music.play()
                pg.mixer.music.set_volume(1)

        elif i.type == pg.MOUSEBUTTONUP:
            if i.button == 1:
                sound1.play()
            elif i.button == 3:
                sound2.play()

    pg.time.delay(20)