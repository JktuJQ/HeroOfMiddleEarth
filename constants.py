import pygame

bullet_animation = pygame.image.load

WIDTH = 1600
HEIGHT = 900

PLAYER_SPEED = 250
MOB_SPEED = 200

PLAYER_HP = 200
MOB_HP = 300

PLAYER_IMAGE = pygame.image.load('block/Player/Mag/Stay/mag_stay.png')
PLAYER_IMAGE.set_colorkey((255, 255, 255))
MOB_IMAGE = pygame.image.load('test_player.png')
MOB_IMAGE.set_colorkey((255, 255, 255))

INVENTORY_PROP = {'gun': {'type of shooting': 'line', 'range': 200, 'damage': 20,
                          'animation': bullet_animation("test_bullet.png"),
                          'cooldown': 500},
                  'sword': {'type of shooting': 'circle', 'range': 50, 'damage': 50, 'cooldown': 500},
                  'bow': {'type of shooting': 'line', 'range': 250,
                          'damage': 40, 'cooldown': 1000,
                          'animation': bullet_animation("test_bullet.png")}}

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
                    }}


TILE_SIZE = 32
FPS = 60
MAP_WIDTH = 100
MAP_HEIGHT = 100
WINDOW_SIZE = (WIDTH, HEIGHT)
MAP_SIZE = (MAP_WIDTH * TILE_SIZE, MAP_HEIGHT * TILE_SIZE)
