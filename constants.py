from pathlib import Path
import pygame

## Pygame ##
SCREEN = pygame.display.set_mode((600, 600))

## Paths ## 
#! CHANGE ASSETS_PATH TO THE PATH OF THE ASSETS FOLDER
FILE_PATH = Path(__file__).parent.absolute()
ASSETS_PATH = str(FILE_PATH.parent.absolute().parent.absolute() / 'assets') + '/' # add .parent.absolute() after file_path to go back at directory

## Colors ##
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
LIGHT_GREEN = (116, 252, 152, 230)
RED = (244, 66, 66)