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

    a = """
    def __init__(self, name: str, rating: int, board: Board):
        self.name = name
        self.rating = rating

        self.board = board
        #self.team = team #?

    def move(self, destination: (int, int)):
        if not is_legal_move(self, Location(destination)):
            #TODO illegal move
            self.real_time_position = self.board_position
        else:
            #TODO if capture
            #TODO 
            pass
    
    def set_pieces(self, *pieces: Piece):
        self.pieces = pieces
    
    #TODO Event Listeners Here
    """