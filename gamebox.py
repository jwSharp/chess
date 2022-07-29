import pygame, sys
from pygame.locals import *
from config import *

class Gamebox:
    def __init__(self, surface):
        self.surface = surface

        self.boarders = 

    def draw(self):
        # Frame
        pygame.draw.rect(self.surface, GOLD, ((0, 0), (WIDTH / 5, HEIGHT)), 10)
        pygame.draw.rect(self.surface, GOLD, ((WIDTH / 1.25, 0), (WIDTH / 5, HEIGHT)), 10)
        pygame.draw.rect(self.surface, GOLD, ((0, 0), (WIDTH, HEIGHT)), 10)

        self.add_shadows()
        self.add_captured_rects()
        self.add_timer_rects()
        self.add_logo_text()
        self.add_menu_buttons()
        self.add_player1_text()
        self.add_player2_text()

    ''' The add_gamebox_shadows function adds shadows to the decorative elements of the gamebox.'''

    def add_shadows(self):
        pygame.draw.line(self.surface, GOLD_SHADOW, (8, 8), (WIDTH - 8, 8), 4)
        pygame.draw.line(self.surface, GOLD_SHADOW, (8, 8), (8, HEIGHT - 8), 4)
        pygame.draw.line(self.surface, GOLD_SHADOW, (WIDTH - 3, 3), (WIDTH - 3, HEIGHT - 5), 4)
        pygame.draw.line(self.surface, GOLD_SHADOW, (0, HEIGHT - 3), (WIDTH, HEIGHT - 3), 4)
        pygame.draw.line(self.surface, GOLD_SHADOW, (WIDTH / 5.05, 8), (WIDTH / 5.05, HEIGHT - 8), 4)
        pygame.draw.line(self.surface, GOLD_SHADOW, (WIDTH / 1.24, 8), (WIDTH / 1.24, HEIGHT - 8), 4)

    ''' The add_captured_rects function adds blank rectangles to hold captured pieces.'''

    def add_captured_rects(self):
        pygame.draw.rect(self.surface, GOLD, ((20, HEIGHT / 4.5), (WIDTH / 5 - 40, HEIGHT / 2)), 5)
        pygame.draw.rect(self.surface, GOLD, ((WIDTH / 1.225, HEIGHT / 4.5), (WIDTH / 5 - 40, HEIGHT / 2)), 5)

    ''' The add_timer_rects function adds blank rectangles to hold the player timers.'''

    def add_timer_rects(self):
        pygame.draw.rect(self.surface, GOLD, ((20, HEIGHT / 9), (WIDTH / 5 - 40, HEIGHT / 11)), 5)
        pygame.draw.rect(self.surface, GOLD, ((WIDTH / 1.225, HEIGHT / 9), (WIDTH / 5 - 40, HEIGHT / 11)), 5)

    ''' The add_logo_text function adds the Retro|Modern Chess text in the lower left corner of the gamebox.'''

    def add_logo_text(self):
        overthinkerFont = pygame.font.SysFont('ocr', 64)
        retroText = overthinkerFont.render("Retro", True, GOLD, BLACK)
        modernText = overthinkerFont.render("Modern", True, GOLD, BLACK)
        retroTextRect = retroText.get_rect()
        modernTextRect = modernText.get_rect()
        retroTextRect.centerx = WIDTH / 10
        modernTextRect.centerx = WIDTH / 10
        retroTextRect.centery = HEIGHT / 1.25
        modernTextRect.centery = HEIGHT / 1.16
        chessText = overthinkerFont.render("Chess", True, GOLD, BLACK)
        chessTextRect = chessText.get_rect()
        chessTextRect.centerx = WIDTH / 10
        chessTextRect.centery = HEIGHT / 1.08
        self.surface.blit(retroText, retroTextRect)
        self.surface.blit(modernText, modernTextRect)
        self.surface.blit(chessText, chessTextRect)

    ''' The add_menu_buttons function adds buttons to the lower right corner of the gamebox.'''

    def add_menu_buttons(self):
        buttonFont = pygame.font.SysFont('elephant', 26)
        menuText = buttonFont.render("Menu", True, BLACK)
        menuTextRect = pygame.draw.rect(self.surface, GREY, ((WIDTH / 1.19, HEIGHT / 1.3), (150, 40)))

        exitText = buttonFont.render("Exit", True, BLACK)
        exitTextRect = pygame.draw.rect(self.surface, GREY, ((WIDTH / 1.19, HEIGHT / 1.15), (150, 40)))

        self.surface.blit(menuText, menuTextRect)
        self.surface.blit(exitText, exitTextRect)

    ''' The add_player1_text function adds text, either "Player" or "Player 1", to the upper left corner of the gamebox.'''

    def add_player1_text(self):
        # TODO if p2 == human then...
        playersFont = pygame.font.SysFont('brushscript', 62)
        p1Text = playersFont.render("Player 1", True, GOLD, BLACK)
        p1TextRect = p1Text.get_rect()
        p1TextRect.centerx = WIDTH / 10
        p1TextRect.centery = 49

        self.surface.blit(p1Text, p1TextRect)

    ''' The add_player2_text function adds text, either "CPU" or "Player 2", to the upper right corner of the gamebox.'''

    def add_player2_text(self):
        # TODO if p2 == human then...
        playersFont = pygame.font.SysFont('brushscript', 62)
        p2Text = playersFont.render("Player 2", True, GOLD, BLACK)
        p2TextRect = p2Text.get_rect()
        p2TextRect.centerx = WIDTH / 1.1
        p2TextRect.centery = 49
        self.surface.blit(p2Text, p2TextRect)

    def update(self):
        pass
