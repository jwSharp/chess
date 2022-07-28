# Updated/Created scene.py which includes Scene Parent Class and sub classes
# MainMenuScene(Scene), Options(Scene), Play(Scene)* PLACEHOLDER, Credits(Scene),
# and SceneManager


import pygame
import sys
from button import Button
from config import *


############
# Abstract #
############


class Scene:
    def __init__(self):
        pass

    def input(self, events):
        pass

    def draw(self):
        pass

    def onEnter(self):
        pass

    def onExit(self):
        pass


class MainMenuScene(Scene):
    def __init__(self, manager):
        pygame.display.set_caption("Main Menu")
        self.manager = manager

        self.text = GET_FONT('Regular', 100).render("MAIN MENU", True, ORANGE)
        self.text_rect = self.text.get_rect(center=(640, 100))

        self.text_shadow= GET_FONT('Regular', 100).render("MAIN MENU", True, WHITE)
        self.text_shadow_rect = self.text_shadow.get_rect(center=(644, 104))

        self.play_button = Button(None, pos=(640, 275),
                                  text_input="PLAY", font=GET_FONT('Regular', 75),
                                  base_color=ORANGE, hovering_color=WHITE)
        self.play_shadow = GET_FONT('Regular', 75).render("PLAY", True, WHITE)
        self.play_shadow_rect = self.play_shadow.get_rect(center=(644, 279))

        self.options_button = Button(None, pos=(640, 440),
                                     text_input="OPTIONS", font=GET_FONT('Regular', 75),
                                     base_color=ORANGE, hovering_color=WHITE)
        self.options_shadow = GET_FONT('Regular', 75).render("OPTIONS", True, WHITE)
        self.options_shadow_rect = self.options_shadow.get_rect(center=(644, 444))

        self.quit_button = Button(None, pos=(640, 600),
                                  text_input="QUIT", font=GET_FONT('Regular', 75),
                                  base_color=ORANGE, hovering_color=WHITE)
        self.quit_shadow = GET_FONT('Regular', 75).render("QUIT", True, WHITE)
        self.quit_shadow_rect = self.quit_shadow.get_rect(center=(644, 604))

    def input(self, event):
        mouse_pos = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.play_button.checkForInput(mouse_pos):
                scene = Play(self.manager)
                self.manager.push(scene)
            elif self.options_button.checkForInput(mouse_pos):
                scene = Options(self.manager)
                self.manager.push(scene)
            elif self.quit_button.checkForInput(mouse_pos):
                pygame.quit()
                sys.exit()

        for button in [self.play_button, self.options_button, self.quit_button]:
            button.changeColor(mouse_pos)

    def draw(self, screen):
        # print("Main Menu draw")
        screen.blit(BG, (0, 0))

        screen.blit(self.text_shadow, self.text_shadow_rect)
        screen.blit(self.text, self.text_rect)
        screen.blit(self.play_shadow, self.play_shadow_rect)
        screen.blit(self.options_shadow, self.options_shadow_rect)
        screen.blit(self.quit_shadow, self.quit_shadow_rect)

        for button in [self.play_button, self.options_button, self.quit_button]:
            button.update(screen)


class Options(Scene):
    def __init__(self, manager):
        pygame.display.set_caption("Options")
        self.manager = manager

        self.text = GET_FONT('Regular', 100).render("OPTIONS", True, ORANGE)
        self.text_rect = self.text.get_rect(center=(640, 160))
        self.text_shadow = GET_FONT('Regular', 100).render("OPTIONS", True, BLACK)
        self.text_shadow_rect = self.text_shadow.get_rect(center=(644, 164))

        self.credits = Button(image=None, pos=(640, 400),
                              text_input="CREDITS", font=GET_FONT('Regular', 75),
                              base_color=ORANGE, hovering_color=BLACK)
        self.credits_shadow = GET_FONT('Regular', 75).render("CREDITS", True, BLACK)
        self.credits_rect = self.credits_shadow.get_rect(center=(644, 404))

        self.back = Button(image=None, pos=(640, 560),
                           text_input="BACK", font=GET_FONT('Regular', 75),
                           base_color=ORANGE, hovering_color=BLACK)
        self.back_shadow = GET_FONT('Regular', 75).render("BACK", True, BLACK)
        self.back_rect = self.back_shadow.get_rect(center=(644, 564))

    def input(self, event):
        mouse_pos = pygame.mouse.get_pos()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.credits.checkForInput(mouse_pos):
                scene = Credits(self.manager)
                self.manager.push(scene)
            elif self.back.checkForInput(mouse_pos):
                self.manager.pop()  # close options menu

        self.credits.changeColor(mouse_pos)
        self.back.changeColor(mouse_pos)

    def draw(self, screen):
        # print("Options draw")
        screen.fill(WHITE)

        screen.blit(self.text_shadow, self.text_shadow_rect)
        screen.blit(self.text, self.text_rect)
        screen.blit(self.credits_shadow, self.credits_rect)
        screen.blit(self.back_shadow, self.back_rect)

        self.credits.update(screen)
        self.back.update(screen)


class Play(Scene):
    def __init__(self, manager):
        self.manager = manager

    def input(self, sm):
        pass

    def draw(self, sm):
        pass


class Credits(Scene):
    def __init__(self, manager):
        pygame.display.set_caption("Credits")
        self.manager = manager

        self.text = GET_FONT('Regular', 45).render("This game is presented by: ", True, BLACK)
        self.text_rect = self.text.get_rect(center=(655, 100))
        self.text_shadow = GET_FONT('Regular', 45).render("This game is presented by: ", True, WHITE)
        self.text_shadow_rect = self.text_shadow.get_rect(center=(658, 102))

        self.name_1 = GET_FONT('Regular', 40).render("Ashley Butela", True, BLACK)
        self.name_1_rect = self.name_1.get_rect(center=(640, 220))
        self.name_2 = GET_FONT('Regular', 40).render("Amy Ciuffoletti", True, BLACK)
        self.name_2_rect = self.name_2.get_rect(center=(640, 295))
        self.name_3 = GET_FONT('Regular', 40).render("Mehmet Ozen", True, BLACK)
        self.name_3_rect = self.name_2.get_rect(center=(700, 370))
        self.name_4 = GET_FONT('Regular', 40).render("Jacob Sharp", True, BLACK)
        self.name_4_rect = self.name_2.get_rect(center=(700, 445))
        self.name_5 = GET_FONT('Regular', 40).render("Nabeyou Tadessa", True, BLACK)
        self.name_5_rect = self.name_2.get_rect(center=(640, 520))

        self.back = Button(image=None, pos=(640, 640),
                        text_input="BACK", font=GET_FONT('Regular', 50),
                      base_color=BLACK, hovering_color=WHITE)
        self.back_shadow = GET_FONT('Regular', 50).render("BACK", True, WHITE)
        self.back_rect = self.back_shadow.get_rect(center=(642, 642))

    def input(self, event):
        mouse_pos = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.back.checkForInput(mouse_pos):
                self.manager.pop()  # close credits menu

        self.back.changeColor(mouse_pos)

    def draw(self, screen):
        # print("Credits draw")
        screen.fill(ORANGE)

        screen.blit(self.text_shadow, self.text_shadow_rect)
        screen.blit(self.text, self.text_rect)
        screen.blit(self.name_1, self.name_1_rect)
        screen.blit(self.name_2, self.name_2_rect)
        screen.blit(self.name_3, self.name_3_rect)
        screen.blit(self.name_4, self.name_4_rect)
        screen.blit(self.name_5, self.name_5_rect)
        screen.blit(self.back_shadow, self.back_rect)

        self.back.update(screen)


class SceneManager:
    # Will be a stack that can pop/push next scene to top
    def __init__(self):
        self.scenes = []

    def enterScene(self):
        pass

    def exitScene(self):
        pass

    def input(self, event):
        if self.scenes:
            self.scenes[-1].input(event)

    def draw(self, screen):
        if self.scenes:
            self.scenes[-1].draw(screen)

    def push(self, scene):
        # Exit Current Scene
        if self.scenes:
            self.scenes[-1].onExit()

        self.scenes.append(scene)
        self.scenes[-1].onEnter()

    def pop(self):
        self.exitScene()
        self.scenes.pop()
        self.enterScene()

    def set(self, scene):
        self.scenes = [scene]
