import pygame
from pathlib import Path

import config
import player

##################
# Abstract Class #
##################
class Piece:
    '''Represents a game piece.'''
    def __init__(self, start_pos: (int, int)):
        self.piece_name = None
        self.sprite = None
        self.piece_moves = None

        self.start_pos, self.pos, self.current_pos = start_pos, start_pos, start_pos
        self.turn = 0
        
        self.capturables = []
        self.captured = False
        self.check_count = 0

    def move_piece(self, x, y, current_turn=0, other_pieces=[]) -> (int, int):
        if self.can_move(x, y, other_pieces) and self.turn == current_turn:
            self.current_pos = (x, y)
            self.pos = (x, y)
        else:
            self.pos = self.current_pos
        return self.current_pos

    def force_move(self, x, y, count_move=True, condition=True) -> (int, int):
        if condition:
            self.current_pos = (x, y)
            self.pos = (x, y)
        return self.current_pos

    def can_move(self, target_x, target_y, other_pieces=[]) -> bool:
        if target_x < 0 or target_x > 7 or target_y < 0 or target_y > 7:
            return False
        if (target_x, target_y) in self.get_movement(other_pieces):
            return True
        return (target_x, target_y) in self.get_capturables(other_pieces)

    def get_movement(self, other_pieces) -> [(int, int)]:
        blocks = []
        self.capturables = []
        if other_pieces != []:
            piece_positions = [p.current_pos for p in other_pieces]
        else:
            piece_positions = []

        for move in [list(move) for move in self.piece_moves]:
            if self.current_pos == None:
                continue
            pos = [
                (self.current_pos[0] + j[0], self.current_pos[1] - j[1])
                for j in self.movable_blocks(move)
            ]
            for p in pos:
                if p not in piece_positions:
                    blocks.append(p)
                else:
                    if (
                        self.different_attacks == None
                        and other_pieces[piece_positions.index(p)].turn != self.turn
                    ):
                        self.capturables.append(p)
                    break
            else:
                blocks += pos
        return blocks

    def get_capturables(self, other_pieces) -> [(int, int)]:
        if self.different_attacks == None:
            self.get_movement(other_pieces)
            return self.capturables
        if other_pieces != []:
            piece_positions = [p.current_pos for p in other_pieces]
        else:
            piece_positions = []

        self.capturables = []
        attack_list = [list(attack) for attack in self.different_attacks]
        for attack in attack_list:
            if self.current_pos == None:
                continue
            pos = self.get_movable_blocks(attack)
            for p in pos:
                if p in piece_positions:
                    piece = other_pieces[piece_positions.index(p)]
                    if piece.turn != self.turn:
                        self.capturables.append(p)
                    break
        return self.capturables

    def get_movable_blocks(self, move: str):
        return [
            (self.current_pos[0] + j[0], self.current_pos[1] - j[1])
            for j in self.movable_blocks(move)
        ]

    def movable_blocks(self, area) -> [(int, int)]:
        blocks = []
        pos_x = []
        pos_y = []
        if "|" in area[-2]:
            pos_x = self._get_n2n(area[-2], "|")
        else:
            pos_x = [int(area[-2])]

        if "|" in area[-1]:
            pos_y = self._get_n2n(area[-1], "|")
        else:
            pos_y = [int(area[-1])]

        ## Append all possible blocks to the list ##
        for i in range(max([len(pos_x), len(pos_y)])):
            x = pos_x[-1] if pos_x.index(pos_x[-1]) < i else pos_x[i]
            y = pos_y[-1] if pos_y.index(pos_y[-1]) < i else pos_y[i]
            blocks.append((x, y))
        return blocks

    def destroy_piece(self):
        self.current_pos = None
        self.pos = None
        self.captured = True

    def set_movement(self, movement: [(str)]):
        self.piece_moves = movement

    def add_movement(self, move_add: [(str)]):
        self.piece_moves += move_add

    def reflect_place(self):
        '''Needs documentation.'''
        if self.current_pos == None:
            return
        x = 7 - self.current_pos[0]
        y = 7 - self.current_pos[1]
        self.force_move(x, y, False)
        self.piece_moves = self.get_reflected_move(self.piece_moves)
        if self.different_attacks != None:
            self.different_attacks = self.get_reflected_move(self.different_attacks)
        return (x, y)

    def get_reflected_move(self, old_move: [(str)]) -> [(str)]:
        """ Get all the numbers from n | n 
        i.e: 1 | 5 => [1, 2, 3, 4, 5] """
        new_move = []
        for move in old_move:
            new_points = []
            for point in move:
                temp = point
                try:
                    temp = str(int(temp) * -1)
                except:
                    temp = (
                        str(int(temp.split("|")[0]) * -1)
                        + "|"
                        + str(int(temp.split("|")[1]) * -1)
                    )
                new_points.append(temp)
            new_move.append(new_points)
        return new_move


    def _get_n2n(self, n2n: str, seperator: str):
        '''Needs documentation.'''
        nums = []
        n1, n2 = n2n.split(seperator)[0:2]
        while n1 != n2:
            nums.append(int(n1))
            if int(n1) < int(n2):
                n1 = str(int(n1) + 1)
            else:
                n1 = str(int(n1) - 1)
        return nums


#################################


class Pawn(Piece):
    def __init__(self, start_pos: (int, int), turn: int):
        self.piece_name = 'pawn'
        if self.player.team == 0:
            self.sprite = pygame.image.load(Path(CHESS_PIECES / 'White/Pawn/Top/white_pawn_top.png'))
            self.piece_moves = [('0', '1'), ('F', '0', '1|3')] #! Remove 'F'?
            self.different_attacks = [('1', '1'), ('-1', '1')]
        else:
            self.sprite = pygame.image.load(Path(CHESS_PIECES / 'Black/Pawn/Top/black_pawn_top.png'))
            self.piece_moves = [('0', '-1'), ('F', '0', '-1|-3')] #! Remove 'F'?
            self.different_attacks = [('1', '-1'), ('-1', '-1')]

        self.start_pos, self.pos, self.current_pos = start_pos, start_pos, start_pos
        self.turn = 0
        
        self.capturables = []
        self.captured = False
        self.has_moved = False
        self.check_count = 0
    
    def move_piece(self, x, y, current_turn=0, other_pieces=[]) -> (int, int):
        if self.can_move(x, y, other_pieces) and self.turn == current_turn:
            self.current_pos = (x, y)
            self.pos = (x, y)
            self.has_moved = True
        else:
            self.pos = self.current_pos
        return self.current_pos
    
    def force_move(self, x, y, count_move=True, condition=True) -> (int, int):
        if condition:
            self.current_pos = (x, y)
            self.pos = (x, y)
            self.has_moved = True
        return self.current_pos
    
    def get_movement(self, other_pieces) -> [(int, int)]:
        blocks = []
        self.capturables = []
        if other_pieces != []:
            piece_positions = [p.current_pos for p in other_pieces]
        else:
            piece_positions = []

        for move in [list(move) for move in self.piece_moves]:
            if 'F' in move and not self.has_moved or self.current_pos == None:
                continue
            pos = [
                (self.current_pos[0] + j[0], self.current_pos[1] - j[1])
                for j in self.movable_blocks(move)
            ]
            for p in pos:
                if p not in piece_positions:
                    blocks.append(p)
                else:
                    if (
                        self.different_attacks == None
                        and other_pieces[piece_positions.index(p)].turn != self.turn
                    ):
                        self.capturables.append(p)
                    break
            else:
                blocks += pos
        return blocks
    
    def get_capturables(self, other_pieces) -> [(int, int)]:
        if self.different_attacks == None:
            self.get_movement(other_pieces)
            return self.capturables
        if other_pieces != []:
            piece_positions = [p.current_pos for p in other_pieces]
        else:
            piece_positions = []

        self.capturables = []
        attack_list = [list(attack) for attack in self.different_attacks]
        for attack in attack_list:
            if 'F' in attack and not self.has_moved or self.current_pos == None:
                continue
            pos = self.get_movable_blocks(attack)
            for p in pos:
                if p in piece_positions:
                    piece = other_pieces[piece_positions.index(p)]
                    if piece.turn != self.turn:
                        self.capturables.append(p)
                    break
        return self.capturables
    
    def get_reflected_move(self, old_move: [(str)]) -> [(str)]:
        '''Get all the numbers from n | n 
        i.e: 1 | 5 => [1, 2, 3, 4, 5]'''
        new_move = []
        for move in old_move:
            new_points = []
            for point in move:
                if point == 'F':
                    new_points.append(point)
                    continue
                temp = point
                try:
                    temp = str(int(temp) * -1)
                except:
                    temp = (
                        str(int(temp.split("|")[0]) * -1)
                        + "|"
                        + str(int(temp.split("|")[1]) * -1)
                    )
                new_points.append(temp)
            new_move.append(new_points)
        return new_move


class Knight(Piece):
    def __init__(self, start_pos: (int, int), team: int):
        self.piece_name = 'knight'
        if self.player.team == 0:
            self.sprite = pygame.image.load(Path(CHESS_PIECES / 'White/Knight/Top/white_knight_top.png'))
        else:
            self.sprite = pygame.image.load(Path(CHESS_PIECES / 'Black/Knight/Top/black_knight_top.png'))
        self.piece_moves = [('1', '2'), ('-1', '2'), ('2', '1'), ('-2', '1'), ('2', '-1'), ('-2', '-1'), ('1', '-2'), ('-1', '-2')]

        self.start_pos, self.pos, self.current_pos = start_pos, start_pos, start_pos
        self.turn = 0
        
        self.capturables = []
        self.captured = False
        self.check_count = 0

class Bishop(Piece):
    def __init__(self, start_pos: (int, int), team: int):
        self.piece_name = 'bishop'
        if self.player.team == 0:
            self.sprite = pygame.image.load(Path(CHESS_PIECES / 'White/Bishop/Top/white_bishop_top.png'))
        else:
            self.sprite = pygame.image.load(Path(CHESS_PIECES / 'Black/Bishop/Top/black_bishop_top.png'))
        self.piece_moves = [('1|7', '1|7'), ('-1|-7', '-1|-7'), ('-1|-7', '1|7'), ('1|7', '-1|-7')]

        self.start_pos, self.pos, self.current_pos = start_pos, start_pos, start_pos
        self.turn = 0
        
        self.capturables = []
        self.captured = False
        self.check_count = 0


class Rook(Piece):
    def __init__(self, start_pos: (int, int), team: int):
        self.piece_name = 'rook'
        if self.player.team == 0:
            self.sprite = pygame.image.load(Path(CHESS_PIECES / 'White/Rook/Top/white_rook_top.png'))
        else:
            self.sprite = pygame.image.load(Path(CHESS_PIECES / 'Black/Rook/Top/black_rook_top.png'))
        self.piece_moves = [('0', '1|8'), ('0', '-1|-8'), ('1|8', '0'), ('-1|-8', '0')]

        self.start_pos, self.pos, self.current_pos = start_pos, start_pos, start_pos
        self.turn = 0
        
        self.capturables = []
        self.captured = False
        self.has_moved = False
        self.check_count = 0
    
    def move_piece(self, x, y, current_turn=0, other_pieces=[]) -> (int, int):
        if self.can_move(x, y, other_pieces) and self.turn == current_turn:
            self.current_pos = (x, y)
            self.pos = (x, y)
            self.has_moved = True
        else:
            self.pos = self.current_pos
        return self.current_pos
    
    def force_move(self, x, y, count_move=True, condition=True) -> (int, int):
        if condition:
            self.current_pos = (x, y)
            self.pos = (x, y)
            self.has_moved = True
        return self.current_pos
    
    def get_movement(self, other_pieces) -> [(int, int)]:
        blocks = []
        self.capturables = []
        if other_pieces != []:
            piece_positions = [p.current_pos for p in other_pieces]
        else:
            piece_positions = []

        for move in [list(move) for move in self.piece_moves]:
            if not self.has_moved or self.current_pos == None:
                continue
            pos = [
                (self.current_pos[0] + j[0], self.current_pos[1] - j[1])
                for j in self.movable_blocks(move)
            ]
            for p in pos:
                if p not in piece_positions:
                    blocks.append(p)
                else:
                    if (
                        self.different_attacks == None
                        and other_pieces[piece_positions.index(p)].turn != self.turn
                    ):
                        self.capturables.append(p)
                    break
            else:
                blocks += pos
        return blocks

    def get_capturables(self, other_pieces) -> [(int, int)]:
        if self.different_attacks == None:
            self.get_movement(other_pieces)
            return self.capturables
        if other_pieces != []:
            piece_positions = [p.current_pos for p in other_pieces]
        else:
            piece_positions = []

        self.capturables = []
        attack_list = [list(attack) for attack in self.different_attacks]
        for attack in attack_list:
            if not self.has_moved or self.current_pos == None:
                continue
            pos = self.get_movable_blocks(attack)
            for p in pos:
                if p in piece_positions:
                    piece = other_pieces[piece_positions.index(p)]
                    if piece.turn != self.turn:
                        self.capturables.append(p)
                    break
        return self.capturables


class Queen(Piece):
    def __init__(self, start_pos: (int, int), team: int):
        self.piece_name = 'queen'
        if self.player.team == 0:
            self.sprite = pygame.image.load(Path(CHESS_PIECES / 'White/Queen/Top/white_queen_top.png'))
        else:
            self.sprite = pygame.image.load(Path(CHESS_PIECES / 'Black/Queen/Top/black_queen_top.png'))
        self.piece_moves = [('0', '1|8'), ('0', '-1|-8'), ('1|8', '0'), ('-1|-8', '0'), ('1|7', '1|7'), ('-1|-7', '-1|-7'), ('-1|-7', '1|7'), ('1|7', '-1|-7')]

        self.start_pos, self.pos, self.current_pos = start_pos, start_pos, start_pos
        self.turn = 0
        
        self.capturables = []
        self.captured = False
        self.check_count = 0



class King(Piece):
    def __init__(self, start_pos: (int, int), team: int):
        self.piece_name = 'king'
        if self.player.team == 0:
            self.sprite = pygame.image.load(Path(CHESS_PIECES / 'White/King/Top/white_king_top.png'))
        else:
            self.sprite = pygame.image.load(Path(CHESS_PIECES / 'Black/King/Top/black_king_top.png'))
        self.piece_moves = [('0', '1'), ('0', '-1'), ('1', '0'), ('-1', '0'), ('1', '1'), ('-1', '-1'), ('1', '-1'), ('-1', '1')]

        self.start_pos, self.pos, self.current_pos = start_pos, start_pos, start_pos
        self.turn = 0
        
        self.capturables = []
        self.captured = False
        self.has_moved = False
        self.check_count = 0
    
    def move_piece(self, x, y, current_turn=0, other_pieces=[]) -> (int, int):
        if self.can_move(x, y, other_pieces) and self.turn == current_turn:
            self.current_pos = (x, y)
            self.pos = (x, y)
            self.has_moved = True
        else:
            self.pos = self.current_pos
        return self.current_pos
    
    def force_move(self, x, y, count_move=True, condition=True) -> (int, int):
        if condition:
            self.current_pos = (x, y)
            self.pos = (x, y)
            self.has_moved = True
        return self.current_pos
    
    def get_movement(self, other_pieces) -> [(int, int)]:
        blocks = []
        self.capturables = []
        if other_pieces != []:
            piece_positions = [p.current_pos for p in other_pieces]
        else:
            piece_positions = []

        for move in [list(move) for move in self.piece_moves]:
            if not self.has_moved or self.current_pos == None:
                continue
            pos = [
                (self.current_pos[0] + j[0], self.current_pos[1] - j[1])
                for j in self.movable_blocks(move)
            ]
            for p in pos:
                if p not in piece_positions:
                    blocks.append(p)
                else:
                    if (
                        self.different_attacks == None
                        and other_pieces[piece_positions.index(p)].turn != self.turn
                    ):
                        self.capturables.append(p)
                    break
            else:
                blocks += pos
        return blocks

    def get_capturables(self, other_pieces) -> [(int, int)]:
        if self.different_attacks == None:
            self.get_movement(other_pieces)
            return self.capturables
        if other_pieces != []:
            piece_positions = [p.current_pos for p in other_pieces]
        else:
            piece_positions = []

        self.capturables = []
        attack_list = [list(attack) for attack in self.different_attacks]
        for attack in attack_list:
            if not self.has_moved or self.current_pos == None:
                continue
            pos = self.get_movable_blocks(attack)
            for p in pos:
                if p in piece_positions:
                    piece = other_pieces[piece_positions.index(p)]
                    if piece.turn != self.turn:
                        self.capturables.append(p)
                    break
        return self.capturables