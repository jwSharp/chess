import pygame

from config import *
from game import *
from gui import *


def main():
    pygame.init()
    pygame.display.set_caption("Chess")
    
    while True:
        SCREEN.fill(BLACK)
        make_chess_GUI()
        chess.draw_letters(GOLD, 36, "elephant")
        chess.draw_board()
        chess.draw_pieces()

        for event in pygame.event.get():
            chess.handle_events(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        pygame.display.update()

        CLOCK.tick(60)

main()
