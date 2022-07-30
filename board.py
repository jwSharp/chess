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

    def draw(self, screen, panel: pygame.Rect):
        sq_width = panel.width/8
        sq_height = panel.height/8
        for i in range(0,8):
            for j in range(0,8):
                x_pos = i * sq_width + panel.x
                y_pos = j * sq_height + panel.y
                r = pygame.Rect(x_pos, y_pos, sq_width, sq_height)
                if (i + j) % 2 == 0:
                    pygame.draw.rect(screen, TAN, r)
                else:
                    pygame.draw.rect(screen, BROWN, r)
        
        #for piece in self.pieces:
        #    piece.draw(self, screen)