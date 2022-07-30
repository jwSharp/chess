import pygame
import math

from config import *
#from piece import *

class Board:
    def __init__(self):
        self.current_turn = 1
        self.selected_block = None

    def input(self, event):
        mouse_pos = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.selected_block = self.select_block(mouse_pos)
        elif event.type == pygame.MOUSEBUTTONUP:
            pass
        elif pygame.mouse.get_pressed()[0]:
            pass

    def draw(self, screen, panel: pygame.Rect):
        self.board_panel = panel
        sq_width = panel.width/8
        sq_height = panel.height/8
        for i in range(0,8):
            for j in range(0,8):
                sq_left = i * sq_width + panel.x
                sq_top = j * sq_height + panel.y
                sq = pygame.Rect(sq_left, sq_top, sq_width, sq_height)
                
                if (i + j) % 2 == 0:
                    pygame.draw.rect(screen, TAN, sq)
                else:
                    pygame.draw.rect(screen, BROWN, sq)
                if (i, j) == self.selected_block:
                    pygame.draw.rect(screen, LIGHT_GREEN, sq, 6)
                    
    def select_block(self, pos: tuple):
        x, y = list(pos)
        x, y = self._get_grid_position(x, y)
        print(x, y)
        if (x >= 0 and x <= 7) and (y >= 0) and (y <= 7):
            return (x, y)
        return None

    def _get_grid_position(self, x: float, y: float):
        block_size = self.board_panel.width / 8
        x = int((x - self.board_panel.x) / block_size)
        y = int((y - self.board_panel.y) / block_size)
        return x, y