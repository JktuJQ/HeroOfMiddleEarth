import sys
import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hidden"
import pygame


WIDTH = 1200
HEIGHT = 700

PLAYER_SPEED = 250
MOB_SPEED = 200

PLAYER_IMAGE = pygame.image.load('data/test_player.png')
PLAYER_IMAGE.set_colorkey((255, 255, 255))
MOB_IMAGE = pygame.image.load('data/test_player.png')
MOB_IMAGE.set_colorkey((255, 255, 255))

INVENTORY_PROP = {'gun': ['line', 200, 20], 'sword': ['circle', 50, 50]}

TILE_SIZE = 32
FPS = 60

MAP_WIDTH = 50
MAP_HEIGHT = 50
WINDOW_SIZE = (WIDTH, HEIGHT)
MAP_SIZE = (MAP_WIDTH * TILE_SIZE, MAP_HEIGHT * TILE_SIZE)