import board.py
import pieces.py

##################
# Abstract Class #
##################
class Player:
    def __init__(self, name: str, rating: int, board: Board):
        self.name = name #! prompt for name
        self.rating = rating #! fetch rating

        self.board = board
        self.team = team

    def move(self, destination: (int, int)):
        if not is_legal_move(self, Location(destination)):
            #TODO illegal move
            self.real_time_position = self.board_position
        else:
            #TODO if capture
            #TODO 
    
    def set_pieces(self, *pieces: Piece):
        self.pieces = pieces
    
    #TODO Event Listeners Here
