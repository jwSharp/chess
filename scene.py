# Updated scene.py to include updates from 7/29 - 8/1

import pygame
import sys
from button import *
from config import *
from player import *


class SceneManager:
    '''A stack of Scene objects that can pop/push next scene to top.'''

    def __init__(self, players: [Player]):
        self.players = players
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


class MainMenuScene(Scene):
    def __init__(self, manager):
        self.manager = manager

        self.text = GET_FONT('Regular', 100).render("MAIN MENU", True, ORANGE)
        self.text_rect = self.text.get_rect(center=(640, 100))

        self.text_shadow = GET_FONT('Regular', 100).render("MAIN MENU", True, WHITE)
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
                scene = PlayerSelection(self.manager)
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


#############
# Selection #
#############
class PlayerSelection(Scene):
    def __init__(self, manager):
        self.manager = manager

        self.game_selection = GET_FONT('Regular', 85).render("PLAYER OPTIONS", True, ORANGE)
        self.game_selection_rect = self.game_selection.get_rect(center=(640, 100))
        self.game_selection_shadow = GET_FONT('Regular', 85).render("PLAYER OPTIONS", True, WHITE)
        self.game_selection_shadow_rect = self.game_selection_shadow.get_rect(center=(644, 104))

        self.one_player = Button(None, (640, 275), "One Player", GET_FONT('Regular', 75), ORANGE, WHITE)
        self.one_player_shadow = GET_FONT('Regular', 75).render("One Player", True, WHITE)
        self.one_player_rect = self.one_player_shadow.get_rect(center=(644, 279))

        self.two_player = Button(None, (640, 450), "Two Player", GET_FONT('Regular', 75), ORANGE, WHITE)
        self.two_player_shadow = GET_FONT('Regular', 75).render("Two Player", True, WHITE)
        self.two_player_rect = self.two_player_shadow.get_rect(center=(644, 454))

        self.back = Button(None, (340, 660), "BACK", GET_FONT('Regular', 65), ORANGE, WHITE)
        self.back_shadow = GET_FONT('Regular', 65).render("BACK", True, WHITE)
        self.back_rect = self.back_shadow.get_rect(center=(344, 664))

        self.quit = Button(None, (940, 660), "QUIT", GET_FONT('Regular', 65), ORANGE, WHITE)
        self.quit_shadow = GET_FONT('Regular', 65).render("QUIT", True, WHITE)
        self.quit_rect = self.back_shadow.get_rect(center=(944, 664))

    def input(self, event):
        mouse_pos = pygame.mouse.get_pos()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.quit.input(mouse_pos):
                pygame.quit()
                sys.exit()
            if self.one_player.input(mouse_pos) or self.two_player.input(mouse_pos):
                if self.one_player.input(mouse_pos):
                    self.manager.players[1] = Computer()
                    self.manager.players[2] = None
                    self.manager.players[3] = None
                else:
                    self.manager.players[1] = Human()
                    self.manager.players[2] = None
                    self.manager.players[3] = None

                scene = TimeSelection(self.manager)
                self.manager.push(scene)

            elif self.back.input(mouse_pos):
                self.manager.pop()

        self.one_player.set_color(mouse_pos)
        self.two_player.set_color(mouse_pos)
        self.quit.set_color(mouse_pos)
        self.back.set_color(mouse_pos)


    def draw(self, screen):
        pygame.display.set_caption("Society of Overthinker's Chess")
        screen.fill(BLACK)

        screen.blit(self.game_selection_shadow, self.game_selection_shadow_rect)
        screen.blit(self.game_selection, self.game_selection_rect)
        screen.blit(self.one_player_shadow, self.one_player_rect)
        screen.blit(self.two_player_shadow, self.two_player_rect)
        screen.blit(self.back_shadow, self.back_rect)
        screen.blit(self.quit_shadow, self.quit_rect)

        self.one_player.update(screen)
        self.two_player.update(screen)
        self.quit.update(screen)
        self.back.update(screen)


class TimeSelection(Scene):

    def __init__(self, manager):
        self.manager = manager

        # get w/h and check % initial WIDTH/HEIGHT
        self.text = GET_FONT('Regular', 50).render("CHOOSE YOUR TIMER OPTION", True, ORANGE)
        self.text_rect = self.text.get_rect(center=(640, 75))
        self.text_shadow = GET_FONT('Regular', 50).render("CHOOSE YOUR TIMER OPTION", True, BLACK)
        self.text_shadow_rect = self.text_shadow.get_rect(center=(644, 79))

        self.time_1_0 = Button(None, (225, 200), "BULLET 1 + 0", GET_FONT('Regular', 25), ORANGE, BLACK)
        self.time_2_1 = Button(None, (640, 200), "BULLET 2 + 1", GET_FONT('Regular', 25), ORANGE, BLACK)
        self.time_3_0 = Button(None, (1055, 200), "BLITZ 3 + 0", GET_FONT('Regular', 25), ORANGE, BLACK)
        self.time_3_2 = Button(None, (225, 350), "BLITZ 3 + 0", GET_FONT('Regular', 25), ORANGE, BLACK)
        self.time_5_0 = Button(None, (640, 350), "BLITZ 5 + 0", GET_FONT('Regular', 25), ORANGE, BLACK)
        self.time_5_3 = Button(None, (1055, 350), "BLITZ 5 + 3", GET_FONT('Regular', 25), ORANGE, BLACK)
        self.time_10_0 = Button(None, (225, 495), "RAPID 10 + 0", GET_FONT('Regular', 25), ORANGE, BLACK)
        self.time_10_5 = Button(None, (640, 495), "RAPID 10 + 5", GET_FONT('Regular', 25), ORANGE, BLACK)
        self.time_15_10 = Button(None, (1055, 495), "RAPID 15 + 10", GET_FONT('Regular', 25), ORANGE, BLACK)

        self.time_unlimited = Button(None, (644, 620), "UNLIMITED", GET_FONT('Regular', 40), ORANGE, BLACK)
        self.time_unlimited_shadow = GET_FONT('Regular', 40).render("UNLIMITED", True, BLACK)
        self.time_unlimited_rect = self.time_unlimited_shadow.get_rect(center=(640, 623))

        self.back = Button(None, (100, 750), "<=", GET_FONT('Regular', 50), ORANGE, BLACK)
        self.back_shadow = GET_FONT('Regular', 50).render("<=", True, BLACK)
        self.back_shadow_rect = self.back_shadow.get_rect(center=(103, 753))

        self.info = Button(None, (640, 750), "TIMER INFO", GET_FONT('Regular', 35), ORANGE, BLACK)
        self.info_shadow = GET_FONT('Regular', 35).render("TIMER INFO", True, BLACK)
        self.info_shadow_rect = self.info_shadow.get_rect(center=(644, 753))

        self.quit = Button(None, (1140, 750), "QUIT", GET_FONT('Regular', 35), ORANGE, BLACK)
        self.quit_shadow = GET_FONT('Regular', 35).render("QUIT", True, BLACK)
        self.quit_rect = self.quit_shadow.get_rect(center=(1144, 753))

    def input(self, event):
        mouse_pos = pygame.mouse.get_pos()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.quit.input(mouse_pos):
                pygame.quit()
                sys.exit()
            if self.back.input(mouse_pos):
                self.manager.pop()

            if self.info.input(mouse_pos):
                scene = TimerInfo(self.manager)
                self.manager.push(scene)

            if self.time_1_0.input(mouse_pos) or self.time_2_1.input(mouse_pos) or self.time_3_0.input(
                    mouse_pos) or self.time_3_2.input(mouse_pos) or self.time_5_0.input(
                mouse_pos) or self.time_5_3.input(mouse_pos) or self.time_10_0.input(
                mouse_pos) or self.time_10_5.input(mouse_pos) or self.time_15_10.input(
                mouse_pos) or self.time_unlimited.input(mouse_pos):
                pass


        # buncha if's

        # elif self.time_unlimited.input(mouse_pos):

        self.time_1_0.set_color(mouse_pos)
        self.time_2_1.set_color(mouse_pos)
        self.time_3_0.set_color(mouse_pos)
        self.time_3_2.set_color(mouse_pos)
        self.time_5_0.set_color(mouse_pos)
        self.time_5_3.set_color(mouse_pos)
        self.time_10_0.set_color(mouse_pos)
        self.time_10_5.set_color(mouse_pos)
        self.time_15_10.set_color(mouse_pos)
        self.time_unlimited.set_color(mouse_pos)
        self.back.set_color(mouse_pos)
        self.info.set_color(mouse_pos)
        self.quit.set_color(mouse_pos)


    def draw(self, screen):
        pygame.display.set_caption("Time Selection")
        screen.fill(WHITE)

        screen.blit(self.text_shadow, self.text_shadow_rect)
        screen.blit(self.text, self.text_rect)
        self.time_1_0.update(screen)
        self.time_2_1.update(screen)
        self.time_3_0.update(screen)
        self.time_3_2.update(screen)
        self.time_5_0.update(screen)
        self.time_5_3.update(screen)
        self.time_10_0.update(screen)
        self.time_10_5.update(screen)
        self.time_15_10.update(screen)
        self.time_unlimited.update(screen)
        screen.blit(self.time_unlimited_shadow, self.time_unlimited_rect)
        screen.blit(self.back_shadow, self.back_shadow_rect)
        self.back.update(screen)
        screen.blit(self.info_shadow, self.info_shadow_rect)
        self.info.update(screen)
        screen.blit(self.quit_shadow, self.quit_rect)
        self.quit.update(screen)



class TimerInfo(TimeSelection):
    def __init__(self, manager):
        self.manager = manager

        # get w/h and check % initial WIDTH/HEIGHT
        self.text = GET_FONT('Regular', 50).render("TIMER INFO", True, ORANGE)
        self.text_rect = self.text.get_rect(center=(640, 75))
        self.text_shadow = GET_FONT('Regular', 50).render("TIMER INFO", True, BLACK)
        self.text_shadow_rect = self.text_shadow.get_rect(center=(644, 79))

        self.info = GET_FONT('Regular', 20).render("Time controls are based on estimated game duration", True, BLACK)
        self.info_rect = self.info.get_rect(center=(640, 180))

        # Triple quoted strings contain new line characters
        self.t_text = GET_FONT('Regular', 20).render("(clock initial time in seconds) + 40 × (clock increment)", True, BLACK)
        self.t_text_rect = self.t_text.get_rect(center=(640, 225))

        self.bullet = GET_FONT('Regular', 30).render("≤ 179s = Bullet", True, BLACK)
        self.bullet_rect = self.bullet.get_rect(center=(640, 350))

        self.blitz = GET_FONT('Regular', 30).render("≤ 479s = Blitz", True, BLACK)
        self.blitz_rect = self.blitz.get_rect(center=(640, 450))

        self.rapid = GET_FONT('Regular', 30).render("≤ 1499s = Rapid", True, BLACK)
        self.rapid_rect = self.rapid.get_rect(center=(640, 550))

        self.back = Button(None, (100, 700), "<=", GET_FONT('Regular', 50), ORANGE, BLACK)
        self.back_shadow = GET_FONT('Regular', 50).render("<=", True, BLACK)
        self.back_shadow_rect = self.back_shadow.get_rect(center=(103, 703))



    def input(self, event):
        mouse_pos = pygame.mouse.get_pos()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.back.input(mouse_pos):
                self.manager.pop()

        # buncha if's

        self.back.set_color(mouse_pos)

    def draw(self, screen):
        pygame.display.set_caption("Timer Info")
        screen.fill(WHITE)


        screen.blit(self.text_shadow, self.text_shadow_rect)
        screen.blit(self.text, self.text_rect)
        screen.blit(self.info, self.info_rect)
        screen.blit(self.t_text, self.t_text_rect)
        screen.blit(self.bullet, self.bullet_rect)
        screen.blit(self.blitz, self.blitz_rect)
        screen.blit(self.rapid, self.rapid_rect)
        screen.blit(self.back_shadow, self.back_shadow_rect)
        self.back.update(screen)




#############
# Game Play #
#############
class Game(Scene):
    def __init__(self, manager, time: (int, int)):
        self.manager = manager

        print(self.manager.players)
        print(self.time)


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


#########
# Other #
#########
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


