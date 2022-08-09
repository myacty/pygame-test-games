from abc import ABC, abstractmethod
from enum import Enum
import pygame

pygame.init()

# Colors
class Color:
    white = (255, 255, 255)
    red = (255, 0, 0)
    green = (0, 255, 0)
    blue = (0, 0, 255)
    black = (0, 0, 0)

# Anchors
class Anchor(Enum):
    CENTER = 0,
    LEFT = 1,
    RIGHT = 2,
    TOP = 3,
    BOTTOM = 4,

# Game Screen
scr_width = 960
scr_height = 540
screen = pygame.display.set_mode(size=(scr_width, scr_height))
def ClearScreen():
    screen.fill(Color.black)
def UpdateScreen():
    pygame.display.update()
    pygame.time.delay(20)

# GUI
class GUIComponent(ABC):
    @abstractmethod
    def __init__(self, position: tuple[int, int]) -> None:
        self.SetPosition(position[0], position[1])
    
    def SetPosition(self, x: int, y: int):
        self.position_x = x
        self.position_y = y
    
    def PinToAnchor(self, component_width: int, component_height: int, anchor_horizontal: Anchor = Anchor.CENTER, anchor_vertical: Anchor = Anchor.CENTER):
        match anchor_horizontal:
            case Anchor.CENTER:
                self.SetPosition(self.position_x-component_width/2, self.position_y)
            case Anchor.LEFT:
                self.SetPosition(self.position_x, self.position_y)
            case Anchor.RIGHT:
                self.SetPosition(self.position_x-component_width, self.position_y)
        match anchor_vertical:
            case Anchor.CENTER:
                self.SetPosition(self.position_x, self.position_y-component_height/2)
            case Anchor.TOP:
                self.SetPosition(self.position_x, self.position_y)
            case Anchor.BOTTOM:
                self.SetPosition(self.position_x, self.position_y-component_height)    
    
    def Draw(self):
        pass

class GUILabel(GUIComponent):
    def __init__(self, position: tuple[int, int], text: str, font_name: str, font_size: int, label_color = Color.white, anchor_horizontal: Anchor = Anchor.CENTER, anchor_vertical: Anchor = Anchor.CENTER) -> None:
        super().__init__(position)
        self.SetFont(font_name, font_size)
        self.SetLabel(text, label_color)
        super().PinToAnchor(component_width=self.label.get_width(), component_height=self.label.get_height(), anchor_horizontal=anchor_horizontal, anchor_vertical=anchor_vertical)

    def SetFont(self, name: str, size: int):
        self.font = pygame.font.SysFont(name, size)

    def SetLabel(self, text: str, label_color):
        self.label = self.font.render(text, True, label_color)
    
    def Draw(self):
        screen.blit(self.label, (self.position_x, self.position_y))

# GUI Canvas
class GUI:
    GUIElements = []

    def AppendElement(self, element: GUIComponent):
        self.GUIElements.append(element)
    
    def ExtendElements(self, elements: set[GUIComponent]):
        self.GUIElements.extend(elements)

    def Draw(self):
        for i in self.GUIElements:
            i.Draw()

# GUI View
GUICanvas = GUI()
ccLabel = GUILabel(position=(scr_width/2, scr_height/2), text='Welcome to the game, Buddy!', font_name="Sans Serif", font_size=32, label_color=Color.white)
lbLabel = GUILabel(position=(0, scr_height), text='LEFT BOTTOM', font_name="Sans Serif", font_size=32, label_color=Color.white, anchor_horizontal=Anchor.LEFT, anchor_vertical=Anchor.BOTTOM)
rbLabel = GUILabel(position=(scr_width, scr_height), text='RIGHT BOTTOM', font_name="Sans Serif", font_size=32, label_color=Color.white, anchor_horizontal=Anchor.RIGHT, anchor_vertical=Anchor.BOTTOM)
ltLabel = GUILabel(position=(0, 0), text='LEFT TOP', font_name="Sans Serif", font_size=32, label_color=Color.white, anchor_horizontal=Anchor.LEFT, anchor_vertical=Anchor.TOP)
rtLabel = GUILabel(position=(scr_width, 0), text='RIGHT TOP', font_name="Sans Serif", font_size=32, label_color=Color.white, anchor_horizontal=Anchor.RIGHT, anchor_vertical=Anchor.TOP)
GUICanvas.ExtendElements([ccLabel, lbLabel, rbLabel, ltLabel, rtLabel])

def main():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        ClearScreen()
        GUICanvas.Draw()
        UpdateScreen()

main()