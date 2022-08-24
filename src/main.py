'''
Modern | Retro Chess - A chess program focused on providing a simple solution to online simultaneous exhibitions.
Copyright (C) 2022 Society of Overthinkers

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''

import pygame

from config import * #TODO Import in a cleaner fashion
from scene import SceneManager, MainMenuScene
from player import Human


def main():
    # Create Window
    pygame.init()
    screen = pygame.display.set_mode(PIXEL_TO_ASPECT(WIDTH, HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("Main Menu")

    # Create Player
    players = [Human('Player 1'), None]

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
                width, height = FIXED_SCALE(width, height, (600, 400), (WIDTH, HEIGHT))
                width, height = PIXEL_TO_ASPECT(width, height)
                screen = pygame.display.set_mode((width,height), pygame.RESIZABLE)
            
            # Events
            manager.input(event)

        # Screen
        manager.draw(screen)
        pygame.display.update()

main()
