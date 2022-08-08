import pygame

pygame.init()

# Colors
class Color:
    white = (255, 255, 255)
    red = (255, 0, 0)
    green = (0, 255, 0)
    blue = (0, 0, 255)
    black = (0, 0, 0)

# SFX & Music
class Sounds:
    PopSound = pygame.mixer.Sound('F:\Development Folder\Python\PyGame\pygame-test-games\Pop.wav')
#Sounds.PopSound.play()

class Music:
    MainTheme = pygame.mixer.music.load('F:\Development Folder\Python\PyGame\pygame-test-games\Pop.wav')
#pygame.mixer.music.play()

# Game Screen
scr_width = 960
scr_height = 540
screen = pygame.display.set_mode(size=(scr_width, scr_height))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    pygame.draw.rect(surface=screen, color=Color.red, rect=(scr_width/2-50, scr_height/2-50, 100, 100))

    pygame.draw.polygon(surface=screen, color=Color.white, points=[[0, scr_height], [scr_width/2-50, scr_height * 0.6], [scr_width/2+50, scr_height * 0.6], [scr_width, scr_height]])
    pygame.draw.polygon(surface=screen, color=Color.white, points=[[0, 0], [scr_width/2-50, scr_height * 0.4], [scr_width/2+50, scr_height * 0.4], [scr_width, 0]])

    pygame.display.update()