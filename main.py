import pygame
from scene import *
from player import *
from config import *

def main():
    # create Window
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("Main Menu")

    # create player
    players = [Human(), None, None, None]

    # create scene manager
    manager = SceneManager(players)
    main_menu = MainMenuScene(manager)
    manager.push(main_menu)

    # game loop
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