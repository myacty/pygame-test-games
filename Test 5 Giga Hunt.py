from abc import ABC, abstractmethod
import os
import pygame

# Some Math Shit
def clamp(num, min_value, max_value):
   return max(min(num, max_value), min_value)

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
    input_hover = False

    def GetMousePos() -> tuple[int, int]:
        return pygame.mouse.get_pos()

    def OnClick(down: bool):
        MouseCursor.input_LMB = down
    
    def OnHover(on: bool):
        MouseCursor.input_hover = on

    def DrawNormalState():
        MouseCursor.DrawCircle(radius=16, color=Color.white)
    
    def DrawClickedState():
        if MouseCursor.input_LMB:
            MouseCursor.DrawCircle(radius=14, color=Color.black)  
    
    def DrawHoverState():
        if MouseCursor.input_hover:
            MouseCursor.DrawCircle(radius=8, color=Color.red)    
            #MouseCursor.OnHover(False)
    
    def DrawCircle(radius: float, color: Color = Color.white):
        pygame.draw.circle(surface=screen, color=color, center=pygame.mouse.get_pos(), radius=radius) 
    
    def Draw():
        MouseCursor.DrawNormalState()
        MouseCursor.DrawClickedState()
        MouseCursor.DrawHoverState()

# Game Assets
data_path = os.path.dirname(__file__)
sounds_data_path = os.path.dirname(__file__) + '\Sounds'
sprites_data_path = os.path.dirname(__file__) + '\Sprites'

def LoadSound(name: str) -> pygame.mixer.Sound:
    return pygame.mixer.Sound(sounds_data_path + name)

def LoadMusic(name: str) -> pygame.mixer.Sound:
    return pygame.mixer.music.load(sounds_data_path + name)

def LoadSprite(name: str) -> pygame.image:
    return pygame.image.load(sprites_data_path + name)

# Game Objects
class GameObject:
    name = 'New Game Object'
    position_x = 0
    position_y = 0

    def __init__(self, name: str, position: tuple[int, int]) -> None:
        self.SetName(name)
        self.SetPosition(position[0], position[1])
    
    def SetName(self, name: str):
        self.name = name

    def SetPosition(self, x: int, y: int):
        self.position_x = x
        self.position_y = y
        self.OnPositionChanged()
    
    def MoveInDirection(self, x: int, y: int, velocity: float = 1.0):
        self.SetPosition(self.position_x + (x * velocity), self.position_y + (y * velocity))
    
    def OnPositionChanged(self): pass

    def Destroy(self):
        self = None
        self.OnDestroy()
    
    def OnDestroy(self): pass

class SpritedGameObject(GameObject):
    scale = 1.0
    sprite_pack = []
    sprite = LoadSprite('\\None.svg')
    collider = pygame.Rect(0, 0, 0, 0)

    def __init__(self, name: str, position: tuple[int, int], sprite_pack: set[str], scale: float) -> None:
        super().__init__(name, position)
        self.SetScale(scale)
        self.LoadSpritePack(sprite_pack)
        self.SetCollider()
    
    def SetScale(self, scale: int):
        self.scale = scale

    def LoadSpritePack(self, sprite_pack: list):
        for i in sprite_pack:
            self.sprite_pack.append(LoadSprite(i))
        self.SetDefaultSprite()
    
    def SetDefaultSprite(self):
        self.SetSprite(self.sprite_pack[0])

    def SetSprite(self, sprite: pygame.image):
        self.sprite = pygame.transform.scale(sprite, (sprite.get_width() * self.scale, sprite.get_height() * self.scale))
        self.sprite = pygame.transform.flip(self.sprite, flip_x=self.is_looking_left, flip_y=False)

    def SetCollider(self):
        self.collider = pygame.Rect(self.position_x, self.position_y, self.sprite.get_width(), self.sprite.get_height())
    
    def Draw(self):
        screen.blit(self.sprite, self.collider)
    
    frame = 0
    def PlayAnimation(self):
        self.SetSprite(self.sprite_pack[self.frame])
        self.frame += 1
        if self.frame >= self.sprite_pack.__len__():
            self.frame = 0

    is_looking_left = False
    def FlipSprite(self, look_left: bool):
        self.is_looking_left = look_left

    def OnPositionChanged(self):
        self.SetCollider()
        self.Draw()

class Victim(SpritedGameObject):
    current_point_id = 0
    current_movement_point = GameObject
    movement_points = [GameObject]

    dir_x = 0
    dir_y = 0

    at_gunpoint = False

    def __init__(self, name: str, position: tuple[int, int], sprite_pack: set[str], scale: float) -> None:
        super().__init__(name, position, sprite_pack, scale)
    
    def SetMovementPoints(self, points: list[GameObject]):
        self.movement_points = points
        self.SetNextMovementPoint()
    
    def SetNextMovementPoint(self):
        self.current_point_id += 1
        if (self.current_point_id >= self.movement_points.__len__()):
            self.current_point_id = 0
        self.current_movement_point = self.movement_points[self.current_point_id]
    
    def SetRandomMovementPoint(self): # TODO: 
        pass

    def GetDirectionToPoint(self, movement_point: GameObject) -> tuple[int, int]:
        return [clamp(movement_point.position_x - self.position_x, -1, 1), clamp(movement_point.position_y - self.position_y, -1, 1)]
    def MovementPointIsCrossed(self, movement_point: GameObject) -> bool:
        return movement_point.position_x == self.position_x and movement_point.position_y == self.position_y
    def MoveToCurrentPoint(self):
        direction = self.GetDirectionToPoint(self.current_movement_point)
        self.dir_x = direction[0]
        self.dir_y = direction[1]
        self.MoveInDirection(self.dir_x, self.dir_y, velocity=5)
        if self.MovementPointIsCrossed(self.current_movement_point):
            self.SetNextMovementPoint()

    def CursorIsColliding(self) -> bool:
        return self.collider.collidepoint(MouseCursor.GetMousePos())
    
    def UpdateCursorColliding(self):
        if self.at_gunpoint and not self.CursorIsColliding():
            MouseCursor.OnHover(False)
        self.at_gunpoint = self.CursorIsColliding()
        if self.at_gunpoint:
            MouseCursor.OnHover(True)
            self.SetNextMovementPoint()

    def PhysicsUpdate(self):
        self.MoveToCurrentPoint()
        self.UpdateCursorColliding()
    
    def RenderingUpdate(self):
        self.FlipSprite(look_left=self.dir_x < 0)
        self.Draw()
        if self.dir_x != 0 or self.dir_y != 0:
            self.PlayAnimation()
        else:
            self.SetDefaultSprite()

# Game World
# TODO: Спавнер гигов
giga = Victim('Giga_1', (scr_width/2, scr_height/2), ['\Player_0.svg', '\Player_1.svg', '\Player_2.svg'], 0.5)
giga.SetMovementPoints([GameObject('point_1', (scr_width, 0)), GameObject('point_2', (0, 0))])

giga2 = Victim('Giga_2', (scr_width/2, scr_height/2), ['\Player_0.svg', '\Player_1.svg', '\Player_2.svg'], 0.5)
giga2.SetMovementPoints([GameObject('point_1', (50, 100)), GameObject('point_2', (600, 300)), GameObject('point_2', (900, 20))])


# Physics Queue
def PhysicsUpdate():
    giga.PhysicsUpdate()
    giga2.PhysicsUpdate()

# Rendering Queue
def RenderingUpdate():
    giga.RenderingUpdate()
    giga2.RenderingUpdate()
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
        
        PhysicsUpdate()
        RenderingUpdate()
        
        UpdateScreen()

main()