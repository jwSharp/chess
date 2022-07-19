import pygame
import board
import piece
from constants import *

## Pieces ##
# White
pawn = piece.Piece(pygame.image.load(ASSETS_PATH + 'pawn.png'), (0, 6), 'pawn', 0, [('0', '1'), ('F', '0', '1|3')], [('1', '1'), ('-1', '1')])
rook = piece.Piece(pygame.image.load(ASSETS_PATH + 'rook.png'), (0, 7), 'rook', 0, [('0', '1|8'), ('0', '-1|-8'), ('1|8', '0'), ('-1|-8', '0')])
bishop = piece.Piece(pygame.image.load(ASSETS_PATH + 'bishop.png'), (2, 7), 'bishop', 0, [('1|7', '1|7'), ('-1|-7', '-1|-7'), ('-1|-7', '1|7'), ('1|7', '-1|-7')])
knight = piece.Piece(pygame.image.load(ASSETS_PATH + 'knight.png'), (1, 7), 'knight', 0, [('1', '2'), ('-1', '2'), ('2', '1'), ('-2', '1'), ('2', '-1'), ('-2', '-1'), ('1', '-2'), ('-1', '-2')])
queen = piece.Piece(pygame.image.load(ASSETS_PATH + 'queen.png'), (3, 7), 'queen', 0, [('0', '1|8'), ('0', '-1|-8'), ('1|8', '0'), ('-1|-8', '0'), ('1|7', '1|7'), ('-1|-7', '-1|-7'), ('-1|-7', '1|7'), ('1|7', '-1|-7')])
king = piece.Piece(pygame.image.load(ASSETS_PATH + 'king.png'), (4, 7), 'king', 0, [('0', '1'), ('0', '-1'), ('1', '0'), ('-1', '0'), ('1', '1'), ('-1', '-1'), ('1', '-1'), ('-1', '1')])

# Black
pawn1 = piece.Piece(pygame.image.load(ASSETS_PATH + 'pawn1.png'), (0, 1), 'pawn', 1, [('0', '-1'), ('F', '0', '-1|-3')], [('1', '-1'), ('-1', '-1')])
rook1 = piece.Piece(pygame.image.load(ASSETS_PATH + 'rook1.png'), (0, 0), 'rook', 1, rook.piece_moves)
bishop1 = piece.Piece(pygame.image.load(ASSETS_PATH + 'bishop1.png'), (2, 0), 'bishop', 1, bishop.piece_moves)
knight1 = piece.Piece(pygame.image.load(ASSETS_PATH + 'knight1.png'), (1, 0), 'knight', 1, knight.piece_moves)
queen1 = piece.Piece(pygame.image.load(ASSETS_PATH + 'queen1.png'), (3, 0), 'queen', 1, queen.piece_moves)
king1 = piece.Piece(pygame.image.load(ASSETS_PATH + 'king1.png'), (4, 0), 'king', 1, king.piece_moves)

## Chess ##
board_panel = pygame.Rect(SCREEN.get_width() / 2 - 200, SCREEN.get_height() / 2 - 200, 400, 400)
# chess board creation and piece setup
chess = board.Board(SCREEN, board_panel, pawn, rook, bishop, queen, king, knight, pawn1, rook1, bishop1, knight1, queen1, king1) 
chess.add_sets(pawn, ('0|7', '6'))
chess.add_sets(rook, ('7|7', '7'))
chess.add_sets(bishop, ('5|5', '7'))
chess.add_sets(knight, ('6|6', '7'))
chess.add_sets(pawn1, ('0|7', '1'))
chess.add_sets(rook1, ('7|7', '0'))
chess.add_sets(bishop1, ('5|5', '0'))
chess.add_sets(knight1, ('6|6', '0'))