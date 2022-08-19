import pygame
from pathlib import Path


##########
# Pygame #
##########
pygame.init() #TODO Move to main ideally
ASPECT_RATIO = (16, 10) #TODO Make more streamlined
HEIGHT = 800
WIDTH = 1280


def PIXEL_TO_ASPECT(width, height, aspect = ASPECT_RATIO):
    ''''''
    if width < height:
        width = abs(round(height / aspect[1])) * aspect[0] 
    else:
        height = abs(round(width / aspect[0])) * aspect[1]
    return width, height

def FIXED_SCALE(width, height, limit_min: tuple, limit_max: tuple):
    ''''''
    if width < limit_min[0]:
        width = limit_min[0]
    if height < limit_min[1]:
        height = limit_min[1]
    if width > limit_max[0]:
        width = limit_max[0]
    if height > limit_max[1]:
        height = limit_max[1]
    return width, height

#########
# Paths #
#########
FILE_PATH = Path(__file__).parent.absolute()
ASSETS_PATH = str(FILE_PATH / "Assets") + "/"
IMAGES_PATH = ASSETS_PATH + "Images/"
TEXTURE_PATH = ASSETS_PATH + "Textures/"
#TODO Redo structure ex. Pieces/ViewType/Black
BLACK_PIECES_PATH = ASSETS_PATH + "Pieces/Black/Top/"
WHITE_PIECES_PATH = ASSETS_PATH + "Pieces/White/Top/"
FONTS_PATH = ASSETS_PATH + "Fonts" + "/"

#########
# Fonts #
#########

CUSTOM_FONTS = { 'Regular' : FONTS_PATH + "regular.ttf", 'Timer' : FONTS_PATH + "alarm_clock.ttf", 'elephant' : FONTS_PATH + "elephant.ttf", 'ocr' : FONTS_PATH + "ocr.ttf"}
SYS_FONTS = pygame.font.get_fonts()
def GET_FONT(name: str, size: int):
    '''Returns the pygame font of a particular size.'''
    if name in SYS_FONTS:
        return pygame.font.SysFont(name, size)
    return pygame.font.Font(CUSTOM_FONTS[name], size)

##########
# Colors #
##########
BLACK = (0, 0, 0) #TODO Change all to hexcode.
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
LIGHT_GREEN = (116, 252, 152, 50)
RED = (244, 66, 66)
DARK_RED = ('#880015')
LIGHT_BROWN = ('#b97a57')
BROWN = ('#693F19')
GOLD_HIGHLIGHT = ('#F6F456')
GOLD = ('#FFD700')
GOLD_SHADOW = ('#91792F')
GREY = ('#99958D')
OAK = ('#DBA16A')
DARK_OAK = ('#341f0c')
ORANGE = ('#b68f40')
PURPLE = ('#cc5ced')

##########
# Images #
##########
BACKGROUND = pygame.image.load(IMAGES_PATH + "brain_colorful.jpg")
