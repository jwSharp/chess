import pygame
from scene import *
from player import *
from config import *
import pygame
import sys
from config import *
from accessories import *
from board import *

def main():
    # Create Window
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("Main Menu")

    # Create Player
    players = [Human('Player 1'), None, None]

    # Create Scene Manager
    manager = SceneManager(players)
    main_menu = MainMenuScene(manager)
    manager.push(main_menu)
    
    pygame.time.set_timer(pygame.USEREVENT, 1000)
    # Game Loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or not manager.scenes:
                pygame.quit()
                running = False
            
            # handle events
            manager.input(event)

        manager.draw(screen)
        pygame.display.update()

main()
