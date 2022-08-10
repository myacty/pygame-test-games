from abc import ABC, abstractmethod
import os
import pygame

import COLORS as Color
import GUI

pygame.init()
clock = pygame.time.Clock()
clock_speed = 25 # FPS

# Game Screen
scr_width = 960
scr_height = 540
screen = pygame.display.set_mode(size=(scr_width, scr_height))
def ClearScreen():
    screen.fill(Color.black)
def UpdateScreen():
    pygame.display.update()
    clock.tick(clock_speed)

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

# SFX & Music
class Sounds:
    PopSound = LoadSound('\Pop.wav')
#Sounds.PopSound.play()

class Music:
    MainTheme = LoadMusic('\Pop.wav')
#pygame.mixer.music.play()

# Game Objects
class GameObject(ABC):
    @abstractmethod
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
    
    def OnPositionChanged(): pass

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
    
    frame = 1
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

player_spawn_point = (scr_width/2, scr_height * 0.8)
player_scale = 0.5
player = SpritedGameObject('Player', player_spawn_point, ['\Player_0.svg', '\Player_1.svg', '\Player_2.svg'], player_scale)

# Input System
class Input:
    x_input = 0
    y_input = 0

    def SetInput(x: int = x_input, y: int = y_input):
        Input.x_input = x
        Input.y_input = y

# DEBUG
print('Game Loaded')

def main():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    Input.SetInput(x=1)
                if event.key == pygame.K_LEFT:
                    Input.SetInput(x=-1) 
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                    Input.SetInput(x=0)
        
        ClearScreen()

        player.MoveInDirection(x=Input.x_input, y=Input.y_input, velocity=5)
        if Input.x_input != 0:
            player.PlayAnimation()
            player.FlipSprite(look_left=Input.x_input < 0)
        else:
            player.SetDefaultSprite()

        UpdateScreen()

main()