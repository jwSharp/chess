import pygame
import math

from config import *
from piece import *

class Board:
    def __init__(self, manager):
        self.manager = manager
        self.current_turn = 0
        self.board_panel = None
        self.selected_block = None
        self.holding_piece = False
        self.selected_piece = None
        self._reset_selected()
        self._reset_pieces()

    def input(self, event, mouse_pos):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.selected_block = self.select_block(mouse_pos)
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # release left click to drop the piece
                self.drop_piece(mouse_pos[0], mouse_pos[1])
        elif pygame.mouse.get_pressed()[0]:  # if dragging, move the piece
            self.drag_piece(mouse_pos[0], mouse_pos[1])

    def draw(self, screen, panel: pygame.Rect):
        self.board_panel = panel
        sq_width = panel.width/8
        sq_height = panel.height/8
        for x in range(0,8):
            for y in range(0,8):
                sq_left = x * sq_width + panel.x
                sq_top = y * sq_height + panel.y
                sq = pygame.Rect(sq_left, sq_top, sq_width, sq_height)
                
                if (x + y) % 2 == 0:
                    pygame.draw.rect(screen, TAN, sq)
                else:
                    pygame.draw.rect(screen, BROWN, sq)
                if (x, y) in self.feedback_blocks:
                    pygame.draw.rect(SCREEN, self.feedback_blocks[(x, y)], sq, 5)
                elif (x, y) == self.selected_block:
                    pygame.draw.rect(SCREEN, LIGHT_GREEN, sq)
                if (x, y) in self.movable_blocks:
                    pygame.draw.rect(SCREEN, LIGHT_GREEN, sq, 6)
                elif (x, y) in self.capturables:
                    pygame.draw.rect(SCREEN, RED, sq, 3)
        
        for piece in self.pieces:
            piece.update()
            img_width = self.board_panel.width / 8 - 10
            img_height = self.board_panel.height / 8 - 10
            piece.draw(screen, (img_width, img_height), self.board_panel)
        
                    
    def select_block(self, pos: tuple):
        x, y = pos
        piece_positions = [i.current_pos for i in self.pieces]
        if self.drop_piece(x, y) == True:
            return
        x, y = self._get_grid_position(x, y)
        if (x, y) not in self.movable_blocks or (x, y) not in self.capturables:
            self._reset_selected()
        if (x >= 0 and x <= 7) and (y >= 0) and (y <= 7):
            self.selected_block = (x, y)
            if self.selected_block in piece_positions:
                if (self.pieces[piece_positions.index(self.selected_block)].turn == self.current_turn):
                    self.selected_piece = self.pieces[piece_positions.index(self.selected_block)]
                    self.movable_blocks = self.selected_piece.get_movement(self.pieces)
                    self.capturables = self.selected_piece.get_capturables(self.pieces)
                else:
                    self.draw_feedback(self.selected_block, RED, True)
                    self._reset_selected(True)
        return (x, y)

    def draw_feedback(self, xy: (int, int), color, reset_feedbacks):
        if reset_feedbacks:
            self.feedback_blocks = {xy: color}
        else:
            self.feedback_blocks[xy] = color

    def _get_grid_position(self, x: float, y: float):
        block_size = self.board_panel.width / 8
        x = int((x - self.board_panel.x) / block_size)
        y = int((y - self.board_panel.y) / block_size)
        return x, y
        
    def drag_piece(self, x, y):
        """
        Since draw_pieces renders the piece by its position, drag_piece changes
        the position of the held piece to the mouse position until drop_piece runs.
        """
        if self.board_panel == None:
            return
        block_size = self.board_panel.width / 8
        x = (x - self.board_panel.x) / block_size - 0.5
        y = (y - self.board_panel.y) / block_size - 0.5
        for i in self.pieces:
            if (self.selected_block == i.current_pos and not self.holding_piece and not i.captured):
                self.holding_piece = True
                self.selected_piece = i
                return
        if self.selected_piece is not None:
            self.pieces[self.pieces.index(self.selected_piece)].pos = (x, y)

    def drop_piece(self, x, y):
        """
        Calculates the grid point of the mouse position, after this method called
        it will set the piece position to the grid point. which will give the snap effect.
        """
        # converts x, y to grid position
        block_x, block_y = self._get_grid_position(x, y)
        if self.selected_piece == None:
            return False
        piece_positions = [p.current_pos for p in self.pieces]
        if (self.selected_piece.current_pos == self.pieces[self.pieces.index(self.selected_piece)].move_piece(block_x, block_y, self.current_turn, self.pieces) and self.selected_block != None):
            self.pieces[self.pieces.index(self.selected_piece)].move_piece(
                self.selected_block[0],
                self.selected_block[1],
                self.current_turn,
                self.pieces
            )
            return False

        if (block_x, block_y) in self.capturables:
            self.pieces[piece_positions.index((block_x, block_y))].destroy_piece()
            self.next_turn()
            self._reset_selected()
            return True
        
        if (block_x, block_y) != self.selected_block:
            self.next_turn()
            self._reset_selected()
            return True
        
        self._reset_selected()
        return False

    def next_turn(self):
        self.turns = [p.turn for p in self.pieces]
        if self.current_turn < max(self.turns):
            self.current_turn += 1
        else:
            self.current_turn = min(self.turns)
    
    def _reset_selected(self, keep_feedback=False):
        self.selected_piece = None
        self.holding_piece = False
        self.selected_block = None
        self.movable_blocks = []
        self.capturables = []
        if not keep_feedback:
            self.feedback_blocks = {}
            
    def _reset_pieces(self):
        pawn1 = [Pawn((0, 6), 0), Pawn((0, 1), 1)]
        pawn2 = [Pawn((1, 6), 0), Pawn((1, 1), 1)]
        pawn3 = [Pawn((2, 6), 0), Pawn((2, 1), 1)]
        pawn4 = [Pawn((3, 6), 0), Pawn((3, 1), 1)]
        pawn5 = [Pawn((4, 6), 0), Pawn((4, 1), 1)]
        pawn6 = [Pawn((5, 6), 0), Pawn((5, 1), 1)]
        pawn7 = [Pawn((6, 6), 0), Pawn((6, 1), 1)]
        pawn8 = [Pawn((7, 6), 0), Pawn((7, 1), 1)]
        rook1 = [Rook((0, 7), 0), Rook((0, 0), 1)]
        rook2 = [Rook((7, 7), 0), Rook((7, 0), 1)]
        knight1 = [Knight((1, 7), 0), Knight((1, 0), 1)]
        knight2 = [Knight((6, 7), 0), Knight((6, 0), 1)]
        bishop1 = [Bishop((2, 7), 0), Bishop((2, 0), 1)]
        bishop2 = [Bishop((5, 7), 0), Bishop((5, 0), 1)]
        queen = [Queen((3, 7), 0), Queen((3, 0), 1)]
        king = [King((4, 7), 0), King((4, 0), 1)]
        self.manager.players[0].pieces = [pawn1[0], pawn2[0], pawn3[0], pawn4[0], pawn5[0], pawn6[0], pawn7[0], pawn8[0], rook1[0], rook2[0], knight1[0], knight2[0], bishop1[0], bishop2[0], queen[0], king[0]]
        self.manager.players[1].pieces = [pawn1[1], pawn2[1], pawn3[1], pawn4[1], pawn5[1], pawn6[1], pawn7[1], pawn8[1], rook1[1], rook2[1], knight1[1], knight2[1], bishop1[1], bishop2[1], queen[1], king[1]]
        self.pieces = self.manager.players[0].pieces + self.manager.players[1].pieces