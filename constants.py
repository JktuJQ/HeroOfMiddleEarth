import pygame
import sys
import os

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"


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

WIDTH = 1600
HEIGHT = 900

PLAYER_SPEED = 250
MOB_SPEED = 200

PLAYER_HP = 200
MOB_HP = 1

PLAYER_IMAGE = pygame.image.load('block/Player/Mag/Stay/mag_stay.png')
PLAYER_IMAGE.set_colorkey((255, 255, 255))
MOB_IMAGE = pygame.image.load('data/player.png')

LEVELS = ['level_0.tmx', 'level_1.tmx', 'level_2.tmx']

INVENTORY_PROP = {'gun': {'type of shooting': 'line', 'range': 200, 'damage': 20,
                          'animation': bullet_animation("data/images/bullet.png"),
                          'cooldown': 500},
                  'sword': {'type of shooting': 'line', 'range': 50, 'damage': 50, 'cooldown': 500,
                            'animation': bullet_animation("data/images/sword.png")},
                  'bow': {'type of shooting': 'line', 'range': 250,
                          'damage': 40, 'cooldown': 1000,
                          'animation': bullet_animation("data/images/arrow.png")},
                  'zombie_ball': {'type of shooting': 'line', 'range': 100,
                                  'damage': 40, 'cooldown': 1000,
                                  'animation': bullet_animation("data/images/zombie_ball.png")}
                  }

RIGHT_HERO = [bullet_animation("block/Player/Mag/Right/mag_right_s.png"),
              bullet_animation("block/Player/Mag/Right/mag_right_r.png"),
              bullet_animation("block/Player/Mag/Right/mag_right_s.png"),
              bullet_animation("block/Player/Mag/Right/mag_right_l.png")]
LEFT_HERO = [bullet_animation("block/Player/Mag/Left/mag_left_s.png"),
             bullet_animation("block/Player/Mag/Left/mag_left_r.png"),
             bullet_animation("block/Player/Mag/Left/mag_left_s.png"),
             bullet_animation("block/Player/Mag/Left/mag_left_l.png")]
DOWN_HERO = [bullet_animation("block/Player/Mag/Down/mag_down_s.png"),
             bullet_animation("block/Player/Mag/Down/mag_down_r.png"),
             bullet_animation("block/Player/Mag/Down/mag_down_s.png"),
             bullet_animation("block/Player/Mag/Down/mag_down_l.png")]
TOP_HERO = [bullet_animation("block/Player/Mag/Top/mag_top_s.png"),
            bullet_animation("block/Player/Mag/Top/mag_top_r.png"),
            bullet_animation("block/Player/Mag/Top/mag_top_s.png"),
            bullet_animation("block/Player/Mag/Top/mag_top_l.png")]

MOBS = {'archer': {'type_gun': 'bow', 'hp': 50, 'speed': 130,
                   'animation_r': [bullet_animation("block/Player/Mobs/Archer/archer_stay_r.png"),
                                   bullet_animation("block/Player/Mobs/Archer/archer_run_r.png")],
                   'animation_l': [bullet_animation("block/Player/Mobs/Archer/archer_stay_l.png"),
                                   bullet_animation("block/Player/Mobs/Archer/archer_run_l.png")],
                   },
        'mag': {'type_gun': 'gun', 'hp': 75, 'speed': 150,
                'animation_r': [bullet_animation("block/Player/Mobs/Mag/m_stay_r.png"),
                                bullet_animation("block/Player/Mobs/Mag/m_run_r.png")],
                'animation_l': [bullet_animation("block/Player/Mobs/Mag/m_stay_l.png"),
                                bullet_animation("block/Player/Mobs/Mag/m_run_l.png")],
                },
        'warrior': {'type_gun': 'sword', 'hp': 100, 'speed': 200,
                    'animation_r': [bullet_animation("block/Player/Mobs/Warrior/warrior_stay_r.png"),
                                    bullet_animation("block/Player/Mobs/Warrior/warrior_run_r.png")],
                    'animation_l': [bullet_animation("block/Player/Mobs/Warrior/warrior_stay_l.png"),
                                    bullet_animation("block/Player/Mobs/Warrior/warrior_run_l.png")]
                    },
        'zombie': {'type_gun': 'zombie_ball', 'hp': 100, 'speed': 100,
                    'animation_r': [bullet_animation("block/Player/Mobs/Zombie/zombie_stay_r.png"),
                                    bullet_animation("block/Player/Mobs/Zombie/zombie_run_r.png")],
                    'animation_l': [bullet_animation("block/Player/Mobs/Zombie/zombie_stay_l.png"),
                                    bullet_animation("block/Player/Mobs/Zombie/zombie_run_r.png")]
                    }}

TILE_SIZE = 32
FPS = 60
MAP_WIDTH = 100
MAP_HEIGHT = 58
WINDOW_SIZE = (WIDTH, HEIGHT)
MAP_SIZE = (MAP_WIDTH * TILE_SIZE, MAP_HEIGHT * TILE_SIZE)