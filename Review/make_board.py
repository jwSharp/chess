import pygame, sys
from pygame.locals import *

pygame.init()
pygame.font.init()
playersFont = pygame.font.SysFont('brushscript', 62)
windowSurface = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Retro|Modern Chess")
background = pygame.Surface(windowSurface.get_size())
background = background.convert()

def make_chess_GUI():
    # Run the game loop
    while True:
    # draw background - black
        background.fill(BLACK)
        # event listeners
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        # Draw objects
        make_board(windowSurface, True)
        make_gamebox(windowSurface)
        add_player1_text(windowSurface, True)
        add_player2_text(windowSurface, True)
        add_menu_buttons(windowSurface)

        # Update window
        pygame.display.update()

''' The make_board function creates the chess playting field.'''

def make_board(windowSurface, isChess: bool):
    start_x = WIDTH/5
    start_y = 11
    sq_width = 96
    sq_height = 98
    for i in range(1,9):
        if i % 2 == 1:
            for j in range(0,4):
                pygame.draw.rect(windowSurface,TAN,((start_x,start_y),(sq_width,sq_height)))
                start_x+=sq_width
                pygame.draw.rect(windowSurface,BROWN,((start_x,start_y), (sq_width,sq_height)))
                start_x+=sq_width
        else:
            for j in range(0, 4):
                pygame.draw.rect(windowSurface, BROWN, ((start_x, start_y), (sq_width, sq_height)))
                start_x += sq_width
                pygame.draw.rect(windowSurface, TAN, ((start_x, start_y), (sq_width, sq_height)))
                start_x += sq_width
        start_x=256
        start_y+=sq_height

''' The make_gamebox function calls other functions to create a functional field around the chessboard, 
with decorative elements, placeholders for timers, placeholders for captured pieces, and a logo'''

def make_gamebox(windowSurface):
    add_gamebox_frame(windowSurface)
    add_gamebox_shadows(windowSurface)
    add_captured_rects(windowSurface)
    add_timer_rects(windowSurface)
    add_logo_text(windowSurface)

''' The add_gamebox_frame function adds the decorative elements to the gamebox.'''

def add_gamebox_frame(windowSurface):
    pygame.draw.rect(windowSurface, GOLD, ((0,0), (WIDTH/5,HEIGHT)),10)
    pygame.draw.rect(windowSurface, GOLD, ((WIDTH/1.25, 0), (WIDTH/5,HEIGHT)),10)
    pygame.draw.rect(windowSurface, GOLD, ((0,0), (WIDTH, HEIGHT)), 10)

''' The add_gamebox_shadows function adds shadows to the decorative elements of the gamebox.'''

def add_gamebox_shadows(windowSurface):
    pygame.draw.line(windowSurface, GOLD_SHADOW, (8,8), (WIDTH-8,8), 4)
    pygame.draw.line(windowSurface, GOLD_SHADOW, (8,8), (8, HEIGHT-8), 4)
    pygame.draw.line(windowSurface, GOLD_SHADOW, (WIDTH-3, 3), (WIDTH-3, HEIGHT-5), 4)
    pygame.draw.line(windowSurface, GOLD_SHADOW, (0, HEIGHT-3), (WIDTH, HEIGHT-3), 4)
    pygame.draw.line(windowSurface, GOLD_SHADOW, (WIDTH/5.05, 8), (WIDTH/5.05,HEIGHT-8),4)
    pygame.draw.line(windowSurface, GOLD_SHADOW, (WIDTH/1.24, 8), (WIDTH/1.24, HEIGHT-8), 4)

''' The add_captured_rects function adds blank rectangles to hold captured pieces.'''

def add_captured_rects(windowSurface):
    pygame.draw.rect(windowSurface, GOLD, ((20, HEIGHT / 4.5), (WIDTH / 5 - 40, HEIGHT / 2)), 5)
    pygame.draw.rect(windowSurface, GOLD, ((WIDTH / 1.225, HEIGHT / 4.5), (WIDTH / 5 - 40, HEIGHT / 2)), 5)

''' The add_timer_rects function adds blank rectangles to hold the player timers.'''

def add_timer_rects(windowSurface):
    pygame.draw.rect(windowSurface, GOLD, ((20, HEIGHT / 9), (WIDTH / 5 - 40, HEIGHT / 11)), 5)
    pygame.draw.rect(windowSurface, GOLD, ((WIDTH / 1.225, HEIGHT / 9), (WIDTH / 5 - 40, HEIGHT / 11)), 5)

''' The add_logo_text function adds the Retro|Modern Chess text in the lower left corner of the gamebox.'''

def add_logo_text(windowSurface):
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
    windowSurface.blit(retroText, retroTextRect)
    windowSurface.blit(modernText, modernTextRect)
    windowSurface.blit(chessText, chessTextRect)

''' The add_menu_buttons function adds buttons to the lower right corner of the gamebox.'''

def add_menu_buttons(windowSurface):
    # make buttons
    buttonFont = pygame.font.SysFont('elephant', 26)
    menuText = buttonFont.render("Menu", True, BLACK)
    menuTextRect = pygame.draw.rect(windowSurface, GREY, ((WIDTH/1.19, HEIGHT/1.3), (150,40)))

    exitText = buttonFont.render("Exit", True, BLACK)
    exitTextRect = pygame.draw.rect(windowSurface, GREY, ((WIDTH/1.19, HEIGHT/1.15), (150, 40)))

    windowSurface.blit(menuText, menuTextRect)
    windowSurface.blit(exitText, exitTextRect)

''' The add_player1_text function adds text, either "Player" or "Player 1", to the upper left corner of the gamebox.'''

def add_player1_text(windowSurface, is2p: bool):
    # TODO if p2 == human then...
    p1Text = playersFont.render("Player 1", True, GOLD, BLACK)
    p1TextRect = p1Text.get_rect()
    p1TextRect.centerx = WIDTH/10
    p1TextRect.centery = 49

    windowSurface.blit(p1Text, p1TextRect)

''' The add_player2_text function adds text, either "CPU" or "Player 2", to the upper right corner of the gamebox.'''

def add_player2_text(windowSurface, is2p: bool):
    # TODO if p2 == human then...
    p2Text = playersFont.render("Player 2", True, GOLD, BLACK)
    p2TextRect = p2Text.get_rect()
    p2TextRect.centerx = WIDTH / 1.1
    p2TextRect.centery = 49
    windowSurface.blit(p2Text, p2TextRect)

make_chess_GUI()
