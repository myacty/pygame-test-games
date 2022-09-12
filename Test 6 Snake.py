from random import randint
from typing import List
import pygame

import COLORS as Color

pygame.init()

pygame.display.set_caption('Snake Game')

scr_width = 960
scr_height = 540
screen = pygame.display.set_mode(size=(scr_width, scr_height))

clock = pygame.time.Clock()
framerate = 15 # FPS

class Tail:
    pos_x = 0
    pos_y = 0
    size = 15
    color = Color.white

    def __init__(self, start_pos_x: int, start_pos_y: int, start_size: int, start_color: Color = Color.red) -> None:
        self.SetSize(start_size)
        self.SetPosition(start_pos_x, start_pos_y)
        self.SetColor(start_color)

    def SetPosition(self, x: int, y: int):
        self.pos_x = x
        self.pos_y = y
    
    def SetSize(self, size: int):
        self.size = size
    
    def SetColor(self, color: Color):
        self.color = color
    
    rect: pygame.Rect = None
    def Draw(self):
        self.rect = pygame.draw.rect(screen, self.color, (self.pos_x, self.pos_y, self.size, self.size))

class Snake:
    pos_x = 0
    pos_y = 0
    direction = -90
    size = 15
    color = Color.white

    # TODO: Создать лист "хвостов"
    tails:List[Tail] = list()

    def __init__(self, start_pos_x: int, start_pos_y: int, start_size: int, start_color: Color = Color.white) -> None:
        self.SetSize(start_size)
        self.SetPosition(start_pos_x, start_pos_y)
        self.SetColor(start_color)

    def SetPosition(self, x: int, y: int):
        self.pos_x = x - self.size
        self.pos_y = y - self.size
    
    def SetSize(self, size: int):
        self.size = size

    def SetDirection(self, angle: int):
        if (self.CheckReverseAbility(angle)):
            self.direction = angle

    def SetColor(self, color: Color):
        self.color = color

    # TODO: Улучшить методы чтобы получить бесконечную змейку
    def MoveLeft(self):
        if self.pos_x > self.size / 2:
            self.pos_x -= self.size
        else:
            self.pos_x = scr_width - self.size

    def MoveRight(self):
        if self.pos_x < scr_width - self.size:
            self.pos_x += self.size
        else:
            self.pos_x = 0
    
    def MoveUp(self):
        if self.pos_y > self.size / 2:
            self.pos_y -= self.size
        else:
            self.pos_y = scr_height - self.size
    
    def MoveDown(self):
        if self.pos_y < scr_height - self.size:
            self.pos_y += self.size
        else:
            self.pos_y = 0
    
    # ? Проверить работоспособность метода
    def MoveForward(self):
        match self.direction:
            case 0:
                self.MoveUp()
            case 90:
                self.MoveRight()
            case 180:
                self.MoveDown()
            case -90:
                self.MoveLeft()
        pygame.time.delay(10)

    # ? Проверить работоспособность невозможности разворота
    def CheckReverseAbility(self, angle: int) -> bool:
        if (self.tails.__len__() > 0):
            match self.direction, angle:
                case 0, 180:
                    return False
                case 90, -90:
                    return False
                case 180, 0:
                    return False
                case -90, 90:
                    return False
        return True

    # TODO: Инициализировать этот метод
    def GrowUp(self):
        new_tail: Tail = Tail(scr_width + 1, scr_height + 1, self.size)
        self.tails.append(new_tail)
    
    # TODO: Инициализировать этот метод
    def MoveTail(self):
        # ? if "количество хвостов" == 3:
        # todo:   self.tails[2].SetPosition(self.tails[1].pos_x, self.tails[1].pos_y)
        # todo:   self.tails[1].SetPosition(self.tails[0].pos_x, self.tails[0].pos_y)
        # todo:   self.tails[0].SetPosition(self.pos_x, self.pos_y)
        # ? if "количество хвостов" == 2:
        # todo:   self.tails[1].SetPosition(self.tails[0].pos_x, self.tails[0].pos_y)
        # todo:   self.tails[0].SetPosition(self.pos_x, self.pos_y)
        # ? if "количество хвостов" == 1:
        # todo: self.tails[0].SetPosition(self.pos_x, self.pos_y)
        
        for i in reversed(range(self.tails.__len__())):
            if i == 0:
                self.tails[0].SetPosition(self.pos_x, self.pos_y)
            else:
                self.tails[i].SetPosition(self.tails[i-1].pos_x, self.tails[i-1].pos_y)    
    
    # TODO: Отрисовка "хвостов" следом за головой
    # TODO: Присовение отрисованного ректа к self.rect
    rect: pygame.Rect = None
    def Draw(self):
        self.rect = pygame.draw.rect(screen, self.color, (self.pos_x, self.pos_y, self.size, self.size))
        for tail in self.tails:
            tail.Draw()

class Food:
    pos_x = 0
    pos_y = 0
    size = 15
    color = Color.red

    def __init__(self, start_size: int, start_color: Color = Color.red) -> None:
        self.SetSize(start_size)
        self.SetRandomPosition()
        self.SetColor(start_color)
    
    def SetPosition(self, x: int, y: int):
        self.pos_x = x - self.size
        self.pos_y = y - self.size
    
    def SetSize(self, size: int):
        self.size = size

    def SetColor(self, color: Color):
        self.color = color
        
    def SetRandomPosition(self):
        width_cellcount = scr_width / self.size
        height_cellcount = scr_height / self.size
        x = randint(1, width_cellcount) * self.size
        y = randint(1, height_cellcount) * self.size
        self.SetPosition(x, y)

    rect: pygame.Rect = None
    def Draw(self):
        self.rect = pygame.draw.rect(screen, self.color, (self.pos_x, self.pos_y, 15, 15))

# ! Продвинутый левел-дизайн
class Wall:
    pos_x = 0
    pos_y = 0
    size = 15
    color = Color.grey

    def __init__(self, start_pos_x: int, start_pos_y: int, start_size: int, start_color: Color = Color.grey) -> None:
        self.SetSize(start_size)
        self.SetPosition(start_pos_x, start_pos_y)
        self.SetColor(start_color)
    
    def SetPosition(self, x: int, y: int):
        self.pos_x = x * self.size
        self.pos_y = y * self.size
    
    def SetSize(self, size: int):
        self.size = size

    def SetColor(self, color: Color):
        self.color = color

    rect: pygame.Rect = None
    def Draw(self):
        self.rect = pygame.draw.rect(screen, self.color, (self.pos_x, self.pos_y, 15, 15))

# ! Продвинутый левел-дизайн
class GameMap:
    CHAR_EMPTY = ''
    CHAR_WALL = 'x'
    CHAR_MAP = (
        ['x', 'x', 'x', 'x', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'x', 'x', 'x', 'x'],
        ['x', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'x'],
        ['x', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'x'],
        ['x', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'x'],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    )

    walls:List[Wall] = list()

    def __init__(self) -> None:
        self.Create()

    def Create(self):
        for i, e in enumerate(self.CHAR_MAP):
            for j, c in enumerate(e):
                if c == 'x':
                    self.walls.append(Wall(j, i, 15))

    def Draw(self):
        for i in self.walls:
            i.Draw()

# TODO: Новые методы: OnWallCollision, OnTailCollision, GameOver, и специальный _HasRectCollide для новой проверки коллизий.
class GameObserver:
    GameIsActive = True

    def CheckWallCollision(snake: Snake):
        for wall in gamemap.walls:
            if GameObserver._HasRectCollide(snake.rect, wall.rect):
                GameObserver._OnWallCollision(snake)
    
    def CheckTailCollision(snake: Snake):
        for tail in snake.tails:
            if GameObserver._HasRectCollide(snake.rect, tail.rect):
                GameObserver._OnTailCollision(snake)
    
    def CheckFoodCollision(snake: Snake, food: Food):
        if GameObserver._HasRectCollide(snake.rect, food.rect):
            GameObserver._OnFoodCollision(snake, food)
    
    def _OnWallCollision(snake: Snake):
        print("Wall hit.")
        GameObserver._GameOver()
    
    def _OnTailCollision(snake: Snake):
        print("Tail hit.")
        GameObserver._GameOver()

    def _OnFoodCollision(snake: Snake, food: Food):
        food.SetRandomPosition()
        snake.GrowUp()
        print("Score:", snake.tails.__len__())
    
    def _GameOver():
        GameObserver.GameIsActive = False
        print('Game over.')

    def _HasRectCollide(rect1: pygame.Rect, rect2: pygame.Rect) -> bool:
        if rect1 == None or rect2 == None: return False
        return rect1.colliderect(rect2.left, rect2.top, rect2.width, rect2.height)

class InputListener:
    is_left_pressed = False
    is_right_pressed = False
    is_up_pressed = False
    is_down_pressed = False

player = Snake(scr_width/2, scr_height/2, 15)
food = Food(15, Color.GetRandomColor())
gamemap = GameMap()

run = True
while run:
    # * Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                InputListener.is_left_pressed = True
            if event.key == pygame.K_RIGHT:
                InputListener.is_right_pressed = True
            if event.key == pygame.K_UP:
                InputListener.is_up_pressed = True
            if event.key == pygame.K_DOWN:
                InputListener.is_down_pressed = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                InputListener.is_left_pressed = False
            if event.key == pygame.K_RIGHT:
                InputListener.is_right_pressed = False
            if event.key == pygame.K_UP:
                InputListener.is_up_pressed = False
            if event.key == pygame.K_DOWN:
                InputListener.is_down_pressed = False

    # * Behaviour
    if GameObserver.GameIsActive:
        if InputListener.is_left_pressed:
            player.SetDirection(-90)
        elif InputListener.is_right_pressed:
            player.SetDirection(90)
        if InputListener.is_up_pressed:
            player.SetDirection(0)
        elif InputListener.is_down_pressed:
            player.SetDirection(180)
        player.MoveTail()
        player.MoveForward()

        GameObserver.CheckWallCollision(player)
        GameObserver.CheckTailCollision(player)
        GameObserver.CheckFoodCollision(player, food)

    # * Draw-call
    screen.fill(Color.black)

    player.Draw()
    food.Draw()
    gamemap.Draw()

    pygame.display.update()
    clock.tick(framerate)