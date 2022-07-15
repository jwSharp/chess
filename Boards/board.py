import pygame
import math

import constants.py
import player.py

class Board:
    def __init__(self, screen: pygame.surface, panel: pygame.Rect, *players: player.Player):
        self.screen = screen #? existing already?
        self.board_panel = panel #? .width?

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
                
                #! if( there exists a piece on this square) then _draw_piece(self, piece)
    

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
    
    

