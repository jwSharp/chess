import pygame
from pathlib import Path

import constants
import board
import player

def main():
    FPS = 60

    pygame.init()
    pygame.display.set_caption('Chess')
    clock = pygame.time.Clock()

    dims = pygame.display.get_desktop_sizes()[0]
    screen = pygame.display.set_mode((dims[0], dims[1]))

    #! decide players
    players = set_players()
    

    #! decide game
    chess = board.Board(screen)

    
    #board_panel = pygame.Rect(SCREEN.get_width() / 2 - 200, SCREEN.get_height() / 2 - 200, 400, 400)
    #file_path = Path(__file__).parent.absolute()
    #assets_path = str(file_path / 'Assets') + '/'

    
    # chess
    #! create board
    #chess = Board(screen)
    
    while True:
        for event in pygame.event.get():
            handle_events(event)

        
        clock.tick(FPS)
        screen.fill(constants.BLACK)
        
        #game.draw()

        
        

        pygame.display.update()


def handle_events(event):
    global chess
    if event.type == pygame.QUIT:
        pygame.quit()
        quit()

    # Dragging pieces.
    #elif event.type == pygame.MOUSEBUTTONDOWN: 
    #    if event.button == 1: # left click to select a block
    #        chess.select_block(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
    #elif event.type == pygame.MOUSEBUTTONUP:
    #    if event.button == 1: # release left click to drop the piece
    #        chess.drop_piece(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
    #elif event.type == pygame.KEYDOWN:
    #    if event.key == pygame.K_r: # reset the board !!currently not working 
    #        chess = board.Board(SCREEN, board_panel, pawn)
    #if pygame.mouse.get_pressed()[0]: # if dragging, move the piece
    #    chess.drag_piece(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
    

def set_players() -> [player.Player]:
    players = []
    #! Loop for desired amount of players
    name = input("Player name:")
    players.append(player.Player(name))
    return players

      
main()

