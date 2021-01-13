import sys
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame


# Functions
def load_data(name, **kwargs):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл '{fullname}' не найден")
        sys.exit()
    ext = fullname.split(".")[-1].lower()
    file = None
    if ext == "png" or ext == "jpg" or ext == "gif":  # Load image
        file = pygame.image.load(fullname)
    elif ext == "ttf":  # Load font
        try:
            file = pygame.font.Font(name, kwargs.get("size"))
        except FileNotFoundError:
            file = pygame.font.Font(fullname, kwargs.get("size"))
    return file  # If file is None, then file extension is unknown


bullet_animation = pygame.image.load

WINDOW_SIZE = WIDTH, HEIGHT = 1600, 900

PLAYER_SPEED = 250
MOB_SPEED = 200

PLAYER_HP = 200
MOB_HP = 300

PLAYER_IMAGE = pygame.image.load('data/player.png')
PLAYER_IMAGE.set_colorkey((255, 255, 255))
MOB_IMAGE = pygame.image.load('data/player.png')
MOB_IMAGE.set_colorkey((255, 255, 255))

INVENTORY_PROP = {'gun': {'type of shooting': 'line', 'range': 200, 'damage': 20,
                          'animation': {'start': bullet_animation("data/bullet.png"),
                                        'end': [bullet_animation("data/bullet_end.png"),
                                                bullet_animation("data/bullet_end.png"),
                                                bullet_animation("data/bullet_end.png"),
                                                bullet_animation("data/bullet_end.png")]},
                          'cooldown': 500},
                  'sword': {'type of shooting': 'circle', 'range': 50, 'damage': 50, 'cooldown': 500}}

LEVELS = ['demoLevel.tmx']

TILE_SIZE = 32
FPS = 60
MAP_WIDTH = 50
MAP_HEIGHT = 50
MAP_SIZE = (MAP_WIDTH * TILE_SIZE, MAP_HEIGHT * TILE_SIZE)
