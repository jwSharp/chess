import pygame
from constants import *
from game import *


def make_chess_GUI():
    # Set up the game box, board, and player details
    make_gamebox(SCREEN)
    add_player_text(SCREEN, True)
    add_menu_buttons(SCREEN)
    draw_clocks()


def draw_clocks():
    ##### Add rect for clocks
    rect1 = pygame.draw.rect(
        SCREEN, GOLD, ((20, HEIGHT / 9), (WIDTH / 5 - 40, HEIGHT / 11)), 5
    )
    rect2 = pygame.draw.rect(
        SCREEN, GOLD, ((WIDTH / 1.225, HEIGHT / 9), (WIDTH / 5 - 40, HEIGHT / 11)), 5
    )
    ##### TODO: Add timer text for clocks


def make_gamebox(SCREEN):
    # Primary lines
    pygame.draw.rect(SCREEN, GOLD, ((0, 0), (WIDTH / 5, HEIGHT)), 10)
    pygame.draw.rect(SCREEN, GOLD, ((WIDTH / 1.25, 0), (WIDTH, HEIGHT)), 10)
    pygame.draw.rect(SCREEN, GOLD, ((0, 0), (WIDTH, HEIGHT)), 10)

    # Shadows
    pygame.draw.line(SCREEN, GOLD_SHADOW, (8, 8), (WIDTH - 8, 8), 4)
    pygame.draw.line(SCREEN, GOLD_SHADOW, (8, 8), (8, HEIGHT - 8), 4)
    pygame.draw.line(SCREEN, GOLD_SHADOW, (WIDTH - 3, 3), (WIDTH - 3, HEIGHT - 5), 4)
    pygame.draw.line(SCREEN, GOLD_SHADOW, (0, HEIGHT - 3), (WIDTH, HEIGHT - 3), 4)
    pygame.draw.line(
        SCREEN, GOLD_SHADOW, (WIDTH / 5.05, 8), (WIDTH / 5.05, HEIGHT - 8), 4
    )
    pygame.draw.line(
        SCREEN, GOLD_SHADOW, (WIDTH / 1.24, 8), (WIDTH / 1.24, HEIGHT - 8), 4
    )

    # Set up the fonts
    pygame.font.init()
    overthinkerFont = pygame.font.SysFont("ocr", 64)

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
    SCREEN.blit(retroText, retroTextRect)
    SCREEN.blit(modernText, modernTextRect)
    SCREEN.blit(chessText, chessTextRect)

    ###### Add captured pieces rects
    captured_box_1 = pygame.draw.rect(
        SCREEN, GOLD, ((20, HEIGHT / 4.5), (WIDTH / 5 - 40, HEIGHT / 2)), 5
    )
    captured_box_2 = pygame.draw.rect(
        SCREEN, GOLD, ((WIDTH / 1.225, HEIGHT / 4.5), (WIDTH / 5 - 40, HEIGHT / 2)), 5
    )

    captured_count1, captured_count2 = 0, 0
    for i, piece in enumerate(chess.captured_pieces):
        image = pygame.transform.smoothscale(
            piece.sprite, (piece.sprite.get_width() * 2, piece.sprite.get_height() * 2)
        )
        if piece.turn == 0:
            x = captured_box_1.center[0] - image.get_width() / 2
            y = (captured_box_1.top) + captured_count1 * image.get_height() / (
                captured_count1 + 1
            )
            captured_count1 += 1
        else:
            x = captured_box_2.center[0] - image.get_width() / 2
            y = (captured_box_2.top) + captured_count2 * image.get_height() / (
                captured_count2 + 1
            )
            captured_count2 += 1
        SCREEN.blit(image, (x, y))


def add_menu_buttons(SCREEN):
    # make buttons
    buttonFont = pygame.font.SysFont("elephant", 26)
    menuTextRect = pygame.Rect((WIDTH / 1.19, HEIGHT / 1.3), (150, 40))
    exitTextRect = pygame.Rect((WIDTH / 1.19, HEIGHT / 1.2), (150, 40))

    on_button_press(menuTextRect, "Menu", buttonFont, GOLD, GOLD_HIGHLIGHT)
    on_button_press(exitTextRect, "Exit", buttonFont, TAN, BROWN)


def add_player_text(SCREEN, is2p: bool):
    # Set up the player/player1 text
    playersFont = pygame.font.SysFont("brushscript", 62)
    # TODO if p2 == human then...
    text_display = "Player 1" if is2p else "Player"
    p1Text = playersFont.render(
        text_display, True, GOLD if chess.current_turn == 0 else DARK_RED, BLACK
    )
    p1TextRect = p1Text.get_rect()
    p1TextRect.centerx = WIDTH / 10
    p1TextRect.centery = 49
    # Set up the AI/player2 text
    # TODO if p2 == human then...
    text_display = "Player 2" if is2p else "CPU"
    p2Text = playersFont.render(
        text_display, True, GOLD if chess.current_turn == 1 else DARK_RED, BLACK
    )
    p2TextRect = p2Text.get_rect()
    p2TextRect.centerx = WIDTH / 1.1
    p2TextRect.centery = 49

    # Draw the texts' background rectangles
    pygame.draw.rect(SCREEN, BLACK, ((10, 10), (20, 20)), 3)
    # Draw the text onto the  surface
    SCREEN.blit(p1Text, p1TextRect)
    SCREEN.blit(p2Text, p2TextRect)


def on_button_press(
    button_rect: pygame.Rect, button_str: str, font, color: tuple, hover_color: tuple
):  # call_func: callable, *args):
    # pygame.draw.rect(SCREEN, color, button_rect, 2, 10)
    if button_rect.collidepoint(pygame.mouse.get_pos()):
        pygame.draw.rect(SCREEN, hover_color, button_rect, 2, 10)
        button_text = font.render(button_str, True, hover_color)
        # if pygame.mouse.get_pressed()[0]:
        #     call_func(*args)
    else:
        pygame.draw.rect(SCREEN, color, button_rect, 2, 10)
        button_text = font.render(button_str, True, color)
    SCREEN.blit(
        button_text,
        (
            button_rect.x + button_rect.width / 2 - button_text.get_width() / 2,
            button_rect.y + button_rect.height / 2 - button_text.get_height() / 2,
        ),
    )
