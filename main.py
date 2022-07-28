import pygame
from scene import *
from player import *

def main():
    # create Window
    pygame.init()
    screen = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
    pygame.display.set_caption("Main Menu")

    # create player
    player = Player()

    # create scene manager
    manager = SceneManager(player)
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