'''
Modern | Retro Chess - A chess program focused on providing a simple solution to online simultaneous exhibitions.
Copyright (C) 2022 Society of Overthinkers

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''

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
        
    
    
