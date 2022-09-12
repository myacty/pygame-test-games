
# ? My custom Color Pallete.

from random import randint

white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
grey = (60, 60, 60)
black = (0, 0, 0)

def GetColor(r: int, g: int, b: int) -> tuple[int, int, int]:
    return (r, g, b)

def GetRandomColor() -> tuple[int, int, int]:
    r = randint(0, 255)
    g = randint(0, 255)
    b = randint(0, 255)
    return (r, g, b)