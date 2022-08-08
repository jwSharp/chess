import pygame

from config import *
from accessory import *
from player import *
from piece import *


class Board:
    def __init__(self, manager, view):
        self.manager = manager
        self.view = view
        
        self.current_turn = 1
        self.selected_block = None

    def input(self, event):
        mouse_pos = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            pass
        elif event.type == pygame.MOUSEBUTTONUP:
            pass
        elif pygame.mouse.get_pressed()[0]:
            pass

    def draw(self, screen):
        '''
        The draw function takes the user's desired perspective and draws the respective board.
        '''
        if self.view == "flat":
            board = self.draw_flat(screen)[0]
            playing_field = self.draw_flat(screen)[1]
        elif self.view == "iso":
            board = self.draw_iso(screen)[0]
            playing_field = self.draw_iso(screen)[1]

        pygame.draw.rect(screen, BROWN, board)
        pygame.draw.rect(screen, OAK, playing_field)

        self.draw_squares(screen, playing_field)
        self.add_texture(screen, board)
        self.add_border(screen, playing_field)

    def draw_flat(self, screen):
        screen_center = (screen.get_width() / 2, screen.get_height() / 2)
        board = pygame.Rect(0, 0, screen.get_width() * .6, screen.get_width() * .6)
        playing_field = pygame.Rect(0, 0, board.width/1.2,board.height/1.2)
        playing_field.center = board.center = screen_center

        return board, playing_field

    def draw_iso(self, screen):
        screen_topcenter = (screen.get_width() / 2, screen.get_height() / 2.1)
        board = pygame.Rect(0, 0, screen.get_width() * .6, screen.get_height() * .80)
        playing_field = pygame.Rect(0, 0, board.width / 1.2, board.height / 1.2)
        playing_field.center = board.center = screen_topcenter
        board_front = pygame.Rect(0,0,board.width, board.height * .05)
        board_front.midtop = board.midbottom
        pygame.draw.rect(screen, DARK_OAK, board_front)

        return board, playing_field

    def draw_squares(self, screen, playing_field):
        sq_width, sq_height = playing_field.width/8, playing_field.height/8
        square = pygame.Rect(0, 0, sq_width, sq_height)
        square.topleft = playing_field.topleft
        for i in range (0, 8):
            if i % 2 == 0:
                for j in range (0, 4):
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
        label_font = pygame.font.SysFont('arial', screen.get_width() // 36, bold = True)

        for i in range (0, 8):
            label_text = label_font.render(letters[i], True, DARK_OAK)
            label_rect = label_text.get_rect()
            label_rect.centerx = square.centerx
            if self.view == "flat":
                label_rect.centery = playing_field.top *.5
            elif self.view == "iso":
                label_rect.centery = playing_field.top * .75
            screen.blit(label_text, label_rect)
            square.left += square.width
        square.topleft = playing_field.topleft

    def add_numbers(self, screen, square, playing_field):
        label_font = pygame.font.SysFont('arial', screen.get_width() // 36, bold=True)

        for i in range (1, 9):
            number_text = label_font.render(str(i), True, DARK_OAK)
            number_rect = number_text.get_rect()
            number_rect.centerx = playing_field.left - playing_field.width * 0.05
            number_rect.centery = square.centery
            screen.blit(number_text, number_rect)
            square.top += square.height

    def add_texture(self, screen, board):
        texture = pygame.image.load(TEXTURE_PATH + "wood_grain.png")
        texture = pygame.transform.scale(texture, (board.width, board.height))
        texture_rect = texture.get_rect()
        texture.set_alpha(80)
        texture_rect.topleft = board.topleft
        screen.blit(texture, texture_rect)

    def add_border(self, screen, playing_field):
        border = pygame.Rect(0, 0, playing_field.width, playing_field.height)
        border.top = playing_field.top-2
        border.left = playing_field.left - 2
        pygame.draw.rect(screen, GOLD, border, 4)
        
        shadow = pygame.Rect(0, 0, playing_field.width, playing_field.height)
        shadow.top = border.top + 2
        shadow.left = border.left + 2
        pygame.draw.rect(screen, GOLD_SHADOW, shadow, 2)
        
        highlight = pygame.Rect(0, 0, playing_field.width, playing_field.height)
        highlight.top = playing_field.top - 3
        highlight.left = playing_field.left - 3
        pygame.draw.rect(screen, WHITE, highlight, 1)
