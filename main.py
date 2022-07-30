import pygame
from scene import *
from player import *
from config import *

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