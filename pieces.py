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
    def _ways_to_move(ways_of_move: list) -> list:
        return ways_of_move #! @staticmethod can only be used on functions

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





class Knight(Piece):

    ways_to_move = Piece._ways_to_move([('1', '2'), ('-1', '2'), ('2', '1'), ('-2', '1'), ('2', '-1'), ('-2', '-1'), ('1', '-2'), ('-1', '-2')]) 

    def __init__(self, position: (int, int), player: Player):
        self.player = player
        self.sprite = _set_sprite()

        self.position_board = Location(position)
        self.position_real_time = Location(position)

        self.sprite = _set_sprite(team)


    def _set_sprite(team: int) -> pygame.image:
        '''Returns a path to the correct png.'''
        if self.player.team == 0:
            piece_path = Path(CHESS_PIECES / 'White/Knight.png')
        else:
            piece_path = Path(CHESS_PIECES / 'Black/Knight.png')
        return pygame.image.load(piece_path)





class Bishop(Piece):

    ways_to_move = Piece._ways_to_move([('1|7', '1|7'), ('-1|-7', '-1|-7'), ('-1|-7', '1|7'), ('1|7', '-1|-7')])

    def __init__(self, position: (int, int), player: Player):
        self.player = player
        self.sprite = _set_sprite()

        self.position_board = Location(position)
        self.position_real_time = Location(position)

        self.sprite = _set_sprite(team)


    def _set_sprite(team: int) -> pygame.image:
        '''Returns a path to the correct png.'''
        if self.player.team == 0:
            piece_path = Path(CHESS_PIECES / 'White/Bishop.png')
        else:
            piece_path = Path(CHESS_PIECES / 'Black/Bishop.png')
        return pygame.image.load(piece_path)
    



class Rook(Piece):

    ways_to_move = Piece._ways_to_move([('0', '1|8'), ('0', '-1|-8'), ('1|8', '0'), ('-1|-8', '0')])

    def __init__(self, position: (int, int), player: Player):
        self.player = player
        self.sprite = _set_sprite()

        self.position_board = Location(position)
        self.position_real_time = Location(position)

        self.sprite = _set_sprite(team)


    def _set_sprite(team: int) -> pygame.image:
        '''Returns a path to the correct png.'''
        if self.player.team == 0:
            piece_path = Path(CHESS_PIECES / 'White/Rook.png')
        else:
            piece_path = Path(CHESS_PIECES / 'Black/Rook.png')
        return pygame.image.load(piece_path)




class Queen(Piece):

    ways_to_move = Piece._ways_to_move([('0', '1|8'), ('0', '-1|-8'), ('1|8', '0'), ('-1|-8', '0'), ('1|7', '1|7'), ('-1|-7', '-1|-7'), ('-1|-7', '1|7'), ('1|7', '-1|-7')])

    def __init__(self, position: (int, int), player: Player):
        self.player = player
        self.sprite = _set_sprite()

        self.position_board = Location(position)
        self.position_real_time = Location(position)

        self.sprite = _set_sprite(team)


    def _set_sprite(team: int) -> pygame.image:
        '''Returns a path to the correct png.'''
        if self.player.team == 0:
            piece_path = Path(CHESS_PIECES / 'White/Queen.png')
        else:
            piece_path = Path(CHESS_PIECES / 'Black/Queen.png')
        return pygame.image.load(piece_path)



class King(Piece):

    ways_to_move = Piece._ways_to_move([('0', '1'), ('0', '-1'), ('1', '0'), ('-1', '0'), ('1', '1'), ('-1', '-1'), ('1', '-1'), ('-1', '1')])

    def __init__(self, position: (int, int), player: Player):
        self.player = player
        self.sprite = _set_sprite()

        self.position_board = Location(position)
        self.position_real_time = Location(position)

        self.sprite = _set_sprite(team)


    def _set_sprite(team: int) -> pygame.image:
        '''Returns a path to the correct png.'''
        if self.player.team == 0:
            piece_path = Path(CHESS_PIECES / 'White/King.png')
        else:
            piece_path = Path(CHESS_PIECES / 'Black/King.png')
        return pygame.image.load(piece_path)
