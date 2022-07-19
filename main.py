import pygame
from game import *
from constants import *

def main():
    pygame.init()
    pygame.display.set_caption('Chess')
    clock = pygame.time.Clock()
    while True:
        clock.tick(60)
        # drawing board, letters numbers arround the board, and pieces on the board
        SCREEN.fill(BLACK)
        chess.draw_letters(WHITE)
        chess.draw_board()
        chess.draw_pieces()
        # event handling
        for event in pygame.event.get():
            chess.handle_events(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        pygame.display.update()
      
main()