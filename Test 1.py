import pygame

pygame.init()
screen = pygame.display.set_mode(size=(960, 540))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()