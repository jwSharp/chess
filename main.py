import pygame
import board
import piece
from pathlib import Path

SCREEN = pygame.display.set_mode((600, 600))
# Path where the file is located
file_path = Path(__file__).parent.absolute()
# path where the assets are stored 
assets_path = str(file_path / 'assets') + '/'

# Pieces
pawn = piece.Piece(pygame.image.load(assets_path + 'pawn.png'), (0, 6), 'pawn', 0, [('0', '1'), ('F', '0', '1|3')], [('1', '1'), ('-1', '1')])
rook = piece.Piece(pygame.image.load(assets_path + 'rook.png'), (0, 7), 'rook', 0, [('0', '1|8'), ('0', '-1|-8'), ('1|8', '0'), ('-1|-8', '0')])
bishop = piece.Piece(pygame.image.load(assets_path + 'bishop.png'), (2, 7), 'bishop', 0, [('1|7', '1|7'), ('-1|-7', '-1|-7'), ('-1|-7', '1|7'), ('1|7', '-1|-7')])
knight = piece.Piece(pygame.image.load(assets_path + 'knight.png'), (1, 7), 'knight', 0, [('1', '2'), ('-1', '2'), ('2', '1'), ('-2', '1'), ('2', '-1'), ('-2', '-1'), ('1', '-2'), ('-1', '-2')])


pawn1 = piece.Piece(pygame.image.load(assets_path + 'pawn1.png'), (0, 1), 'pawn', 1, [('0', '1'), ('F', '0', '1|3')], [('1', '2'), ('-1', '2')])
rook1 = piece.Piece(pygame.image.load(assets_path + 'rook1.png'), (0, 0), 'rook', 1, [('0', '1|8'), ('0', '-1|-8'), ('1|8', '0'), ('-1|-8', '0')])
bishop1 = piece.Piece(pygame.image.load(assets_path + 'bishop1.png'), (2, 0), 'bishop', 1, [('1|7', '1|7'), ('-1|-7', '-1|-7'), ('-1|-7', '1|7'), ('1|7', '-1|-7')])
knight1 = piece.Piece(pygame.image.load(assets_path + 'knight1.png'), (1, 0), 'knight', 1, [('1', '2'), ('-1', '2'), ('2', '1'), ('-2', '1'), ('2', '-1'), ('-2', '-1'), ('1', '-2'), ('-1', '-2')])

# Rectangle for our chess board
board_panel = pygame.Rect(SCREEN.get_width() / 2 - 200, SCREEN.get_height() / 2 - 200, 400, 400)

def main():
    pygame.init()
    pygame.display.set_caption('Chess')
    chess = board.Board(SCREEN, board_panel, pawn, rook, bishop, knight, pawn1, rook1, bishop1, knight1) # chess class
    chess.add_sets(pawn, ('0|7', '6'))
    chess.add_sets(rook, ('7|7', '7'))
    chess.add_sets(bishop, ('5|5', '7'))
    chess.add_sets(knight, ('6|6', '7'))
    chess.add_sets(pawn1, ('0|7', '1'))
    chess.add_sets(rook1, ('7|7', '0'))
    chess.add_sets(bishop1, ('5|5', '0'))
    chess.add_sets(knight1, ('6|6', '0'))
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
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN: 
                if event.button == 1: # left click to select a block
                    chess.select_block(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1: # release left click to drop the piece
                    chess.drop_piece(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
            elif event.type == pygame.MOUSEMOTION:
                if pygame.mouse.get_pressed()[0]: # if dragging, move the piece
                    chess.drag_piece(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r: # reset the board !!currently not working 
                    chess = board.Board(SCREEN, board_panel, pawn)
        pygame.display.update()
        pygame.display.flip()
      
main()