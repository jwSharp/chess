import pygame
import math

import constants.py
import player.py

class Board:
    # list with piece locations [][]

    def __init__(self, screen: pygame.surface, panel: pygame.Rect, *players: player.Player):
        self.screen = screen #? existing already?
        self.board_panel = panel # Board panel is to manage boards width and height 
        #! this is for render board on panel instead of on screen

        for player in players: #! random order functionality
            self.players.append(player)
        
        
        _new_game(self)


    def draw(self):
        '''Draws board, letters/numbers arround the board, and pieces on the board.'''
        _draw_board(self)
        _draw_letters(self)
        _draw_pieces(self)
    


    def _new_game(self): #? game.py? - contains movement, turns etc...
        '''Resets the pieces to their starting squares.'''
        self.turn = 0
        
        self.selected_block = None
        self.selected_piece = None
        self.holding_piece = False

        _add_sets()

    def _add_sets(self, ref_piece: piece.Piece, positions: (str, str) = ('0|7', '6')):
        piece_positions = [i.current_pos for i in self.pieces]
        pos_x = [x for x in range(min([int(j) for j in positions[0].split('|')]), max([int(j) for j in positions[0].split('|')]) + 1)]
        pos_y = [y for y in range(min([int(j) for j in positions[1].split('|')]), max([int(j) for j in positions[1].split('|')]) + 1)]
        for l in range(max([len(pos_x), len(pos_y)])):
            x = pos_x[-1] if pos_x.index(pos_x[-1]) < l else pos_x[l]
            y = pos_y[-1] if pos_y.index(pos_y[-1]) < l else pos_y[l]
            if (x, y) not in piece_positions:
                self.pieces.append(piece.Piece(ref_piece.sprite, (x, y), ref_piece.piece_name, ref_piece.turn, ref_piece.piece_moves, ref_piece.different_attacks))

    def _draw_board(self):
        block_size = self.board_panel.width/8
        for x in range(8):
            for y in range(8):
                x_pos = x * block_size + self.board_panel.x
                y_pos = y * block_size + self.board_panel.y
                r = pygame.Rect(x_pos, y_pos, block_size, block_size)
                
                if (x + y) % 2 == 1:
                    pygame.draw.rect(self.screen, constants.BLACK, r)
                else:
                    pygame.draw.rect(self.screen, constants.WHITE, r)

                if (x, y) in self.feedback_blocks:
                    pygame.draw.rect(self.screen, self.feedback_blocks[(x, y)], r, 5) #? why 3 and 5?
                elif (x, y) == self.selected_block:
                    pygame.draw.rect(self.screen, constants.LIGHT_GREEN_230, r)
                
                if (x, y) in self.movable_blocks:
                    pygame.draw.rect(self.screen, constants.LIGHT_GREEN_230,r, 3)
                
                if (x, y) in self.capturables:
                    pygame.draw.rect(self.screen, constants.SALMON, r, 3)
                
                if (x, y) in self.piece_positions:
                    # piece_index = self.piece_positions.index(self.selected_block)
                    pass # draw -> self.pieces[piece_index]

    def _draw_letters(self, text_color = (0, 0, 0, 255)):
        letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
        block_size = self.board_panel.width/8
        for i in range(8):
            x_pos_left = self.board_panel.x - block_size/2
            x_pos_right = self.board_panel.x + self.board_panel.width + block_size/2
            y_pos_top = self.board_panel.y + self.board_panel.height + block_size/2
            y_pos_bottom = self.board_panel.y - block_size/2
            gap = i * block_size + self.board_panel.y + block_size/2 #! isnt this const
            
            letter_label = pygame.font.SysFont('Arial', 18).render(letters[i], False, text_color) #! move to constants
            number_label = pygame.font.SysFont('Arial', 18).render(str(8 - i), False, text_color) #! move to constants
            
            self.screen.blit(letter_label, (gap, y_pos_top))
            self.screen.blit(letter_label, (gap, y_pos_bottom))
            self.screen.blit(number_label, (x_pos_left, gap))
            self.screen.blit(number_label, (x_pos_right, gap))

    def _draw_pieces(self): #! vs. draw piece when iterating through squares?
        image = None
        holded_image = None
        h_x, h_y = 0, 0 #?
        for piece in self.pieces:
            if piece.pos == None:
                continue
            
            x, y = piece.pos
            x_pos = x * self.board_panel.width/8 + (self.board_panel.x + 5)
            y_pos = y * self.board_panel.height/8 + (self.board_panel.y + 5)
            image = piece.sprite
            
            if self.selected_piece == piece and self.selected_piece.pos != self.selected_piece.current_pos:
                holded_image = image
                holded_image = pygame.transform.scale(holded_image, (holded_image.get_width() * 1.2, holded_image.get_height() * 1.2))
                h_x, h_y = x_pos - 8, y_pos - 10
            else:
                self.screen.blit(image, (x_pos, y_pos))
        
        if holded_image != None:
            self.screen.blit(holded_image, (h_x, h_y))
    
    ###################
    #### Unchecked ####
      #             #
         #       #
            # #
             #

             
    def drag_piece(self, x, y):
        x = (x / self.board_panel.width * 8) - (self.screen.get_width()) / self.board_panel.width - 1
        y = (y / self.board_panel.height * 8) - (self.screen.get_height()) / self.board_panel.height - 1
        for i in self.pieces:
            if self.selected_block == i.current_pos and not self.holding_piece:
                self.holding_piece = True
                self.selected_piece = i
                return
        if self.selected_piece is not None:
            self.pieces[self.pieces.index(self.selected_piece)].pos = (x, y)
    
    def drop_piece(self, x, y):
        # converts x, y to grid position
        block_x = int(x / self.board_panel.width * 8) - int((self.screen.get_width()) / self.board_panel.width) - 1
        block_y = int(y / self.board_panel.height * 8) - int((self.screen.get_height()) / self.board_panel.height) - 1
        if self.selected_piece == None:
            return
        
        piece_positions = [p.current_pos for p in self.pieces]
        
        if self.selected_piece.current_pos == self.pieces[self.pieces.index(self.selected_piece)].move_piece(block_x, block_y, self.pieces, self.current_turn) and self.selected_block != None:
            self.pieces[self.pieces.index(self.selected_piece)].move_piece(self.selected_block[0], self.selected_block[1], self.pieces, self.current_turn)
            return
    
        if (block_x, block_y) in self.capturables:
            self.pieces[piece_positions.index((block_x, block_y))].destroy_piece()
            self.movable_blocks = []
            self.capturables = []
            self.selected_piece = None
            self.holding_piece = False
            self.selected_block = None
            self.next_turn()
            
        if (block_x, block_y) != self.selected_block:
            self.selected_piece = None
            self.holding_piece = False
            self.selected_block = None
            self.movable_blocks = []
            self.capturables = []
            self.next_turn()



    def select_block(self, x: float, y: float):
        piece_positions = [i.current_pos for i in self.pieces]
        x = int(x / self.board_panel.width * 8) - int((self.screen.get_width()) / self.board_panel.width) - 1
        y = int(y / self.board_panel.height * 8) - int((self.screen.get_height()) / self.board_panel.height) - 1
        
        if self.selected_block != None and self.selected_block in self.feedback_blocks:
            self.feedback_blocks.pop(self.selected_block)
        if self.selected_piece != None and (x, y) not in self.capturables and (x, y) not in self.movable_blocks:
            self.selected_piece = None
            self.holding_piece = False
            self.selected_block = None
            self.movable_blocks = []
            self.capturables = []
        if (x >= 0 and x <= 7) and (y >= 0) and (y <= 7):
            self.selected_block = (x, y)
            if self.selected_piece != None and self.selected_block in self.capturables:
                self.pieces[self.pieces.index(self.selected_piece)].move_piece(x, y, self.pieces, self.current_turn)
                self.pieces[piece_positions.index(self.selected_block)].destroy_piece()
                self.selected_piece = None
                self.holding_piece = False
                self.selected_block = None
                self.movable_blocks = []
                self.capturables = []
                self.next_turn()
            elif self.selected_block in piece_positions:
                if self.pieces[piece_positions.index(self.selected_block)].turn == self.current_turn:
                    self.selected_piece = self.pieces[piece_positions.index(self.selected_block)]
                    self.movable_blocks = self.selected_piece.get_movement(self.pieces)
                    self.capturables = self.selected_piece.get_capturables(self.pieces)
                else:
                    self.draw_feedback(self.selected_block, (255, 0, 0, 230), True)
        if self.selected_piece != None and (x, y) in self.movable_blocks:
            self.pieces[self.pieces.index(self.selected_piece)].move_piece(x, y, self.pieces, self.current_turn)
            self.selected_piece = None
            self.holding_piece = False
            self.selected_block = None
            self.movable_blocks = []
            self.capturables = []
            self.next_turn()
        return (x, y)
    

                
    def next_turn(self):
        max_turn = max([p.turn for p in self.pieces])
        min_turn = min([p.turn for p in self.pieces])
        if self.current_turn < max_turn:
            self.current_turn += 1
        else:
            self.current_turn = min_turn
    

    
    def draw_feedback(self, xy: (int, int), color, reset_feedbacks):
        if reset_feedbacks:
            self.feedback_blocks = {xy:color}
        else:
            self.feedback_blocks[xy] = color


