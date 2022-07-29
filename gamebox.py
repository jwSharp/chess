import pygame, sys
from pygame.locals import *
from config import *

class Gamebox:
    def __init__(self, manager, time):
        self.manager = manager




        self.timer_1 = Timer(time)
        self.timer_2 = Timer(time)


    def update(self, event):
        pass


    def draw(self, screen):
        # Frame
        pygame.draw.rect(screen, GOLD, ((0, 0), (WIDTH / 5, HEIGHT)), 10)
        pygame.draw.rect(screen, GOLD, ((WIDTH / 1.25, 0), (WIDTH / 5, HEIGHT)), 10)
        pygame.draw.rect(screen, GOLD, ((0, 0), (WIDTH, HEIGHT)), 10)

        #shadows
        pygame.draw.line(screen, GOLD_SHADOW, (8, 8), (WIDTH - 8, 8), 4)
        pygame.draw.line(screen, GOLD_SHADOW, (8, 8), (8, HEIGHT - 8), 4)
        pygame.draw.line(screen, GOLD_SHADOW, (WIDTH - 3, 3), (WIDTH - 3, HEIGHT - 5), 4)
        pygame.draw.line(screen, GOLD_SHADOW, (0, HEIGHT - 3), (WIDTH, HEIGHT - 3), 4)
        pygame.draw.line(screen, GOLD_SHADOW, (WIDTH / 5.05, 8), (WIDTH / 5.05, HEIGHT - 8), 4)
        pygame.draw.line(screen, GOLD_SHADOW, (WIDTH / 1.24, 8), (WIDTH / 1.24, HEIGHT - 8), 4)

        #captured rects
        pygame.draw.rect(screen, GOLD, ((20, HEIGHT / 4.5), (WIDTH / 5 - 40, HEIGHT / 2)), 5)
        pygame.draw.rect(screen, GOLD, ((WIDTH / 1.225, HEIGHT / 4.5), (WIDTH / 5 - 40, HEIGHT / 2)), 5)


        # timer rects
        pygame.draw.rect(screen, GOLD, ((20, HEIGHT / 9), (WIDTH / 5 - 40, HEIGHT / 11)), 5)
        pygame.draw.rect(screen, GOLD, ((WIDTH / 1.225, HEIGHT / 9), (WIDTH / 5 - 40, HEIGHT / 11)), 5)

        # logo text
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
        screen.blit(retroText, retroTextRect)
        screen.blit(modernText, modernTextRect)
        screen.blit(chessText, chessTextRect)

        # menu buttons
        buttonFont = pygame.font.SysFont('elephant', 26)
        menuText = buttonFont.render("Menu", True, BLACK)
        menuTextRect = pygame.draw.rect(self.surface, GREY, ((WIDTH / 1.19, HEIGHT / 1.3), (150, 40)))

        exitText = buttonFont.render("Exit", True, BLACK)
        exitTextRect = pygame.draw.rect(self.surface, GREY, ((WIDTH / 1.19, HEIGHT / 1.15), (150, 40)))

        self.surface.blit(menuText, menuTextRect)
        self.surface.blit(exitText, exitTextRect)

        # player text
        # TODO if p2 == human then...
        players_font = GET_FONT("brushscript", 62)
        
        p1Text = playersFont.render("Player 1", True, GOLD, BLACK)
        p1TextRect = p1Text.get_rect()
        p1TextRect.centerx = WIDTH / 10
        p1TextRect.centery = 49

        self.surface.blit(p1Text, p1TextRect)

        p2Text = playersFont.render("Player 2", True, GOLD, BLACK)
        p2TextRect = p2Text.get_rect()
        p2TextRect.centerx = WIDTH / 1.1
        p2TextRect.centery = 49
        self.surface.blit(p2Text, p2TextRect)