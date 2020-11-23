import pygame


def check_funk(events):
    running = False
    for i in events:
        print(i)
        if i.type == pygame.QUIT:
            running = True

    return running
