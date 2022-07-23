from pathlib import Path
import pygame

## Pygame ##
WIDTH = 1280
HEIGHT = 800
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
CLOCK = pygame.time.Clock()
pygame.init()

## Paths ## 
#! CHANGE ASSETS_PATH TO THE PATH OF THE ASSETS FOLDER
FILE_PATH = Path(__file__).parent.absolute()
ASSETS_PATH = str(FILE_PATH / 'assets') + '/' # add .parent.absolute() after file_path to go back at directory
FONTS_PATH = str(FILE_PATH / 'fonts') + '/'

## Fonts ##
TIMER_F = pygame.font.Font(FONTS_PATH + 'alarm_clock.ttf', 40)

## Colors ##
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
LIGHT_GREEN = (116, 252, 152, 230)
RED = (244, 66, 66)
DARK_RED = ('#880015')
LIGHT_BROWN = ('#b97a57')
BROWN = ('#724E2F')
GOLD_HIGHLIGHT = ('#F6F456')
GOLD = ('#E6CC39')
GOLD_SHADOW = ('#918A20')
TAN = ('#C9AD71')
GREY = ('#99958D')
