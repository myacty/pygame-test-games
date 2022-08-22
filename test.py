import pygame

import COLORS as Color

pygame.init()
scr_width = 960
scr_height = 540
screen = pygame.display.set_mode(size=(scr_width, scr_height))

clock = pygame.time.Clock()
framerate = 25 # FPS

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.draw.circle(screen, Color.red, (scr_width/2, scr_height/2), 64)
    pygame.draw.circle(screen, Color.white, (scr_width/2, scr_height/2), 58)

    pygame.display.update()
    pygame.time.Clock().tick(framerate)