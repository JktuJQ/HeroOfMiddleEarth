import pygame


def bullet_animation(name):
    return pygame.image.load(name)


WIDTH = 1200
HEIGHT = 700

PLAYER_SPEED = 250
MOB_SPEED = 200

PLAYER_IMAGE = pygame.image.load('data/test_player.png')
PLAYER_IMAGE.set_colorkey((255, 255, 255))
MOB_IMAGE = pygame.image.load('data/test_player.png')
MOB_IMAGE.set_colorkey((255, 255, 255))

INVENTORY_PROP = {'gun': [{'type of shooting': 'line'},
                          {'range': 200},
                          {'damage': 20},
                          {'animation': [{'start': bullet_animation("test_bullet.png")},
                                         {'end': [bullet_animation("test_bullet_end.png"), bullet_animation("test_bullet_end.png"), bullet_animation("test_bullet_end.png"), bullet_animation("test_bullet_end.png")]}]}],
                  'sword': [{'type of shooting': 'circle'},
                            {'range': 50},
                            {'damage': 50}]}

TILE_SIZE = 32
FPS = 60
MAP_WIDTH = 50
MAP_HEIGHT = 50
WINDOW_SIZE = (WIDTH, HEIGHT)
MAP_SIZE = (MAP_WIDTH * TILE_SIZE, MAP_HEIGHT * TILE_SIZE)