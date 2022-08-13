from abc import ABC, abstractmethod
from enum import Enum
from mimetypes import init
import re
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
    _init_x = 0
    _init_y = 0

    @abstractmethod
    def __init__(self, position: tuple[int, int], anchor_horizontal: Anchor = Anchor.CENTER, anchor_vertical: Anchor = Anchor.CENTER) -> None:
        self.SetPosition(position[0], position[1], override_init=True)
        self.SetAnchor(anchor_horizontal, anchor_vertical)
    
    def SetPosition(self, x: int, y: int, override_init: bool = False):
        self.position_x = x
        self.position_y = y
        if override_init:
            self._init_x = x
            self._init_y = y
    
    def SetAnchor(self, anchor_horizontal: Anchor, anchor_vertical: Anchor):
        self.anchor_horizontal = anchor_horizontal
        self.anchor_vertical = anchor_vertical

    # Pin Element to current anchor.
    def PinToAnchor(self, component_width: int, component_height: int):
        self.SetPosition(self._init_x, self._init_y)
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

class GUIRect(GUIComponent):
    _color = Color.white

    _width = 0
    _height = 0

    _is_clickable = False

    def __init__(self, position: tuple[int, int], width: int, height: int, is_clickable = False, rect_color = Color.white, anchor_horizontal: Anchor = Anchor.CENTER, anchor_vertical: Anchor = Anchor.CENTER) -> None:
        super().__init__(position, anchor_horizontal, anchor_vertical)
        self.SetClickableStatus(is_clickable)
        self.SetColor(rect_color)
        self.Create(width, height)
    
    def Create(self, width: int, height: int):
        self.SetSize(width, height)
        self.SetRect()

    def SetClickableStatus(self, is_clickable: bool):
        self._is_clickable = is_clickable

    def SetColor(self, rect_color: Color):
        self._color = rect_color

    def SetSize(self, width: int, height: int):
        self._width = width
        self._height = height
        self.Fit()
    
    def SetRect(self):
        self.rect = pygame.Rect(self.position_x, self.position_y, self._width, self._height)

    def Fit(self):
        self.PinToAnchor(component_width=self._width, component_height=self._height)
    
    is_pressed = False
    def OnClick(self, methodToRun='', args=''):
        if self._is_clickable and not self.is_pressed:
            self.is_pressed = True
            if methodToRun:
                methodToRun(args) if args != '' else methodToRun()
            print(f'{self.rect} has clicked.')
    
    def OnClickOver(self):
        if self.is_pressed:
            self.is_pressed = False

    def Draw(self, screen: pygame.display):
        pygame.draw.rect(surface=screen, color=self._color, rect=self.rect)

class GUILabel(GUIComponent):
    _color = Color.white

    def __init__(self, position: tuple[int, int], text: str, font_name: str, font_size: int, label_color = Color.white, anchor_horizontal: Anchor = Anchor.CENTER, anchor_vertical: Anchor = Anchor.CENTER) -> None:
        super().__init__(position, anchor_horizontal, anchor_vertical)
        self.SetFont(font_name, font_size)
        self.SetColor(label_color)
        self.SetLabel(text)

    def SetFont(self, name: str, size: int):
        self.font = pygame.font.SysFont(name, size)

    def SetColor(self, label_color: Color):
        self._color = label_color

    def SetLabel(self, text: str):
        self.label = self.font.render(text, True, self._color)
        self.Fit()
    
    def Fit(self):
        self.PinToAnchor(component_width=self.label.get_width(), component_height=self.label.get_height())

    def Draw(self, screen: pygame.display):
        screen.blit(self.label, (self.position_x, self.position_y))

class GUIButton(GUIComponent):

    # ? Split GUIRect and GUILabel only for necessary properties
    # TODO: Border_radius
    def __init__(self, rect: GUIRect, caption: GUILabel, anchor_horizontal: Anchor = Anchor.CENTER, anchor_vertical: Anchor = Anchor.CENTER) -> None:
        super().__init__((rect.position_x, rect.position_y), anchor_horizontal, anchor_vertical)
        self.SetButton(rect, caption)
        self.Fit()
    
    def SetButton(self, rect: GUIRect, caption: GUILabel):
        rect.SetClickableStatus(True)
        rect.Create(rect._width + caption.label.get_width(), rect._height + caption.label.get_height())
        self.SetRect(rect)

        caption.SetPosition(rect._init_x + caption._init_x, rect._init_y + caption._init_y, override_init=True)
        self.SetCaption(caption)

    def SetRect(self, rect: GUIRect):
        self.rect = rect

    def SetCaption(self, caption: GUILabel):
        self.caption = caption
    
    def Fit(self):
        self.caption.Fit()
        self.rect.Fit()
    
    def OnClick(self, methodToRun, args=('')):
        self.rect.OnClick(methodToRun, args)
    
    def OnClickOver(self):
        self.rect.OnClickOver()

    def Draw(self, screen: pygame.display):
        self.rect.Draw(screen)
        self.caption.Draw(screen)

# GUI Canvas
class GUICanvas:
    GUIElements: GUIComponent = []

    def AppendElement(self, element: GUIComponent):
        self.GUIElements.append(element)
    
    def ExtendElements(self, elements: set[GUIComponent]):
        self.GUIElements.extend(elements)

    def Clear(self):
        self.GUIElements.clear()

    def Draw(self, screen: pygame.display):
        for i in self.GUIElements:
            i.Draw(screen)