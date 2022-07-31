import pygame
from config import *

class Piece:
    def __init__(self, pos: (int, int), turn: int):
        self.piece_name = None
        self.sprite = None
        self.piece_moves = None
        self.piece_attacks = self.piece_moves

        self.start_pos, self.pos, self.current_pos = pos, pos, pos
        self.turn = 0
        
        self.captured = False
        self.move_count = 0
    
    def input(self, event: pygame.event):
        x, y = pygame.mouse.get_pos()
        pass # TODO: Add events to drag the piece and drop it
    
    def update(self):
        pass
    
    def draw(self, screen):
        if self.sprite != None and self.pos != None:
            screen.blit(self.sprite, self.pos)
        
    def move_piece(self, x, y, current_turn=0, other_pieces=[]) -> (int, int):
        if self.can_move(x, y, other_pieces) and self.turn == current_turn:
            self.current_pos = (x, y)
            self.pos = (x, y)
        else:
            self.pos = self.current_pos
        return self.current_pos

    def can_move(self, target_x, target_y, other_pieces=[]) -> bool:
        if target_x < 0 or target_x > 7 or target_y < 0 or target_y > 7:
            return False
        return (target_x, target_y) in self.get_movement(other_pieces)
    
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

    '''
        Return all possible blocks as a list
    '''
    def movable_blocks(self, area: list) -> [(int, int)]:
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
        
        for i in range(max([len(pos_x), len(pos_y)])):
            x = pos_x[-1] if pos_x.index(pos_x[-1]) < i else pos_x[i]
            y = pos_y[-1] if pos_y.index(pos_y[-1]) < i else pos_y[i]
            blocks.append((x, y))
        return blocks
    
    '''
        Returns List of numbers from n2n by seperating
        with the seperator.
        i.e: n2n = 1|5, seperator = '|' -> [1, 2, 3, 4, 5]
    '''
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

class Pawn(Piece):
    def __init__(self, pos, turn):
        super().__init__(pos, turn)
        self.piece_moves = [('0', '1|2')]
        self.piece_attacks = [('-1', '1'), ('1', '1')]
    
    def update(self):
        if self.move_count > 0:
            self.piece_moves = [('0', '1')]
