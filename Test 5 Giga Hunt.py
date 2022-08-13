from cmath import e
from enum import Enum
import os
import pygame
from random import randint

import COLORS as Color
from GUI import Anchor
from GUI import GUIRect
from GUI import GUILabel
from GUI import GUIButton
from GUI import GUICanvas

# ? Duck-Hunt-Style game.

# Some Math Shit
def clamp(num, min_value, max_value):
   return max(min(num, max_value), min_value)

def sqr_magnitude(start: tuple[int, int], end: tuple[int, int]):
    return (end[0] - start[0])**2 + (end[1] - start[1])**2

pygame.init()

clock = pygame.time.Clock()
clock_speed = 144 # FPS Limit

class Time:
    delta_time = 0
    def SetDeltaTime():
        Time.delta_time = clock.tick(clock_speed)
    def GetRealSecond() -> int:
        return Time.delta_time * 0.001

# Game Screen
scr_width = 960
scr_height = 540
screen = pygame.display.set_mode(size=(scr_width, scr_height))
def ClearScreen():
    screen.fill(Color.black)
def UpdateScreen():
    pygame.display.update()
    Time.SetDeltaTime()

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

# ? Move MouseCursor to GUI (or another special component)
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
        if MouseCursor.input_LMB or not player.HasAmmo:
            MouseCursor.DrawCircle(radius=14, color=Color.black)  
    
    def DrawHoverState():
        if MouseCursor.input_hover:
            MouseCursor.DrawCircle(radius=8, color=Color.red)
    
    def DrawCircle(radius: float, color: Color = Color.white):
        pygame.draw.circle(surface=screen, color=color, center=pygame.mouse.get_pos(), radius=radius) 
    
    def Draw():
        MouseCursor.DrawNormalState()
        MouseCursor.DrawClickedState()
        MouseCursor.DrawHoverState()

class UIScreen(Enum):
    MAIN_MENU = 0,
    GAME_RUN = 1,
    GAME_END = 2

# GUI View
class UI:
    canvas = GUICanvas()

    menu_label = GUILabel(position=(scr_width/2, scr_height/3), text='GIGA HUNT GAME 2022.', font_name="Sans Serif", font_size=64, label_color=Color.white, anchor_horizontal=Anchor.CENTER, anchor_vertical=Anchor.CENTER)
    menu_casual_btn = GUIButton(GUIRect(position=(scr_width/2, scr_height/3+96), width=32, height=32), GUILabel((0,0), 'CASUAL', font_name="Sans Serif", font_size=64, label_color=Color.black))
    menu_normal_btn = GUIButton(GUIRect(position=(scr_width/2, scr_height/3+96+96), width=32, height=32), GUILabel((0,0), 'NORMAL', font_name="Sans Serif", font_size=64, label_color=Color.black))
    menu_hard_btn = GUIButton(GUIRect(position=(scr_width/2, scr_height/3+96+96+96), width=32, height=32), GUILabel((0,0), 'HARD', font_name="Sans Serif", font_size=64, label_color=Color.black))
    
    game_run_timer_label = GUILabel(position=(scr_width/2, 0), text='TIME REMAINING:', font_name="Sans Serif", font_size=32, label_color=Color.white, anchor_horizontal=Anchor.CENTER, anchor_vertical=Anchor.TOP)
    game_run_score_label = GUILabel(position=(scr_width, scr_height), text='KILLS:', font_name="Sans Serif", font_size=32, label_color=Color.white, anchor_horizontal=Anchor.RIGHT, anchor_vertical=Anchor.BOTTOM)
    game_run_ammo_label = GUILabel(position=(0, scr_height), text='AMMO:', font_name="Sans Serif", font_size=32, label_color=Color.white, anchor_horizontal=Anchor.LEFT, anchor_vertical=Anchor.BOTTOM)

    game_end_label = GUILabel(position=(scr_width/2, scr_height/2), text='GAME OVER.', font_name="Sans Serif", font_size=64, label_color=Color.white, anchor_horizontal=Anchor.CENTER, anchor_vertical=Anchor.CENTER)
    game_end_status_label = GUILabel(position=(scr_width/2, game_end_label.position_y+64), text="Time's Up!", font_name="Sans Serif", font_size=32, label_color=Color.white, anchor_horizontal=Anchor.CENTER, anchor_vertical=Anchor.TOP)
    game_end_score_label = GUILabel(position=(scr_width/2, game_end_status_label.position_y+64), text='Your score:', font_name="Sans Serif", font_size=32, label_color=Color.white, anchor_horizontal=Anchor.CENTER, anchor_vertical=Anchor.TOP)

    current_screen = UIScreen.MAIN_MENU

    def __init__(self, screen_type: UIScreen) -> None:
        self.EnableScreen(screen_type)

    def EnableScreen(self, screen_type: UIScreen):
        self.canvas.Clear()
        self.current_screen = screen_type
        match screen_type:
            case UIScreen.MAIN_MENU:
                self.canvas.ExtendElements([self.menu_label, self.menu_casual_btn, self.menu_normal_btn, self.menu_hard_btn])
            case UIScreen.GAME_RUN:
                self.canvas.ExtendElements([self.game_run_timer_label, self.game_run_score_label, self.game_run_ammo_label])
            case UIScreen.GAME_END:
                self.canvas.ExtendElements([self.game_end_label, self.game_end_status_label, self.game_end_score_label])
    
    # Cursor Colliding
    def _CursorIsColliding(self, gui_rect: GUIRect) -> bool:
        return gui_rect.rect.collidepoint(MouseCursor.GetMousePos())
    def _CursorIsClicking(self, gui_rect: GUIRect) -> bool:
        return MouseCursor.input_LMB and self._CursorIsColliding(gui_rect)
    def _UpdateCursorClick(self, gui_rect: GUIRect, on_click_method, args):
        if self._CursorIsClicking(gui_rect):
            gui_rect.OnClick(on_click_method, args)
        else:
            gui_rect.OnClickOver()

    # Update Methods
    def Update(self):
        match self.current_screen:
            case UIScreen.MAIN_MENU:
                self._UpdateCursorClick(self.menu_casual_btn.rect, on_click_method=game_observer.GameStart, args=(GameMode.CASUAL))
                self._UpdateCursorClick(self.menu_normal_btn.rect, on_click_method=game_observer.GameStart, args=(GameMode.NORMAL))
                self._UpdateCursorClick(self.menu_hard_btn.rect, on_click_method=game_observer.GameStart, args=(GameMode.HARDCORE))
            case UIScreen.GAME_RUN:
                self.game_run_timer_label.SetLabel(f'TIME REMAINING: {player.time_remaining}')
                self.game_run_score_label.SetLabel(f'KILLS: {player.score}')
                self.game_run_ammo_label.SetLabel(f'AMMO: {player.ammo}')
            case UIScreen.GAME_END:
                self.game_end_status_label.SetLabel(f'{game_observer.game_over_status}')
                self.game_end_score_label.SetLabel(f'Your score: {player.score}')

    def RenderingUpdate(self):
        self.canvas.Draw(screen)
        MouseCursor.Draw()

# Game Objects
class GameObject(object):
    name = 'New Game Object'
    position_x = 0
    position_y = 0

    def __init__(self, name: str, position: tuple[int, int]) -> None:
        self.SetName(name)
        self.SetPosition(position[0], position[1])
    
    def __del__(self):
        self.OnDestroy()

    def SetName(self, name: str):
        self.name = name

    def SetPosition(self, x: int, y: int):
        self.position_x = x
        self.position_y = y
        self.OnPositionChanged()
    
    def MoveInDirection(self, x: int, y: int, velocity: float = 1.0):
        self.SetPosition(self.position_x + (x * velocity * Time.GetRealSecond()), self.position_y + (y * velocity * Time.GetRealSecond()))
    
    def OnPositionChanged(self):
        print(f'{self.name}: position has changed to {self.position_x} {self.position_y}.')
    
    def OnDestroy(self):
        print(f'{self.name}: has destroyed.')

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
    frame_wait_for = 0
    def PlayAnimation(self):
        self.frame_wait_for -= Time.GetRealSecond()
        if self.frame_wait_for <= 0:
            self.frame_wait_for = 0.1
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

# Victim Game Object Behaviour
class Victim(SpritedGameObject):
    _current_point_id = 0
    _current_movement_point: GameObject = GameObject
    _preloaded_movement_points: GameObject = []

    _dir_x = 0
    _dir_y = 0

    _movement_speed = 200 # Pixels Per Second

    _at_gunpoint = False
    _is_dead = False

    @property
    def is_dead(self):
        return self._is_dead

    def __init__(self, name: str, position: tuple[int, int], sprite_pack: set[str], scale: float) -> None:
        super().__init__(name, position, sprite_pack, scale)
    
    # Path Creating
    def HasNoMovementPoints(self) -> bool:
        return self._preloaded_movement_points.__len__() < 1   
    def SetMovementPoints(self, points: list[GameObject]):
        self._preloaded_movement_points = points
        self.SetNextMovementPoint(random=self.HasNoMovementPoints())  
    def SetNextMovementPoint(self, random: bool = False):
        if random or self.HasNoMovementPoints():
            self._current_movement_point = self.GetRandomMovementPoint()
        else:
            self._current_point_id += 1
            if (self._current_point_id >= self._preloaded_movement_points.__len__()):
                self._current_point_id = 0
            self._current_movement_point = self._preloaded_movement_points[self._current_point_id]    
    def GetRandomMovementPoint(self) -> GameObject:
        rand_x = randint(0, scr_width-self.sprite.get_width())
        rand_y = randint(0, scr_height-self.sprite.get_height())
        return GameObject('random_point', (rand_x, rand_y))

    # Movement Engine
    def GetDirectionToPoint(self, movement_point: GameObject) -> tuple[int, int]:
        return [clamp(movement_point.position_x - self.position_x, -1, 1), clamp(movement_point.position_y - self.position_y, -1, 1)]
    def PointIsReached(self, movement_point: GameObject) -> bool:
        self_pos = (self.position_x, self.position_y)
        point_pos = (movement_point.position_x, movement_point.position_y)
        return sqr_magnitude(self_pos, point_pos) < 64
    def MoveToCurrentPoint(self):
        direction = self.GetDirectionToPoint(self._current_movement_point)
        self._dir_x = direction[0]
        self._dir_y = direction[1]
        self.MoveInDirection(self._dir_x, self._dir_y, velocity=self._movement_speed)
        if self.PointIsReached(self._current_movement_point):
            self.SetNextMovementPoint()

    # Cursor Colliding
    def CursorIsColliding(self) -> bool:
        return self.collider.collidepoint(MouseCursor.GetMousePos())
    # ? Don't like this updating method
    def UpdateCursorColliding(self):
        if self._at_gunpoint and not self.CursorIsColliding():
            MouseCursor.OnHover(False)
        self._at_gunpoint = self.CursorIsColliding()
        if self._at_gunpoint:
            MouseCursor.OnHover(True)
            self.SetNextMovementPoint(random=True)
    # ? It's better to subscribe on MouseCursor.OnClick method -> if self._at_gunpoint: kill(). But idk how for now.
    def UpdateCursorClick(self):
        if player.is_shooting and self._at_gunpoint:
            self.Kill()

    # Lifecycle End
    def Kill(self):
        self._is_dead = True      
        self.OnKill()

    def OnKill(self):
        MouseCursor.OnHover(False)
        player.AddScore(1)

    # Update Methods
    def PhysicsUpdate(self):
        if not self._is_dead:
            self.MoveToCurrentPoint()
            self.UpdateCursorColliding()
            self.UpdateCursorClick()
    
    def RenderingUpdate(self):
        if not self._is_dead:
            self.FlipSprite(look_left=self._dir_x < 0)
            self.Draw()
            if self._dir_x != 0 or self._dir_y != 0:
                self.PlayAnimation()
            else:
                self.SetDefaultSprite()

# Game God and each frame updating Objects.
# ? Still don't know how to make Event System here.
class GameMode(Enum):
    CASUAL = 1,
    NORMAL = 2,
    HARDCORE = 3

class GameObserver():
    _game_mode = GameMode.NORMAL

    @property
    def game_started(self):
        return self._game_started

    @property
    def game_is_over(self):
        return self._game_is_over
    
    @property
    def game_over_status(self):
        return self._game_over_status
    
    def __init__(self) -> None:
        self._SetToDefault()

    def _SetToDefault(self):
        self._game_started = False
        self._game_is_over = False
        self._game_over_status = ""        

    def GameStart(self, game_mode: GameMode):
        gameUI.EnableScreen(screen_type=UIScreen.GAME_RUN)
        match game_mode:
            case GameMode.CASUAL:
                player.__init__(ammo=60, timer=60)
                main_victim_group.__init__(victim_count=15)
            case GameMode.NORMAL:
                player.__init__(ammo=30, timer=30)
                main_victim_group.__init__(victim_count=20)
            case GameMode.HARDCORE:
                player.__init__(ammo=25, timer=15)
                main_victim_group.__init__(victim_count=25)     
        self._game_mode = game_mode
        self._game_started = True

    def BackToMenu(self):
        self._SetToDefault()
        player.Stop()
        main_victim_group.ClearAll()
        gameUI.EnableScreen(UIScreen.MAIN_MENU)

    def Restart(self):
        self._SetToDefault()
        self.GameStart(self._game_mode)

    def GameOver(self, status: str):
        self._game_is_over = True
        self._game_over_status = status
        self.OnGameOver()

    def OnGameOver(self):
        player.Stop()
        gameUI.EnableScreen(UIScreen.GAME_END)

    # Update Methods
    def Update(self):
        if self._game_started and not self._game_is_over:
            if player.TimeIsOut:
                self.GameOver("Time's up, baby!")
            elif player.HasKilledAll:
                self.GameOver("You've killed 'em all!")
            elif not player.HasAmmo:
                self.GameOver("You've lost all your ammo...")

class Player():

    @property
    def score(self):
        return self._score
    
    @property
    def ammo(self):
        return self._ammo

    @property
    def time_remaining(self):
        return self._time_remaining

    @property
    def is_shooting(self):
        return self._is_shooting
    
    def __init__(self, ammo: int, timer: int) -> None:
        self._score = 0
        self._ammo = ammo
        self._time_remaining = timer
        self._timer = timer
        self._is_shooting = False

    def Stop(self):
        self._is_shooting = False

    def AddScore(self, value: int):
        self._score += value
    
    def AddAmmo(self, value: int):
        self._ammo += value
    
    @property
    def HasAmmo(self) -> bool:
        return self._ammo > 0
    
    @property
    def TimeIsOut(self) -> bool:
        return self._time_remaining <= 0
    
    @property
    def HasKilledAll(self) -> bool:
        return main_victim_group.victims.__len__() < 1    
    
    _fire_delay = 0
    def _TryShot(self):
        self._is_shooting = False
        if self.HasAmmo:
            self._fire_delay -= Time.GetRealSecond()
            if self._fire_delay <= 0:
                self._is_shooting = True
                self._fire_delay = 0.1
                self.AddAmmo(-1)

    def _PlayTimerRun(self):
        self._timer -= Time.GetRealSecond()
        self._time_remaining = int(self._timer)
   
    # Update Methods
    def PhysicsUpdate(self):
        if not game_observer.game_is_over:
            self._PlayTimerRun()
            if MouseCursor.input_LMB:
                self._TryShot()
    
    def RenderingUpdate(self):
        pass

class VictimGroup():
    victims = []

    def __init__(self, victim_count: int) -> None:
        self.Create(victim_count)

    def Create(self, victim_count: int):
        self.ClearAll()
        for i in range(0, victim_count):
            self.Add(f'Giga_{i}')
    
    # Collection Methods
    def Add(self, name: str, start_pos: tuple[int, int] = (scr_width/2, scr_height/2), scale: float = 0.5):
        new_victim = Victim(name, start_pos, ['\Player_0.svg', '\Player_1.svg', '\Player_2.svg'], scale)
        new_victim.SetMovementPoints(self.GetMovementPoints())
        self.victims.append(new_victim)
    def Remove(self, obj: Victim):
        self.victims.remove(obj)
        del obj
    def ClearAll(self):
        self.victims = []

    # TODO: RANDOM START POS
    # Generating a random spawn point
    def GetRandomSpawnPoint(self, victim: Victim) -> tuple[int, int]:
        rand_x = randint(0, scr_width-self.sprite.get_width())
        rand_y = randint(0, scr_height-self.sprite.get_height())
        return [rand_x, rand_y]
    # Choosing a random or preloaded movement path
    def GetMovementPoints(self) -> list[GameObject]:
        i = randint(0, 20)
        if i < 2:
            return [GameObject('point_1', (scr_width, 30)), GameObject('point_2', (0, 30))]
        elif i < 6:
            return [GameObject('point_1', (50, 100)), GameObject('point_2', (600, 300)), GameObject('point_2', (900, 20))]
        return []
    
    # Update Methods
    def PhysicsUpdate(self):
        for victim in self.victims:
            if victim.is_dead:
                self.Remove(victim)
            else:
                victim.PhysicsUpdate() 
    
    def RenderingUpdate(self):
        for victim in self.victims:
            victim.RenderingUpdate()

# Physics Queue
def PhysicsUpdate():
    game_observer.Update()
    gameUI.Update()
    if game_observer.game_started:
        main_victim_group.PhysicsUpdate()
        player.PhysicsUpdate()

# Rendering Queue
def RenderingUpdate():
    main_victim_group.RenderingUpdate()
    player.RenderingUpdate()
    gameUI.RenderingUpdate()

# Main Game-loop
game_observer = GameObserver()
gameUI = UI(screen_type=UIScreen.MAIN_MENU)
player = Player(ammo=0, timer=60)
main_victim_group = VictimGroup(victim_count=0)

def main(run: bool):
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                MouseCursor.OnClick(down=event.button == 1)
            if event.type == pygame.MOUSEBUTTONUP:
                MouseCursor.OnClick(down=not event.button == 1)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and game_observer.game_started:
                    game_observer.Restart()
                if event.key == pygame.K_ESCAPE:
                    game_observer.BackToMenu()
        
        ClearScreen()
        
        PhysicsUpdate()
        RenderingUpdate()
        
        UpdateScreen()

main(run=True)