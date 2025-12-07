from screeninfo import get_monitors
from pytmx import load_pygame
import pygame

SCREEN_TITLE = "Dragon Killer"
GETINFO = get_monitors()[0]

SCREEN_WIDTH = int(GETINFO.width)
SCREEN_HEIGHT = int(GETINFO.height)

TARGET_SCREENWIDTH = 580
TARGET_SCREENHEIGHT = TARGET_SCREENWIDTH // 2

PYGAME_WINDOW = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), vsync=1)
PYGAME_SURFACE = pygame.Surface((TARGET_SCREENWIDTH, TARGET_SCREENHEIGHT))

MAP = load_pygame("tiles/WorldTMX/World.tmx")

RUN_GAME = True

MAPWIDTH = MAP.width * MAP.tilewidth
MAPHEIGHT = MAP.height * MAP.tileheight

FIXED_WORLD_WIDTH = MAPWIDTH // 2 + 177
FIXED_WORLD_HEIGHT = MAPHEIGHT // 3 - 128

#state
camera_x = 0
camera_y = 0