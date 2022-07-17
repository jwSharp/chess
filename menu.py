"""
Cheat Menu Screen.  Will need updating to include Scenes/ States
"""

# With a placeholder for game
# To use multiple screens in pygame, use multiple functions with their own game loops (While True)
# To give illusion of multiple screens, fill screen with black and display over that

import pygame
import sys

from button import Button

pygame.init()

SCREEN = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Main Menu")

BG = pygame.image.load("assets/brainColorful2.jpg")


def get_font(size):  # Returns Press-Start 2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)


def play():  # Play Screen...
    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("black")

        PLAY_TEXT = get_font(45).render("This is the PLAY screen.", True, "white")
        PLAY_RECT = PLAY_TEXT.get_rect(center=(640, 160))
        SCREEN.blit(PLAY_TEXT, PLAY_RECT)

        PLAY_BACK = Button(image=None, pos=(640, 560),
                           text_input="BACK", font=get_font(75), base_color="white", hovering_color="orange")
        PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        PLAY_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    main_menu()

        pygame.display.update()


def credits():
    while True:
        CREDITS_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("#b68f40")

        CREDITS_TEXT= get_font(45).render("This game is presented by: ", True, "black")
        CREDITS_RECT = CREDITS_TEXT.get_rect(center=(655, 100))

        CT_SHADOW= get_font(45).render("This game is presented by: ", True, "white")
        CTS_RECT = CT_SHADOW.get_rect(center=(658, 102))

        CREDIT_NAME1 = get_font(40).render("Ashley Butela", True, "black")
        CN1_RECT = CREDIT_NAME1.get_rect(center=(640, 220))

        CREDIT_NAME2 = get_font(40).render("Amy Ciuffoletti", True, "black")
        CN2_RECT = CREDIT_NAME2.get_rect(center=(640, 295))

        CREDIT_NAME3 = get_font(40).render("Mehmet Ozen", True, "black")
        CN3_RECT = CREDIT_NAME2.get_rect(center=(700, 370))

        CREDIT_NAME4 = get_font(40).render("Jacob Sharp", True, "black")
        CN4_RECT = CREDIT_NAME2.get_rect(center=(700, 445))

        CREDIT_NAME5 = get_font(40).render("Nabeyou Tadessa", True, "black")
        CN5_RECT = CREDIT_NAME2.get_rect(center=(640, 520))

        CREDITS_BACK = Button(image=None, pos=(640, 640),
                              text_input="BACK", font=get_font(50), base_color="black", hovering_color="white")

        CTB_SHADOW = get_font(50).render("BACK", True, "white")
        CTBS_RECT = CTB_SHADOW.get_rect(center=(642, 642))

        SCREEN.blit(CT_SHADOW, CTS_RECT)
        SCREEN.blit(CREDITS_TEXT, CREDITS_RECT)
        SCREEN.blit(CREDIT_NAME1, CN1_RECT)
        SCREEN.blit(CREDIT_NAME2, CN2_RECT)
        SCREEN.blit(CREDIT_NAME3, CN3_RECT)
        SCREEN.blit(CREDIT_NAME4, CN4_RECT)
        SCREEN.blit(CREDIT_NAME5, CN5_RECT)
        SCREEN.blit(CTB_SHADOW, CTBS_RECT)
        CREDITS_BACK.changeColor(CREDITS_MOUSE_POS)
        CREDITS_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if CREDITS_BACK.checkForInput(CREDITS_MOUSE_POS):
                    options()

        pygame.display.update()


def options():  # Options Screen
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("white")

        OPTIONS_TEXT = get_font(100).render("OPTIONS", True, "#b68f40")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 160))

        OPTIONS_SHADOW = get_font(100).render("OPTIONS", True, "black")
        OPS_RECT = OPTIONS_SHADOW.get_rect(center=(644, 164))

        SCREEN.blit(OPTIONS_SHADOW, OPS_RECT)
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)

        OPTIONS_CREDITS = Button(image=None, pos=(640, 400),
                                 text_input="CREDITS", font=get_font(75), base_color="#b68f40", hovering_color="black")

        OPC_SHADOW = get_font(75).render("CREDITS", True, "black")
        OCS_RECT = OPC_SHADOW.get_rect(center=(644, 404))

        SCREEN.blit(OPC_SHADOW, OCS_RECT)

        OPTIONS_BACK = Button(image=None, pos=(640, 560),
                              text_input="BACK", font=get_font(75), base_color="#B68F40", hovering_color="black")

        OPB_SHADOW = get_font(75).render("BACK", True, "black")
        OBS_RECT = OPB_SHADOW.get_rect(center=(644, 564))

        SCREEN.blit(OPB_SHADOW, OBS_RECT)

        OPTIONS_CREDITS.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_CREDITS.update(SCREEN)
        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_CREDITS.checkForInput(OPTIONS_MOUSE_POS):
                    credits()
                elif OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()

        pygame.display.update()


def main_menu():  # Main Menu Screen...
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        MENU_SHADOW = get_font(100).render("MAIN MENU", True, "#ffffff" )
        MENU_RECT1 = MENU_SHADOW.get_rect(center=(644, 104))

        PLAY_BUTTON = Button(None, pos=(640, 275),
                             text_input="PLAY", font=get_font(75), base_color="#b68f40", hovering_color="white")
        PLAY_SHADOW = get_font(75).render("PLAY", True, "#ffffff")
        PS_RECT = PLAY_SHADOW.get_rect(center=(644, 279))

        OPTIONS_BUTTON = Button(None, pos=(640, 440),
                                text_input="OPTIONS", font=get_font(75), base_color="#b68f40", hovering_color="white")
        OPTIONS_SHADOW = get_font(75).render("OPTIONS", True, "#ffffff")
        OP_RECT = OPTIONS_SHADOW.get_rect(center=(644, 444))

        QUIT_BUTTON = Button(None, pos=(640, 600),
                             text_input="QUIT", font=get_font(75), base_color="#b68f40", hovering_color="white")
        QUIT_SHADOW = get_font(75).render("QUIT", True, "#ffffff")
        QT_RECT = QUIT_SHADOW.get_rect(center=(644, 604))

        SCREEN.blit(MENU_SHADOW, MENU_RECT1)
        SCREEN.blit(MENU_TEXT, MENU_RECT)
        SCREEN.blit(PLAY_SHADOW, PS_RECT)
        SCREEN.blit(OPTIONS_SHADOW, OP_RECT)
        SCREEN.blit(QUIT_SHADOW, QT_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


main_menu()
