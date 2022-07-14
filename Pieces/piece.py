import pygame
from pathlib import Path

import constants.py
import player.py

##################
# Abstract Class #
##################
class Piece:
    '''Represents a game piece.'''
    
    @staticmethod #TODO make a static method
    class Location:
        '''x and y coordinates on the board.'''
        def __init__(x_coord: int, y_coord: int):
            self.x, self.y = x_coord, y_coord
        def __init__(coordinates: (int, int)):
            self.x, self.y = coordinates

    @staticmethod #TODO make a static variable
    _ways_to_move = []

    def __init__(self, position: (int, int), player: Player):
        self.player = player
        self.sprite = _set_sprite() #TODO based on order

        self.position_board = Location(position)
        self.position_real_time = Location(position)

        self.sprite = _set_sprite(team)
    
    def remove(self):
        '''Removes piece from the board.'''
        #TODO move to graveyard instead
        self.board_position = None
        self.real_time_position = None

        #TODO updates to team stats

    def _set_sprite(team: int) -> pygame.image:
        '''Returns a path to the correct png.'''
        if self.player.team == 0:
            piece_path = Path(CHESS_PIECES / 'White')
        else:
            piece_path = Path(CHESS_PIECES / 'Black')
        return pygame.image.load(piece_path)
