import pygame
from pygame import mixer
pygame.mixer.init()
pygame.mixer.music.load('music&effects/music/menu/Florian Christl - Close Your Eyes.mp3')
klonk_sound = mixer.Sound('music&effects/effects/klonk.wav')
anti_klonk = mixer.Sound('music&effects/effects/miss_sound_cutted.wav')
hopp = mixer.Sound('D:\Pygame Game\music&effects\effects\miss_sound_cutted.wav')

while True:
    hopp.play()
