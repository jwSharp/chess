#from board import *

##################
# Abstract Class #
##################
class Player:
    def __init__(self, name):
        self.name = name

    #def set_board(self, board: board.Board):
    #    self.board = board


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
        self.name = 'CPU -' # + str(rating)
        #self.rating = rating
        self.board = None