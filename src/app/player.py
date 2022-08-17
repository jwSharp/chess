from config import *
# from board import *
# from accessory import *


##################
# Abstract Class #
##################
class Player:
    def __init__(self, name):
        self.name = name

    #def set_board(self, board: board.Board):
    #    self.board = board

    def move(self):
        pass


###########
# Players #
###########
class Human(Player):
    def __init__(self, name, rating=0):
        self.name = name
        
        #self.rating = rating
        self.board = None

class Computer(Player):
    def __init__(self, rating=0):
        self.name = 'CPU' # + str(rating)
        
        rating //= 100
        if rating < 6:
            self.eval_method = 'random'
            self.depth = 0
            
        elif rating < 10:
            self.eval_method = 'simple'
            self.depth = 0
        else:
            self.eval_method = 'complex'
            self.depth = 0
        
        self.board = None
        
    
    
