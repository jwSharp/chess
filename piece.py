import pygame
from constants import *

class Piece:
    def __init__(self, sprite: pygame.image, start_pos: (int, int), piece_name = 'pawn', turn: int = 0, piece_moves = [('0', '1'), ('F', '0', '1|2')], different_attacks = None):
        self.sprite = sprite
        self.start_pos, self.pos, self.current_pos = start_pos, start_pos, start_pos
        self.piece_name = piece_name
        self.turn = turn
        self.piece_moves = piece_moves
        self.different_attacks = different_attacks
        self.capturables = []
        self.captured = False
        self.move_count = 0
        self.check_count = 0
        
      
    def move_piece(self, x, y, current_turn = 0, other_pieces = []) -> (int, int):
        if self.can_move(x, y, other_pieces) and self.turn == current_turn:
            self.current_pos = (x, y)
            self.pos = (x, y)
            self.move_count += 1
        else:
            self.pos = self.current_pos
        return self.current_pos
    
    
    def force_move(self, x, y, condition = True) -> (int, int):
        if condition:
            self.current_pos = (x, y)
            self.pos = (x, y)
            self.move_count += 1
        return self.current_pos
    
    def can_move(self, target_x, target_y, other_pieces = []) -> bool:
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
            if 'F' in move and self.move_count != 0 or self.current_pos == None:
                continue
            pos = [(self.current_pos[0] + j[0], self.current_pos[1] - j[1]) for j in self.movable_blocks(move)]
            for p in pos:
                if p not in piece_positions:
                    blocks.append(p)
                else:
                    if self.different_attacks == None and other_pieces[piece_positions.index(p)].turn != self.turn:
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
            if 'F' in attack and self.move_count != 0 or self.current_pos == None:
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
        return [(self.current_pos[0] + j[0], self.current_pos[1] - j[1]) for j in self.movable_blocks(move)]
    
    def movable_blocks(self, area) -> [(int, int)]:
        blocks = []
        pos_x = []
        pos_y = []
        if '|' in area[-2]:
            pos_x = self._get_n2n(area[-2], '|')
        else:
            pos_x = [int(area[-2])]
        
        if '|' in area[-1]:
            pos_y = self._get_n2n(area[-1], '|')
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
    
    def set_movement(self, movement:[(str)]):
        self.piece_moves = movement
      
    def add_movement(self, move_add:[(str)]):
        self.piece_moves += move_add
    
    def reflect_place(self):
        if self.current_pos == None:
            return
        x = 7 - self.current_pos[0]
        y = 7 - self.current_pos[1]
        self.piece_moves = self.get_reflected_move(self.piece_moves)
        if self.different_attacks != None:
            self.different_attacks = self.get_reflected_move(self.different_attacks)
        return (x, y)

    def get_reflected_move(self, old_move:[(str)]) -> [(str)]:
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
                    temp = str(int(temp.split('|')[0]) * -1) + '|' + str(int(temp.split('|')[1]) * -1)
                new_points.append(temp)
            new_move.append(new_points)
        return new_move
    
    ''' Get all the numbers from n | n 
        i.e: 1 | 5 => [1, 2, 3, 4, 5] '''
    def _get_n2n(self, n2n: str, seperator: str):
      nums = []
      n1, n2 = n2n.split(seperator)[0:2]
      while n1 != n2:
        nums.append(int(n1))
        if int(n1) < int(n2):
            n1 = str(int(n1) + 1)
        else:
            n1 = str(int(n1) - 1)
      return nums