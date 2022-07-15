import pygame

from game_setup import * #! will need updating

def main():
    pygame.init()
    pygame.display.set_caption('Chess')
    clock = pygame.time.Clock()
    #! decide game
    # chess
    #! create board
    game = Board()
    
    while True:
        clock.tick(60)
        # drawing board, letters numbers arround the board, and pieces on the board
        SCREEN.fill((0, 0, 0))
        
        game.draw()

        # event handling
        for event in pygame.event.get():
            handle_events(event)
        pygame.display.update()
      
main()

