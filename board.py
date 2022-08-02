import pygame
import sys
from config import *
from accessories import *
from player import *
from board import *
from piece import *

class Board:
    def __init__(self):
        self.current_turn = 1
        #self.surface = surface
        #self.selected_block = None

    def input(self, event):
        mouse_pos = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            pass
        elif event.type == pygame.MOUSEBUTTONUP:
            pass
        elif pygame.mouse.get_pressed()[0]:
            pass

    def draw(self,screen):
        screen_center = (screen.get_width()/2, screen.get_height()/2)
        board_width = (screen.get_width() * .6)
        board_height = (screen.get_height())
        playing_field_width = board_width/1.2
        playing_field_height = board_height/1.2
        board = pygame.Rect(0, 0, board_width,board_height)
        playing_field = pygame.Rect(0, 0, playing_field_width,playing_field_height)
        playing_field.center = board.center = screen_center

        pygame.draw.rect(screen, BROWN, board)
        pygame.draw.rect(screen, OAK, playing_field)

        self.draw_squares(screen,playing_field)
        self.add_texture(screen,board, board_width, board_height)
        self.add_border(screen,playing_field)

    def draw_squares(self,screen, playing_field):
        sq_width, sq_height = playing_field.width/8, playing_field.height/8
        square = pygame.Rect(0,0,sq_width, sq_height)
        square.topleft = playing_field.topleft
        for i in range (0,8):
            if i % 2 == 0:
                for j in range (0,4):
                    pygame.draw.rect(screen, OAK, square)
                    square.left += sq_width
                    pygame.draw.rect(screen, BROWN, square)
                    square.left += sq_width
                    #if (i, j) == self.selected_block:
                        #pygame.draw.rect(screen, LIGHT_GREEN, sq, 6)
            else:
                for j in range (0,4):
                    pygame.draw.rect(screen, BROWN, square)
                    square.left += sq_width
                    pygame.draw.rect(screen, OAK, square)
                    square.left += sq_width
                    #if (i, j) == self.selected_block:
                        #pygame.draw.rect(screen, LIGHT_GREEN, sq, 6)
            square.left = playing_field.left
            square.bottom += sq_height
        self.add_letters(screen, square, playing_field)
        self.add_numbers(screen, square, playing_field)

    def add_letters(self, screen, square, playing_field):
        letters = ["A", "B", "C", "D", "E", "F", "G", "H"]
        label_font = pygame.font.SysFont('arial', 36, bold = True)

        for i in range (0,8):
            label_text = label_font.render(letters[i], True, DARK_OAK)
            label_rect = label_text.get_rect()
            label_rect.centerx = square.centerx
            label_rect.centery = playing_field.top *.5
            screen.blit(label_text, label_rect)
            square.left += square.width
        square.topleft = playing_field.topleft

    def add_numbers(self, screen,square, playing_field):
        label_font = pygame.font.SysFont('arial', 40, bold=True)

        for i in range (1,9):
            number_text = label_font.render(str(i), True, DARK_OAK)
            number_rect = number_text.get_rect()
            number_rect.centerx = playing_field.left - playing_field.width * 0.05
            number_rect.centery = square.centery
            screen.blit(number_text, number_rect)
            square.top += square.height

    def add_texture(self, screen,board, board_width, board_height):
        texture = pygame.image.load("Assets\Textures\wood_grain.png")
        texture = pygame.transform.scale(texture, (board_width, board_height))
        texture_rect = texture.get_rect()
        texture.set_alpha(80)
        texture_rect.topleft = board.topleft
        screen.blit(texture, texture_rect)

    def add_border(self, screen, playing_field):
        border = pygame.Rect(0,0, playing_field.width, playing_field.height)
        border.top = playing_field.top-2
        border.left = playing_field.left - 2
        pygame.draw.rect(screen, GOLD, border,4)
        shadow = pygame.Rect(0,0, playing_field.width, playing_field.height)
        shadow.top = border.top + 2
        shadow.left = border.left + 2
        pygame.draw.rect(screen, GOLD_SHADOW, shadow, 2)
        highlight = pygame.Rect(0,0, playing_field.width, playing_field.height)
        highlight.top = playing_field.top - 3
        highlight.left = playing_field.left - 3
        pygame.draw.rect(self.surface, WHITE, highlight, 1)
