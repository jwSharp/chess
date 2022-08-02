import pygame

from config import *
from scene import *
from player import *


def main():
    # Create Window
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("Main Menu")

    # Create Player
    players = [Human('Player 1'), None, None, None]

    # Create Scene Manager
    manager = SceneManager(players)
    main_menu = MainMenuScene(manager)
    manager.push(main_menu)
    
    # Game Loop
    running = True
    while running:
        screen.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT or not manager.scenes:
                pygame.quit()
                running = False
            
            if event.type == pygame.VIDEORESIZE:
                width, height = event.size
                if width < 600:
                    width = 600
                if height < 400:
                    height = 400
                screen = pygame.display.set_mode((width,height), pygame.RESIZABLE)
            
            # Events
            manager.input(event)

        # Screen
        manager.draw(screen)
        pygame.display.update()

main()
