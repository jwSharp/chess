import pygame
from pathlib import Path

import constants.py
import player.py
import piece.py

class Pawn(Piece):
    def __init__(self, position: (int, int), player: Player):
        self.player = player
        self.sprite = _set_sprite()

        self.position_board = Location(position)
        self.position_real_time = Location(position)

        self.sprite = _set_sprite(team)

        if player.team == 0:
            self._ways_to_move = [('0', '1'), ('F', '0', '1|3')], [('1', '1'), ('-1', '1')]
        else:
            self._ways_to_move = [('0', '-1'), ('F', '0', '-1|-3')], [('1', '-1'), ('-1', '-1')]


    def _set_sprite(team: int) -> pygame.image:
        '''Returns a path to the correct png.'''
        if self.player.team == 0:
            piece_path = Path(CHESS_PIECES / 'White/Pawn.png')
        else:
            piece_path = Path(CHESS_PIECES / 'Black/Pawn.png')
        return pygame.image.load(piece_path)
