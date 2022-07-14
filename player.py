import board.py

##################
# Abstract Class #
##################
class Player:
    def __init__(self, name: str, rating: int, board: Board):
        
    
    def move(self, destination: (int, int)):
        if not is_legal_move(self, Location(destination)):
            #TODO illegal move
            self.real_time_position = self.board_position
        else:
            #TODO if capture
            #TODO 

    #TODO Event Listeners Here
