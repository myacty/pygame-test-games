from abc import ABC, abstractmethod
from enum import Enum
import pygame

import COLORS as Color
from GUI import Anchor
from GUI import GUILabel
from GUI import GUICanvas

pygame.init()

# Game Screen
scr_width = 960
scr_height = 540
screen = pygame.display.set_mode(size=(scr_width, scr_height))
def ClearScreen():
    screen.fill(Color.black)
def UpdateScreen():
    pygame.display.update()
    pygame.time.delay(20)

# GUI View
canvas = GUICanvas()
ccLabel = GUILabel(position=(scr_width/2, scr_height/2), text='Welcome to the game, Buddy!', font_name="Sans Serif", font_size=32, label_color=Color.white)
lbLabel = GUILabel(position=(0, scr_height), text='LEFT BOTTOM', font_name="Sans Serif", font_size=32, label_color=Color.white, anchor_horizontal=Anchor.LEFT, anchor_vertical=Anchor.BOTTOM)
rbLabel = GUILabel(position=(scr_width, scr_height), text='RIGHT BOTTOM', font_name="Sans Serif", font_size=32, label_color=Color.white, anchor_horizontal=Anchor.RIGHT, anchor_vertical=Anchor.BOTTOM)
ltLabel = GUILabel(position=(0, 0), text='LEFT TOP', font_name="Sans Serif", font_size=32, label_color=Color.white, anchor_horizontal=Anchor.LEFT, anchor_vertical=Anchor.TOP)
rtLabel = GUILabel(position=(scr_width, 0), text='RIGHT TOP', font_name="Sans Serif", font_size=32, label_color=Color.white, anchor_horizontal=Anchor.RIGHT, anchor_vertical=Anchor.TOP)
canvas.ExtendElements([ccLabel, lbLabel, rbLabel, ltLabel, rtLabel])

def main():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        ClearScreen()

        canvas.Draw(screen)
        
        UpdateScreen()

main()