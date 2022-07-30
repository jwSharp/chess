import pygame
import math

from config import *
#from piece import *

class Board:
    def __init__(self):
        self.current_turn = 1

    def input(self, event):
        mouse_pos = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            pass
        elif event.type == pygame.MOUSEBUTTONUP:
            pass
        elif pygame.mouse.get_pressed()[0]:
            pass

    def draw(self, screen):
        start_x = WIDTH/5
        start_y = 11
        sq_width = 96
        sq_height = 98
        for i in range(1,9):
            if i % 2 == 1:
                for j in range(0,4):
                    pygame.draw.rect(screen,TAN,((start_x,start_y),(sq_width,sq_height)))
                    start_x+=sq_width
                    pygame.draw.rect(screen,BROWN,((start_x,start_y), (sq_width,sq_height)))
                    start_x+=sq_width
            else:
                for j in range(0, 4):
                    pygame.draw.rect(screen, BROWN, ((start_x, start_y), (sq_width, sq_height)))
                    start_x += sq_width
                    pygame.draw.rect(screen, TAN, ((start_x, start_y), (sq_width, sq_height)))
                    start_x += sq_width
            start_x = 256
            start_y += sq_height
        
        #for piece in self.pieces:
        #    piece.draw(self, screen)