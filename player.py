import board
#import pieces

##################
# Abstract Class #
##################
class Player:
    def __init__(self, name: str, rating = 0):
        self.name = name
        self.rating = rating

        self.board = None
        #self.team = team #?

    def set_board(self, board: board.Board):
        self.board = board