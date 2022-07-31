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
        return True

class Pawn(Piece):
    def __init__(self, pos, turn):
        super().__init__(pos, turn)
        self.piece_moves = [('0', '1|2')]
        self.piece_attacks = [('-1', '1'), ('1', '1')]
    
    def update(self):
        if self.move_count > 0:
            self.piece_moves = [('0', '1')]