import pygame
from game import *
from constants import *
from gui import *

def main():
    pygame.init()
    pygame.display.set_caption('Chess')
    while True:
        CLOCK.tick(60)
        # drawing board, letters numbers arround the board, and pieces on the board
        SCREEN.fill(BLACK)
        make_chess_GUI()
        chess.draw_letters(GOLD, 36, 'elephant')
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