##
# Constants used in Alien Invasion
#

import pygame
from pygame import mixer

# Colors
BLACK = (0, 0, 0)
DARK_GREEN = (0, 155, 0)
LIGHT_GRAY = (230, 230, 230)
LIGHT_GREEN = (0, 255, 0)
PURPLE = (154, 0, 226)
RED = (255, 0, 0)
WHITE = (255, 255, 255)


# Font related constants
GAME_OVER_TEXT = 'Game Over!'
GAME_TITLE = 'Alien Invasion!'
LARGE_FONT = 100
SMALL_FONT = 48
START_GAME_TEXT = 'Press any Key to Start'
TITLE_FONT = 'freesansbold.ttf'


# Images
ALIEN_IMG_1 = pygame.image.load('images/alien1a.bmp')
ALIEN_IMG_2 = pygame.image.load('images/alien1b.bmp')
SHIP_IMG = pygame.image.load('images/shipa.bmp')


# Offsets
# For offsetting displayed elements slightly to shift them away from other elements or the screen edge
ELEMENT_EDGE_OFFSET = 10  # Additive
ELEMENT_SPACING = 2  # Multiplier
SCREEN_EDGE_OFFSET = 20  # Additive


# Screen related constants
SCREEN_HEIGHT = 720
SCREEN_WIDTH = 1280


# Time related consants (milliseconds)
ALIEN_IMG_PANEL_DURATION = 500
# For blinking "Press Any Key to Start" message
BLINK_DURATION = 500
DEMO_GAMEPLAY_TIMER = 1000
EXPLOSION_DURATION = 125
