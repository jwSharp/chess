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
from piece import *
# from accessory import *


##################
# Abstract Class #
##################
class Player:
    def __init__(self, name):
        self.name = name
        self.color = ''

    def move(self):
        pass

    def reset_pieces(self):
        #TODO Delete old pieces
        
        # Create pieces
        pawns = [[Pawn((i, 6), 0, self.board.theme) for i in range(8)], [Pawn((i, 1), 1, self.board.theme) for i in range(8)]]
        rooks = [ [Rook((0, 7), 0, self.board.theme), Rook((7, 7), 0, self.board.theme)], [Rook((0, 0), 1, self.board.theme), Rook((7, 0), 1, self.board.theme)] ]
        knights = [ [Knight((1, 7), 0, self.board.theme), Knight((6, 7), 0, self.board.theme)], [Knight((1, 0), 1, self.board.theme), Knight((6, 0), 1, self.board.theme)] ]
        bishops = [[Bishop((2, 7), 0, self.board.theme), Bishop((5, 7), 0, self.board.theme)], [Bishop((2, 0), 1, self.board.theme), Bishop((5, 0), 1, self.board.theme)]]
        queen = [Queen((3, 7), 0, self.board.theme), Queen((3, 0), 1, self.board.theme)]
        king = [King((4, 7), 0, self.board.theme), King((4, 0), 1, self.board.theme)]

        self.manager.players[0].pieces = [rooks[0], bishops[0], knights[0], queen[0], king[0]] + pawns[0]
        self.manager.players[1].pieces = [rooks[1], bishops[1], knights[1], queen[1], king[1]] + pawns[1]
    
    def set_board(self, board):
        self.board = board
    
    def set_color(self, color):
        self.color = color


###########
# Players #
###########
class Human(Player):
    def __init__(self, name, rating=0):
        self.name = name
        
        self.rating = rating
        self.board = None
    
    def set_rating(self, rating):
        self.rating = rating

class Computer(Player):
    def __init__(self, color, rating=0):
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
    
    def move(self):
        '''Considers the evaluation method, depth of search, and they type of ai, and makes a move on the board.'''
        # Evaluation Method
        if self.eval_method == 'random':
            evaluate = self.random_evaluation()
        elif self.eval_method == 'simple':
            evaluate = self.simple_evaluation()
        elif self.eval_method == 'complex':
            evaluate = self.complex_evaluation()
    
    def random_evaluation(self) -> int:
        '''Includes which pieces are on the board.'''
        score = 0
        for row in self.board.bitboard:
            for square in row: # ranked from most common to least common
                # white
                if square == "P":
                    score += 1
                # black
                elif square == "p":
                    score -= 1
                # white
                elif square == "N":
                    score += 3
                elif square == "B":
                    score += 3
                # black
                elif square == "n":
                    score -= 3
                elif square == "b":
                    score -= 3
                # white
                elif square == "R":
                    score += 5
                # black
                elif square == "r":
                    score -= 5
                # white
                elif square == "Q":
                    score += 9
                # black
                elif square == "q":
                    score -= 9
        
        return score
    
    def simple_evaluation(self) -> int:
        '''Includes known advantages on the board.'''
        score = self.random_evaluation()
        
        return score
    def complex_evaluation(self) -> int:
        '''Includes maps to evaluate the structure of the board.'''
        score = self.simple_evaluation()
        
        return score
    
    
