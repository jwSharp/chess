import pygame
import sys
from button import Button
from config import *


class SceneManager:
    '''A stack of Scene objects that can pop/push next scene to top.'''
    def __init__(self):
        self.scenes = []

    def enter(self):
        pass

    def exit(self):
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
            self.scenes[-1].exit()

        self.scenes.append(scene)
        self.scenes[-1].enter()

    def pop(self):
        self.exit()
        self.scenes.pop()
        self.enter()

    def set(self, scene):
        self.scenes = [scene]


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

    def enter(self):
        pass

    def exit(self):
        pass


##########
# Scenes #
##########
class MainMenuScene(Scene):
    def __init__(self, manager):
        self.manager = manager

        self.text = GET_FONT('Regular', 100).render("MAIN MENU", True, ORANGE)
        self.text_rect = self.text.get_rect(center=(640, 100))

        self.text_shadow= GET_FONT('Regular', 100).render("MAIN MENU", True, WHITE)
        self.text_shadow_rect = self.text_shadow.get_rect(center=(644, 104))

        self.play = Button(None, (640, 275), "PLAY", GET_FONT('Regular', 75), ORANGE, WHITE)
        self.play_shadow = GET_FONT('Regular', 75).render("PLAY", True, WHITE)
        self.play_shadow_rect = self.play_shadow.get_rect(center=(644, 279))

        self.options = Button(None, (640, 440), "OPTIONS", GET_FONT('Regular', 75), ORANGE, WHITE)
        self.options_shadow = GET_FONT('Regular', 75).render("OPTIONS", True, WHITE)
        self.options_shadow_rect = self.options_shadow.get_rect(center=(644, 444))

        self.quit = Button(None, (640, 600), "QUIT", GET_FONT('Regular', 75), ORANGE, WHITE)
        self.quit_shadow = GET_FONT('Regular', 75).render("QUIT", True, WHITE)
        self.quit_shadow_rect = self.quit_shadow.get_rect(center=(644, 604))

    def input(self, event):
        mouse_pos = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.play.input(mouse_pos):
                scene = Play(self.manager)
                self.manager.push(scene)
            elif self.options.input(mouse_pos):
                scene = Options(self.manager)
                self.manager.push(scene)
            elif self.quit.input(mouse_pos):
                pygame.quit()
                sys.exit()

        self.play.set_color(mouse_pos)
        self.options.set_color(mouse_pos)
        self.quit.set_color(mouse_pos)

    def draw(self, screen):
        pygame.display.set_caption("Main Menu")
        screen.blit(BACKGROUND, (0, 0))

        screen.blit(self.text_shadow, self.text_shadow_rect)
        screen.blit(self.text, self.text_rect)
        screen.blit(self.play_shadow, self.play_shadow_rect)
        screen.blit(self.options_shadow, self.options_shadow_rect)
        screen.blit(self.quit_shadow, self.quit_shadow_rect)

        self.play.update(screen)
        self.options.update(screen)
        self.quit.update(screen)


class Play(Scene):
    def __init__(self, manager):
        self.manager = manager

    def input(self, event):
        mouse_pos = pygame.mouse.get_pos()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pass

    def draw(self, sm):
        pygame.display.set_caption("Society of Overthinker's Chess")


class Options(Scene):
    def __init__(self, manager):
        self.manager = manager

        self.text = GET_FONT('Regular', 100).render("OPTIONS", True, ORANGE)
        self.text_rect = self.text.get_rect(center=(640, 160))
        self.text_shadow = GET_FONT('Regular', 100).render("OPTIONS", True, BLACK)
        self.text_shadow_rect = self.text_shadow.get_rect(center=(644, 164))

        self.credits = Button(None, (640, 400), "CREDITS", GET_FONT('Regular', 75), ORANGE, BLACK)
        self.credits_shadow = GET_FONT('Regular', 75).render("CREDITS", True, BLACK)
        self.credits_rect = self.credits_shadow.get_rect(center=(644, 404))

        self.back = Button(None, (640, 560), "BACK", GET_FONT('Regular', 75), ORANGE, BLACK)
        self.back_shadow = GET_FONT('Regular', 75).render("BACK", True, BLACK)
        self.back_rect = self.back_shadow.get_rect(center=(644, 564))

    def input(self, event):
        mouse_pos = pygame.mouse.get_pos()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.credits.input(mouse_pos):
                scene = Credits(self.manager)
                self.manager.push(scene)
            elif self.back.input(mouse_pos):
                self.manager.pop()  # close options menu

        self.credits.set_color(mouse_pos)
        self.back.set_color(mouse_pos)

    def draw(self, screen):
        pygame.display.set_caption("Options")
        screen.fill(WHITE)

        screen.blit(self.text_shadow, self.text_shadow_rect)
        screen.blit(self.text, self.text_rect)
        screen.blit(self.credits_shadow, self.credits_rect)
        screen.blit(self.back_shadow, self.back_rect)

        self.credits.update(screen)
        self.back.update(screen)


class Credits(Scene):
    def __init__(self, manager):
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

        self.back = Button(None, (640, 640), "BACK", GET_FONT('Regular', 50), BLACK, WHITE)
        self.back_shadow = GET_FONT('Regular', 50).render("BACK", True, WHITE)
        self.back_rect = self.back_shadow.get_rect(center=(642, 642))

    def input(self, event):
        mouse_pos = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.back.input(mouse_pos):
                self.manager.pop()  # close credits menu

        self.back.set_color(mouse_pos)

    def draw(self, screen):
        pygame.display.set_caption("Credits")
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