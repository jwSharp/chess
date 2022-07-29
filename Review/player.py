from board import *

##################
# Abstract Class #
##################
class Player:
    def __init__(self):
        self.name = name

    def set_board(self, board: board.Board):
        self.board = board


###########
# Players #
###########
class Human(Player):
    player_count = 0

    def __init__(self, name='', rating=0):
        if name:
            self.name = name
        else:
            self.name = 'Player ' + player_count
            player_count += 1
        #self.rating = rating
        self.board = None


class Computer(Player):
    def __init__(self, rating=0):
        self.name = 'CPU' + rating
        #self.rating = rating
        self.board = None