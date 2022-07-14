import constants.py
import player.py
from pathlib import Path

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

    @staticmethod #TODO make a static variable
    
    @staticmethod #TODO make a static variable
    _sprites = [] #TODO set based on path

    def __init__(self, position: (int, int), team: int, player: Player):
        self.player = player
        self.sprite = _set_sprite(team)
        self.team = team

        self.position_board = Location(position)
        self.position_real_time = Location(position)

        self.sprite = _set_sprite(team)
    
    def remove(self):
        '''Removes piece from the board.'''
        #TODO move to graveyard instead
        self.board_position = None
        self.real_time_position = None

        #TODO updates to team stats


    def _set_sprite(team: int):
        '''Returns a string containing the path to the correct png.'''
        if self.player.team == 0:
            p = Path(CHESS_PIECES / 'White')
        else:
            p = Path(CHESS_PIECES / 'Black')
        return '' #TODO return [images in _sprites folder][team]
