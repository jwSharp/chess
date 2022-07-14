import board.py
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


    @staticmethod #TODO make a static variable
    PATH = 'Resources/Game_Pieces/' #TODO set based on path
    @staticmethod #TODO make a static variable
    _sprites = [] #TODO set based on path

    def __init__(self, position: (int, int), team: int, board: Board):
        self.board = board
        self.sprite = _set_sprite(team)
        self.team = team

        self.board_position = Location(position)
        self.real_time_position = Location(position)


    def move(self, destination: (int, int)):
        if not is_legal_move(self, Location(destination)):
            #TODO illegal move
            self.real_time_position = self.board_position
        else:
            #TODO if capture
            #TODO 
    
    def remove(self):
        '''Removes piece from the board.'''
        #TODO move to graveyard instead
        self.board_position = None
        self.real_time_position = None

        #TODO updates to team stats


    def _set_sprite(team: int) -> str:
        '''Returns a string containing the path to the correct png.'''
        _sprites = 'Resources/Game_Pieces/'
        return '' #TODO return [images in _sprites folder][team]
