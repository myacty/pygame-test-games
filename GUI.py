from abc import ABC, abstractmethod
from enum import Enum
from mimetypes import init
import pygame

import COLORS as Color

# ? My custom GUI module.
# ! PYGAME is required.

pygame.init()

# Anchors
class Anchor(Enum):
    CENTER = 0,
    LEFT = 1,
    RIGHT = 2,
    TOP = 3,
    BOTTOM = 4,

# GUI
class GUIComponent(ABC):
    init_x = 0
    init_y = 0

    @abstractmethod
    def __init__(self, position: tuple[int, int], anchor_horizontal: Anchor = Anchor.CENTER, anchor_vertical: Anchor = Anchor.CENTER) -> None:
        self.SetPosition(position[0], position[1], override_init=True)
        self.SetAnchor(anchor_horizontal, anchor_vertical)
    
    def SetPosition(self, x: int, y: int, override_init: bool = False):
        self.position_x = x
        self.position_y = y
        if override_init:
            self.init_x = x
            self.init_y = y
    
    def SetAnchor(self, anchor_horizontal: Anchor, anchor_vertical: Anchor):
        self.anchor_horizontal = anchor_horizontal
        self.anchor_vertical = anchor_vertical

    # Pin Element to current anchor.
    def PinToAnchor(self, component_width: int, component_height: int):
        self.SetPosition(self.init_x, self.init_y)
        match self.anchor_horizontal:
            case Anchor.CENTER:
                self.SetPosition(self.position_x-component_width/2, self.position_y)
            case Anchor.LEFT:
                self.SetPosition(self.position_x, self.position_y)
            case Anchor.RIGHT:
                self.SetPosition(self.position_x-component_width, self.position_y)
        match self.anchor_vertical:
            case Anchor.CENTER:
                self.SetPosition(self.position_x, self.position_y-component_height/2)
            case Anchor.TOP:
                self.SetPosition(self.position_x, self.position_y)
            case Anchor.BOTTOM:
                self.SetPosition(self.position_x, self.position_y-component_height)    
    
    # Pin Element to overriding anchor.
    def PinToAnchorOverrided(self, component_width: int, component_height: int, anchor_horizontal: Anchor, anchor_vertical: Anchor):
        self.SetAnchor(anchor_horizontal, anchor_vertical)
        self.PinToAnchor(component_width, component_height)
    
    def Draw(self):
        pass

class GUILabel(GUIComponent):
    color = Color.white

    def __init__(self, position: tuple[int, int], text: str, font_name: str, font_size: int, label_color = Color.white, anchor_horizontal: Anchor = Anchor.CENTER, anchor_vertical: Anchor = Anchor.CENTER) -> None:
        super().__init__(position, anchor_horizontal, anchor_vertical)
        self.SetFont(font_name, font_size)
        self.SetColor(label_color)
        self.SetLabel(text)

    def SetFont(self, name: str, size: int):
        self.font = pygame.font.SysFont(name, size)

    def SetColor(self, label_color: Color):
        self.color = label_color

    def SetLabel(self, text: str):
        self.label = self.font.render(text, True, self.color)
        self.Fit()
    
    def Fit(self):
        self.PinToAnchor(component_width=self.label.get_width(), component_height=self.label.get_height())

    def Draw(self, screen: pygame.display):
        screen.blit(self.label, (self.position_x, self.position_y))

# GUI Canvas
class GUICanvas:
    GUIElements = []

    def AppendElement(self, element: GUIComponent):
        self.GUIElements.append(element)
    
    def ExtendElements(self, elements: set[GUIComponent]):
        self.GUIElements.extend(elements)

    def Clear(self):
        self.GUIElements.clear()

    def Draw(self, screen: pygame.display):
        for i in self.GUIElements:
            i.Draw(screen)