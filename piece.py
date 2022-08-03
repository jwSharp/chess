import pygame

from config import *


class Piece:
    def __init__(self, pos: (int, int), turn: int, piece_name: str = None):
        self.piece_name = piece_name
        self.sprite = None
        self.image_path = None
        self.piece_moves = None
        self.piece_attacks = None

        self.start_pos, self.pos, self.current_pos = pos, pos, pos
        self.turn = turn
        
        self.captured = False
        self.move_count = 0
    
    def input(self, event: pygame.event):
        pass 
    
    def update(self):
        pass
    
    def draw(self, screen, blit_size: (int, int), panel):
        if self.image_path == None or self.pos == None:
            return
        self.sprite = pygame.image.load(self.image_path)
        x, y = self.pos
        x_pos = x * panel.width / 8 + (panel.x + 5)
        y_pos = y * panel.height / 8 + (panel.y + 5)
        self.sprite = pygame.transform.smoothscale(self.sprite, blit_size)
        screen.blit(self.sprite, (x_pos, y_pos))
        
    def move_piece(self, x, y, current_turn=0, other_pieces=[]) -> (int, int):
        if self.can_move(x, y, other_pieces) and self.turn == current_turn:
            self.current_pos = (x, y)
            self.pos = (x, y)
            self.move_count += 1
        else:
            self.pos = self.current_pos
        return self.current_pos
    
    def force_move(self, x, y, count_move = True, condition = True) -> (int, int):
        if condition:
            self.current_pos = (x, y)
            self.pos = (x, y)
            if count_move:
                self.move_count += 1
        return self.current_pos

    def can_move(self, target_x, target_y, other_pieces=[]) -> bool:
        if target_x < 0 or target_x > 7 or target_y < 0 or target_y > 7:
            return False
        return (target_x, target_y) in self.get_movement(other_pieces) or (target_x, target_y) in self.get_capturables(other_pieces)
    
    def get_movement(self, other_pieces):
        blocks = []
        self.capturables = []
        piece_positions = []
        
        if other_pieces != []:
            piece_positions = [p.current_pos for p in other_pieces]
        
        if self.piece_moves == None:
            return blocks
        
        list_moves = [list(move) for move in self.piece_moves]
        for move in list_moves:
            if self.current_pos == None:
                continue
            pos = [
                (self.current_pos[0] + movable_block[0], self.current_pos[1] - movable_block[1])
                for movable_block in self.movable_blocks(move)
            ]
            
            for p in pos:
                if p not in piece_positions:
                    blocks.append(p)
                else:
                    if (self.piece_attacks == None) and other_pieces[piece_positions.index(p)].turn != self.turn:
                        self.capturables.append(p)
                    break
            else:
                blocks += pos
                
        return blocks

    def get_capturables(self, other_pieces):
        if self.piece_attacks == None:
            self.get_movement(other_pieces)
            return self.capturables
        if other_pieces != []:
            piece_positions = [p.current_pos for p in other_pieces]
        else:
            piece_positions = []

        self.capturables = []
        attack_list = [list(attack) for attack in self.piece_attacks]
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
        
    def reflect_place(self):
        '''
            Mirrors the pieces position.
        '''
        if self.current_pos == None:
            return
        x = 7 - self.current_pos[0]
        y = 7 - self.current_pos[1]
        self.force_move(x, y, False)
        self.piece_moves = self.get_reflected_move(self.piece_moves)
        if self.piece_attacks != None:
            self.piece_attacks = self.get_reflected_move(self.piece_attacks)
        return (x, y)

    def get_reflected_move(self, old_move:[(str)]) -> [(str)]:
        '''
            Returns reflected movement of a piece!
        '''
        new_move = []
        for move in old_move:
            new_points = []
            for point in move:
                temp = point
                try:
                    temp = str(int(temp) * -1)
                except:
                    temp = str(int(temp.split('|')[0]) * -1) + '|' + str(int(temp.split('|')[1]) * -1)
                new_points.append(temp)
            new_move.append(new_points)
        return new_move

    def movable_blocks(self, area: list) -> [(int, int)]:
        '''
            Return all possible blocks as a list
        '''
        blocks = []
        pos_x = []
        pos_y = []
        if "|" in area[-2]:
            pos_x = self._get_n2n(n2n=area[-2], seperator="|")
        else:
            pos_x = [int(area[-2])]
        
        if "|" in area[-1]:
            pos_y = self._get_n2n(n2n=area[-1], seperator="|")
        else:
            pos_y = [int(area[-1])]
        
        for i in range(max([len(pos_x), len(pos_y)])):
            # print(pos_y)
            # print(self.piece_name)
            if pos_x == [] or pos_y == []:
                continue
            x = pos_x[-1] if pos_x.index(pos_x[-1]) < i else pos_x[i]
            y = pos_y[-1] if pos_y.index(pos_y[-1]) < i else pos_y[i]
            blocks.append((x, y))
        return blocks

    def destroy_piece(self):
        self.current_pos = None
        self.pos = None
        self.captured = True
    
    def _get_n2n(self, n2n: str, seperator: str):
        '''
            Returns List of numbers from n2n by seperating
            with the seperator.
            i.e: n2n = 1|5, seperator = '|' -> [1, 2, 3, 4, 5]
        '''
        nums = []
        n1, n2 = n2n.split(seperator)[0:2]
        if '-' in n2:
            n2 = str(int(n2) - 1) # for the loop, we need to add 1 to the second number
        else:
            n2 = str(int(n2) + 1)
            
        while n1 != n2:
            nums.append(int(n1))
            if int(n1) < int(n2):
                n1 = str(int(n1) + 1)
            else:
                n1 = str(int(n1) - 1)
        
        return nums

    def _set_sprite(self, turn, white_piece_name, black_piece_name):
        if turn == 0:
            self.image_path = WHITE_PIECES_PATH + white_piece_name
        else:
            self.image_path = BLACK_PIECES_PATH + black_piece_name

class Pawn(Piece):
    def __init__(self, pos, turn):
        super().__init__(pos, turn, "pawn")
        self.piece_moves = [('0', '1|2')] if turn == 0 else [('0', '-1|-2')]
        self.piece_attacks = [('-1', '1'), ('1', '1')] if turn == 0 else [('-1', '-1'), ('1', '-1')]
        self._set_sprite(turn, "pawn_top.png", "pawn_top.png")
    
    def update(self):
        if self.move_count > 0:
            self.piece_moves = [('0', '1')]
    
class Bishop(Piece):
    def __init__(self, pos, turn):
        super().__init__(pos, turn, "bishop")
        self.piece_moves = [("1|8", "1|8"), ("-1|-8", "-1|-8"), ("-1|-8", "1|8"), ("1|8", "-1|-8")]
        self._set_sprite(turn, "bishop_top.png", "bishop_top.png")

class Knight(Piece):
    def __init__(self, pos, turn):
        super().__init__(pos, turn, "knight")
        self.piece_moves = [("1", "2"), ("1", "-2"), ("-1", "2"), ("-1", "-2"), ("2", "1"), ("2", "-1"), ("-2", "-1"), ("-2", "1")]
        self._set_sprite(turn, "knight_top.png", "knight_top.png")

class Rook(Piece):
    def __init__(self, pos, turn):
        super().__init__(pos, turn, "rook")
        self.piece_moves = [("1|8", "0"), ("0", "1|8"), ("-1|-8", "0"), ("0", "-1|-8")]
        self._set_sprite(turn, "rook_top.png", "rook_top.png")

class Queen(Piece):
    def __init__(self, pos, turn):
        super().__init__(pos, turn, "queen")
        self.piece_moves = [("1|8", "0"), ("0", "1|8"), ("-1|-8", "0"), ("0", "-1|-8"), ("1|8", "1|8"), ("-1|-8", "-1|-8"), ("-1|-8", "1|8"), ("1|8", "-1|-8")]
        self._set_sprite(turn, "queen_top.png", "queen_top.png")
        
class King(Piece):
    def __init__(self, pos, turn):
        super().__init__(pos, turn, "king")
        self.piece_moves = [("1", "1"), ("1", "-1"), ("-1", "1"), ("-1", "-1"), ("1", "0"), ("0", "1"), ("-1", "0"), ("0", "-1")]
        self._set_sprite(turn, "king_top.png", "king_top.png")