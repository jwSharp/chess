import pygame
import sys
from config import *
from accessories import *
from player import *
from board import *
from timer import Timer


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

    def input(self, event):
        pass

    def draw(self, screen):
        pass

    def enter(self):
        pass

    def exit(self):
        pass


#############
# Main Menu #
#############
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


class Options(Scene):
    def __init__(self, manager):
        self.manager = manager

        font = GET_FONT('Regular', 100)
        self.text = font.render("OPTIONS", True, ORANGE)
        self.text_rect = self.text.get_rect(center=(640, 160))
        self.text_shadow = font.render("OPTIONS", True, BLACK)
        self.text_shadow_rect = self.text_shadow.get_rect(center=(644, 164))

        font = GET_FONT('Regular', 75)
        self.credits = Button(None, (640, 400), "CREDITS", font, ORANGE, BLACK)
        self.credits_shadow = font.render("CREDITS", True, BLACK)
        self.credits_rect = self.credits_shadow.get_rect(center=(644, 404))

        self.back = Button(None, (640, 560), "BACK", font, ORANGE, BLACK)
        self.back_shadow = font.render("BACK", True, BLACK)
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

        font = GET_FONT('Regular', 45)
        self.text = font.render("This game is presented by: ", True, BLACK)
        self.text_rect = self.text.get_rect(center=(655, 100))
        self.text_shadow = font.render("This game is presented by: ", True, WHITE)
        self.text_shadow_rect = self.text_shadow.get_rect(center=(658, 102))

        font = GET_FONT('Regular', 40)
        self.name_1 = font.render("Ashley Butela", True, BLACK)
        self.name_1_rect = self.name_1.get_rect(center=(640, 220))
        self.name_2 = font.render("Amy Ciuffoletti", True, BLACK)
        self.name_2_rect = self.name_2.get_rect(center=(640, 295))
        self.name_3 = font.render("Mehmet Ozen", True, BLACK)
        self.name_3_rect = self.name_2.get_rect(center=(700, 370))
        self.name_4 = font.render("Jacob Sharp", True, BLACK)
        self.name_4_rect = self.name_2.get_rect(center=(700, 445))
        self.name_5 = font.render("Nabeyou Tadessa", True, BLACK)
        self.name_5_rect = self.name_2.get_rect(center=(640, 520))

        font = GET_FONT('Regular', 50)
        self.back = Button(None, (640, 640), "BACK", font, BLACK, WHITE)
        self.back_shadow = font.render("BACK", True, WHITE)
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


#############
# Selection #
#############
class PlayerSelection(Scene):
    def __init__(self, manager):
       self.manager = manager

       font = GET_FONT('Regular', 85)
       self.game_selection = font.render("PLAYER OPTIONS", True, ORANGE)
       self.game_selection_rect = self.game_selection.get_rect(center=(640, 100))
       self.game_selection_shadow = font.render("PLAYER OPTIONS", True, WHITE)
       self.game_selection_shadow_rect = self.game_selection_shadow.get_rect(center=(644, 104))

       font = GET_FONT('Regular', 75)
       self.one_player = Button(None, (640, 275), "One Player", font, ORANGE, WHITE)
       self.one_player_shadow = font.render("One Player", True, WHITE)
       self.one_player_rect = self.one_player_shadow.get_rect(center=(644, 279))

       self.two_player = Button(None, (640, 450), "Two Player", font, ORANGE, WHITE)
       self.two_player_shadow = font.render("Two Player", True, WHITE)
       self.two_player_rect = self.two_player_shadow.get_rect(center=(644, 454))

       font = GET_FONT('Regular', 75)
       self.back = Button(None, (640, 660), "BACK", font, ORANGE, WHITE)
       self.back_shadow = font.render("BACK", True, WHITE)
       self.back_rect = self.back_shadow.get_rect(center=(644, 664))

    def input(self, event):
        mouse_pos = pygame.mouse.get_pos()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.one_player.input(mouse_pos) or self.two_player.input(mouse_pos):
                if self.one_player.input(mouse_pos):
                    self.manager.players[1] = Computer()
                    self.manager.players[2] = None
                    #self.manager.players[3] = None #!List index out of range
                else:
                    self.manager.players[1] = Human('Player 2')
                    self.manager.players[2] = None
                    #self.manager.players[3] = None #!List index out of range

                scene = TimeSelection(self.manager)
                self.manager.push(scene)
            
            elif self.back.input(mouse_pos):
                self.manager.pop()

        self.one_player.set_color(mouse_pos)
        self.two_player.set_color(mouse_pos)
        self.back.set_color(mouse_pos)

    def draw(self, screen):
        pygame.display.set_caption("Society of Overthinker's Chess")
        screen.fill(BLACK)

        screen.blit(self.game_selection_shadow, self.game_selection_shadow_rect)
        screen.blit(self.game_selection, self.game_selection_rect)
        screen.blit(self.one_player_shadow, self.one_player_rect)
        screen.blit(self.two_player_shadow, self.two_player_rect)
        screen.blit(self.back_shadow, self.back_rect)

        self.one_player.update(screen)
        self.two_player.update(screen)
        self.back.update(screen)


class TimeSelection(Scene):
    def __init__(self, manager):
        self.manager = manager

        # get w/h and check % initial WIDTH/HEIGHT
        font = GET_FONT('Regular', 50)
        self.text = font.render("CHOOSE YOUR TIMER OPTION", True, ORANGE)
        self.text_rect = self.text.get_rect(center=(640, 50))
        self.text_shadow = font.render("CHOOSE YOUR TIMER OPTION", True, BLACK)
        self.text_shadow_rect = self.text_shadow.get_rect(center=(644, 54))

        font = GET_FONT('Regular', 35)
        time_1_0 = Button(None, (325, 150), "1 + 0", font, ORANGE, BLACK)
        time_2_1 = Button(None, (640, 150), "2 + 1", font, ORANGE, BLACK)
        time_3_0 = Button(None, (955, 150), "3 + 0", font, ORANGE, BLACK)
        time_3_2 = Button(None, (325, 315), "3 + 0", font, ORANGE, BLACK)
        time_5_0 = Button(None, (640, 315), "5 + 0", font, ORANGE, BLACK)
        time_5_3 = Button(None, (955, 315), "5 + 3", font, ORANGE, BLACK)
        time_10_0 = Button(None, (325, 500), "10 + 0", font, ORANGE, BLACK)
        time_10_5 = Button(None, (640, 500), "10 + 5", font, ORANGE, BLACK)
        time_15_10 = Button(None, (955, 500), "15 + 10", font, ORANGE, BLACK)
        self.buttons = (time_1_0, time_2_1, time_3_0, time_3_2, time_5_0, time_5_3, time_10_0, time_10_5, time_15_10)

        font = GET_FONT('Regular', 50)
        self.time_unlimited = Button(None, (644, 664), "Unlimited", font, ORANGE, BLACK)
        self.time_unlimited_shadow = font.render("Unlimited", True, BLACK)
        self.time_unlimited_rect = self.time_unlimited_shadow.get_rect(center=(640, 660))

        self.back = Button(None, (100, 664), "<=", GET_FONT('Regular', 50), ORANGE, BLACK)

    def input(self, event):
        mouse_pos = pygame.mouse.get_pos()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.back.input(mouse_pos):
                self.manager.pop()

            for button in self.buttons:
                if button.input(mouse_pos):
                    time = self._parse_time(button.name)

                    self.manager.pop() # TimeSelection
                    self.manager.pop() # PlayerSelection
                    scene = Game(self.manager, time)
                    self.manager.push(scene)

            if self.time_unlimited.input(mouse_pos):
                self.manager.pop() # TimeSelection
                self.manager.pop() # PlayerSelection
                scene = Game(self.manager)
                self.manager.push(scene)

        for button in self.buttons:
            button.set_color(mouse_pos)

        self.back.set_color(mouse_pos)

    def draw(self, screen):
        pygame.display.set_caption("Time Selection")
        screen.fill(WHITE)

        screen.blit(self.text_shadow, self.text_shadow_rect)
        screen.blit(self.text, self.text_rect)

        for button in self.buttons:
            button.update(screen)
        
        screen.blit(self.time_unlimited_shadow, self.time_unlimited_rect)
        self.back.update(screen)

    def _parse_time(self, name: str) -> (int, int):
        if len(name) == 5:
            return (int(name[0]), int(name[-1]))
        elif len(name) == 6:
            return (int(name[:2]), int(name[-1]))
        else:
            return (int(name[:2]), int(name[-2:]))


#############
# Game Play #
#############
class Game(Scene):
    def __init__(self, manager, time=(0,0)):
        '''For timed and untimed chess matches.'''
        self.manager = manager
        self.time = time

        self.player_1_timer = Timer(self.time[0], self.time[1])
        self.player_2_timer = Timer(self.time[0], self.time[1])

        # if self.time == (0,0): # Unlimited Time
        #     self.timer_1 = None
        #     self.timer_2 = None
        # else:
        #     self.timer_1 = Timer(self.time)
        #     self.timer_2 = Timer(self.time)

        # Logo
        font = GET_FONT("ocr", 64) #previously ocr: DNE
        self.retro_text = font.render("Retro", True, GOLD, BLACK)
        self.retro_text_rect = self.retro_text.get_rect(center=(WIDTH / 10, HEIGHT / 1.25))

        self.modern_text = font.render("Modern", True, GOLD, BLACK)
        self.modern_text_rect = self.modern_text.get_rect(center=(WIDTH / 10, HEIGHT / 1.16))

        self.chess_text = font.render("Chess", True, GOLD, BLACK)
        self.chess_text_rect = self.chess_text.get_rect(center=(WIDTH / 10, HEIGHT / 1.08))

        # Menu Buttons
        font = GET_FONT("elephant", 26) #previously elephant: DNE
        self.menu_text = font.render("Menu", True, BLACK)
        self.menu_text_rect = self.menu_text.get_rect(center=(WIDTH / 1.19, HEIGHT / 1.3))

        self.exit_text = font.render("Exit", True, BLACK)
        self.exit_text_rect = self.exit_text.get_rect(center=(WIDTH / 1.19, HEIGHT / 1.15))

        # Players
        font = GET_FONT("brushscript", 62)
        self.player_1 = font.render(self.manager.players[0].name, True, GOLD, BLACK)
        self.player_1_rect = self.player_1.get_rect(center=(WIDTH / 10, 49))

        self.player_2 = font.render(self.manager.players[1].name, True, GOLD, BLACK)
        self.player_2_rect = self.player_2.get_rect(center=(WIDTH / 1.1, 49))

        # Board
        self.board = Board()

    def input(self, event):
        if event.type == pygame.USEREVENT:
            if self.board.current_turn == 0:
                self.player_1_timer.update()
            if self.board.current_turn == 1:
                self.player_2_timer.update()
        mouse_pos = pygame.mouse.get_pos()
        self.board.input(event)
        #self.board.input(event)

    def draw(self, screen):
        pygame.display.set_caption("Retro|Modern Chess")
        screen.fill(BLACK)
        width, height = screen.get_size()

        # Frame
        pygame.draw.rect(screen, GOLD, ((0, 0), (width / 5, height)), 10)
        pygame.draw.rect(screen, GOLD, ((width / 1.25, 0), (width / 5, height)), 10)
        pygame.draw.rect(screen, GOLD, ((0, 0), (width, height)), 10)

        # Shadows
        pygame.draw.line(screen, GOLD_SHADOW, (8, 8), (width - 8, 8), 4)
        pygame.draw.line(screen, GOLD_SHADOW, (8, 8), (8, width - 8), 4)
        pygame.draw.line(screen, GOLD_SHADOW, (width - 3, 3), (width - 3, height - 5), 4)
        pygame.draw.line(screen, GOLD_SHADOW, (0, height - 3), (width, height - 3), 4)
        pygame.draw.line(screen, GOLD_SHADOW, (width / 5.05, 8), (width / 5.05, height - 8), 4)
        pygame.draw.line(screen, GOLD_SHADOW, (width / 1.24, 8), (width / 1.24, height - 8), 4)

        # Capture Area
        pygame.draw.rect(screen, GOLD, ((20, height / 4.5), (width / 5 - 40, height / 2)), 5)
        pygame.draw.rect(screen, GOLD, ((width / 1.225, height / 4.5), (width / 5 - 40, height / 2)), 5)
        
        # Logo
        screen.blit(self.retro_text, self.retro_text_rect)
        screen.blit(self.modern_text, self.modern_text_rect)
        screen.blit(self.chess_text, self.chess_text_rect)

        # Menu Buttons
        screen.blit(self.menu_text, self.menu_text_rect)
        screen.blit(self.exit_text, self.exit_text_rect)

        # Players
        screen.blit(self.player_1, self.player_1_rect)
        screen.blit(self.player_2, self.player_2_rect)

        # Timer
        if self.time:
            time_box_1 = pygame.draw.rect(screen, GOLD, ((20, height / 9), (width / 5 - 40, height / 11)), 5)
            time_box_2 = pygame.draw.rect(screen, GOLD, ((width / 1.225, height / 9), (width / 5 - 40, height / 11)), 5)
            self.player_1_timer.draw(time_box_1.center, 32, screen)
            self.player_2_timer.draw(time_box_2.center, 32, screen)

        # Board
        board_panel = pygame.Rect(screen.get_width() / 2 - 300, screen.get_height() / 2 - 300, 600, 600)
        self.board.draw(screen, board_panel)





