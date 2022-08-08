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
def RefreshScreen():
    screen.fill(Color.black)

# Game Assets
player_sprite = pygame.Surface((10, 40))
player_sprite.fill(Color.white)
player_collider = pygame.Rect(scr_width/2-player_sprite.get_width()/2, scr_height/2-player_sprite.get_height()/2, player_sprite.get_width(), player_sprite.get_height())

# Game World
ground_level = scr_height * 0.9

def DrawGround() -> pygame.draw:
    return pygame.draw.rect(surface=screen, color=Color.white, rect=(0, ground_level, scr_width, ground_level))

def DrawPlayer() -> screen.blit:
    return screen.blit(player_sprite, player_collider)

input_LMB = False
def DrawCursor(radius: float = 16, color: tuple[int, int, int] = Color.white) -> pygame.draw:
    return pygame.draw.circle(surface=screen, color=color, center=pygame.mouse.get_pos(), radius=radius)

# Character Movement
input_dir = 0
input_jump = 0
input_shift = 1.0

def Move(rect: pygame.Rect, x: int, y: int):
    rect.x += x
    rect.y += y

def isNotGrounded(rect: pygame.Rect) -> bool:
    return rect.bottom < scr_height * 0.9

def ApplyMovementTo(rect: pygame.Rect, dir: int, shift: float = 1.0):
    Move(rect, dir * 4 * shift, 0)

def ApplyJumpTo(rect: pygame.Rect, dir: int, shift: float = 1.0):
    if isNotGrounded(rect) == False:
        Move(rect, 0, -input_jump * 40 * shift)

def ApplyGravityTo(rect: pygame.Rect):
    if isNotGrounded(rect):
        Move(rect, 0, 1)

while True:
    RefreshScreen()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            input_LMB = event.button == 1
        if event.type == pygame.MOUSEBUTTONUP:
            input_LMB = not event.button == 1
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                input_dir = 1
                if event.mod & pygame.KMOD_SHIFT:
                    input_shift = 1.3
                else:
                    input_shift = 1.0
            if event.key == pygame.K_LEFT:
                input_dir = -1
                if event.mod & pygame.KMOD_SHIFT:
                    input_shift = 1.3
                else:
                    input_shift = 1.0
            if event.key == pygame.K_UP:
                input_jump = 1
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                input_dir = 0
            if event.key == pygame.K_UP:
                input_jump = 0

    ApplyMovementTo(player_collider, input_dir, input_shift)
    ApplyJumpTo(player_collider, input_jump)
    ApplyGravityTo(player_collider)

    DrawGround()
    DrawPlayer()
    DrawCursor()

    if input_LMB:
        DrawCursor(radius=14, color=Color.black)

    pygame.display.update()
    pygame.time.delay(10)