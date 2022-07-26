import pygame, sys
from pygame.locals import *

# Set up some global stuff
WIDTH = 1280
HEIGHT = 800
BLACK = ('#000000')
WHITE = ('#FFFFFF')
BROWN = ('#724E2F')
GOLD_HIGHLIGHT = ('#F6F456')
GOLD = ('#E6CC39')
GOLD_SHADOW = ('#918A20')
TAN = ('#C9AD71')
GREY = ('#99958D')

def make_chess_GUI():
    # set up pygame
    pygame.init()

    # Set up the window
    windowSurface = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Retro|Modern Chess")
    windowSurface.fill(BLACK)

    # Set up the game box, board, and player details
    make_gamebox(windowSurface)
    add_board(windowSurface, True)
    add_player_text(windowSurface, True)
    add_menu_buttons(windowSurface)

    # Draw the window onto the screen
    pygame.display.update()

    # Run the game loop
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

def make_gamebox(windowSurface):
    #Primary lines
    pygame.draw.rect(windowSurface, GOLD, ((0,0), (WIDTH/5,HEIGHT)),10)
    pygame.draw.rect(windowSurface, GOLD, ((WIDTH/1.25, 0), (WIDTH,HEIGHT)),10)
    pygame.draw.rect(windowSurface, GOLD, ((0,0), (WIDTH, HEIGHT)), 10)
    #Shadows
    pygame.draw.line(windowSurface, GOLD_SHADOW, (8,8), (WIDTH-8,8), 4)
    pygame.draw.line(windowSurface, GOLD_SHADOW, (8,8), (8, HEIGHT-8), 4)
    pygame.draw.line(windowSurface, GOLD_SHADOW, (WIDTH-3, 3), (WIDTH-3, HEIGHT-5), 4)
    pygame.draw.line(windowSurface, GOLD_SHADOW, (0, HEIGHT-3), (WIDTH, HEIGHT-3), 4)
    pygame.draw.line(windowSurface, GOLD_SHADOW, (WIDTH/5.05, 8), (WIDTH/5.05,HEIGHT-8),4)
    pygame.draw.line(windowSurface, GOLD_SHADOW, (WIDTH/1.24, 8), (WIDTH/1.24, HEIGHT-8), 4)

    ###### Add captured pieces rects
    pygame.draw.rect(windowSurface, GOLD, ((20, HEIGHT / 4.5), (WIDTH / 5 - 40, HEIGHT / 2)), 5)
    pygame.draw.rect(windowSurface, GOLD, ((WIDTH / 1.225, HEIGHT / 4.5), (WIDTH / 5 - 40, HEIGHT / 2)), 5)

    ##### Add rect for clocks
    pygame.draw.rect(windowSurface, GOLD, ((20, HEIGHT / 9), (WIDTH / 5 - 40, HEIGHT / 11)), 5)
    pygame.draw.rect(windowSurface, GOLD, ((WIDTH / 1.225, HEIGHT / 9), (WIDTH / 5 - 40, HEIGHT / 11)), 5)

    # Set up the fonts
    pygame.font.init()
    print(pygame.font.get_fonts())
    overthinkerFont = pygame.font.SysFont('ocr', 64)

    #### Add overthinker text
    retroText = overthinkerFont.render("Retro", True, GOLD, BLACK)
    modernText = overthinkerFont.render("Modern", True, GOLD, BLACK)
    retroTextRect, modernTextRect = retroText.get_rect(), modernText.get_rect()
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

def add_menu_buttons(windowSurface):
    # make buttons
    buttonFont = pygame.font.SysFont('elephant', 26)
    menuText = buttonFont.render("Menu", True, BLACK)
    menuTextRect = pygame.draw.rect(windowSurface, GREY, ((WIDTH/1.19, HEIGHT/1.3), (150,40)))

    exitText = buttonFont.render("Exit", True, BLACK)
    exitTextRect = pygame.draw.rect(windowSurface, GREY, ((WIDTH/1.19, HEIGHT/1.15), (150, 40)))

    windowSurface.blit(menuText, menuTextRect)
    windowSurface.blit(exitText, exitTextRect)

def add_player_text(windowSurface, is2p: bool):
    # Set up the player/player1 text
    playersFont = pygame.font.SysFont('brushscript', 62)
    # TODO if p2 == human then...
    p1Text = playersFont.render("Player", True, GOLD, BLACK)
    p1TextRect = p1Text.get_rect()
    p1TextRect.centerx = WIDTH/10
    p1TextRect.centery = 49
    # Set up the AI/player2 text
    # TODO if p2 == human then...
    p2Text = playersFont.render("CPU", True, GOLD, BLACK)
    p2TextRect = p2Text.get_rect()
    p2TextRect.centerx = WIDTH/1.1
    p2TextRect.centery = 49
    #Draw the texts' background rectangles
    pygame.draw.rect(windowSurface, BLACK, ((10,10), (20,20)),3)
    #Draw the text onto the  surface
    windowSurface.blit(p1Text, p1TextRect)
    windowSurface.blit(p2Text, p2TextRect)

def add_board(windowSurface, isChess: bool):
    start_x = WIDTH/5
    start_y = 11
    sq_width = 96
    sq_height = 97.5
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

make_chess_GUI()
