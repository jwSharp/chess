import pygame
from game_setup import *

def main():
    pygame.init()
    pygame.display.set_caption('Chess')
    clock = pygame.time.Clock()
    pygame.display.flip()
    while True:
        clock.tick(60)
        # drawing board, letters numbers arround the board, and pieces on the board
        SCREEN.fill((0, 0, 0))
        chess.draw_letters((255, 255, 255, 255))
        chess.draw_board()
        chess.draw_pieces()
        # event handling
        for event in pygame.event.get():
            handle_events(event)
        pygame.display.update()
        pygame.display.flip()
      
main()