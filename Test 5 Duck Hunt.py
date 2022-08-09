from abc import ABC, abstractmethod
import os
import pygame

pygame.init()
clock = pygame.time.Clock()
clock_speed = 60 # FPS

# Colors
class Color:
    white = (255, 255, 255)
    red = (255, 0, 0)
    green = (0, 255, 0)
    blue = (0, 0, 255)
    black = (0, 0, 0)

# Game Screen
scr_width = 960
scr_height = 540
screen = pygame.display.set_mode(size=(scr_width, scr_height))
def ClearScreen():
    screen.fill(Color.black)
def UpdateScreen():
    pygame.display.update()
    clock.tick(clock_speed)

# Game Cursor
class MouseCursor:
    input_LMB = False

    def OnClick(down: bool):
        MouseCursor.input_LMB = down
    
    def DrawNormalState():
        MouseCursor.DrawCircle(radius=16, color=Color.white)

    def DrawClickedState():
        if MouseCursor.input_LMB:
            MouseCursor.DrawCircle(radius=14, color=Color.black)    
    
    def DrawCircle(radius: float, color: Color = Color.white):
        pygame.draw.circle(surface=screen, color=color, center=pygame.mouse.get_pos(), radius=radius) 
    
    def Draw():
        MouseCursor.DrawNormalState()
        MouseCursor.DrawClickedState()

# Rendering Queue
def RenderAll():
    MouseCursor.Draw()

# Main Game-loop
def main():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                MouseCursor.OnClick(down=event.button == 1)
            if event.type == pygame.MOUSEBUTTONUP:
                MouseCursor.OnClick(down=not event.button == 1)
        
        ClearScreen()
        RenderAll()
        UpdateScreen()

main()