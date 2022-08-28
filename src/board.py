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

import pygame
import random

from config import *
from accessory import Timer # useful?
from player import Human, Computer
from piece import King, Queen, Rook, Bishop, Knight, Pawn


class Board:
    def __init__(self, manager):
        self.manager = manager
        
        # Set up players
        self.players = self.manager.players[:2]
        for player in self.players:
            player.set_board(self)
            player.reset_pieces
        
        # set default view and themes
        self.view = 'top'
        #self.theme = 'light'
        
        # reset the board
        self._reset_board()
        
        self.rotation = all(type(player) is Human for player in self.manager.players) #TODO remove feature?
        self.is_board_to_rotate = False
        
        self.blocks = [(x, y) for x in range(8) for y in range(8)]
        
        self.panel = None
        self.check_state = None
        
        self.delay = 1

        self._reset_selected()
        self._reset_pieces()
    
    def _reset_board(self):
        '''Resets the board to a fresh new game.'''
        # Game State
        self.current_turn = 0
        self.game_state = "Make the First Move"
        
        # Reset bitboard
        self.bitboard = [ # Row (1 - 8), Column (A - H)
                        ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R'],
                        ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
                        ['',  '',  '',  '',  '',  '',  '',  ''],
                        ['',  '',  '',  '',  '',  '',  '',  ''],
                        ['',  '',  '',  '',  '',  '',  '',  ''],
                        ['',  '',  '',  '',  '',  '',  '',  ''],
                        ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
                        ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r']
                        ]
        self.FEN = ""
        self.colored_squares = []
        
        # Reset Players
        for player in self.players:
            player.set_color("Black")
            player.reset_pieces()
            
            
        self.pieces_on_board = self.manager.players[0].pieces + self.manager.players[1].pieces
        self.turns = [p.turn for p in self.pieces_on_board]
        
        # Pick Random Player to Go First
        random_index = random.randrange(0, 1)
        self.player_to_move = self.players[random_index]
        self.players[random_index].set_color("White")
        
        self.selected_block = None
        self.selected_piece = None
        
        self.is_player_holding_piece = False
        
        self.promoting_pawn = None
        
        self.captured_pieces = []
        
        
    def input(self, event):
        mouse_pos = pygame.mouse.get_pos()
        
        # Drag/Drop and Selection
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.selected_block = self.select_block(mouse_pos)
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # release left click to drop the piece
                if self.current_turn == 0 or not type(self.manager.players[1]) == Computer:
                    self.drop_piece(mouse_pos)

        elif pygame.mouse.get_pressed()[0]:  # if dragging, move the piece
            self.drag(mouse_pos[0], mouse_pos[1])
        
        # Pawn Promotion
        elif event.type == pygame.KEYDOWN:
            if self.promoting_pawn:
                pos = self.promoting_pawn.real_time_position
                turn = self.promoting_pawn.is_players_turn
                
                # Keyboard Selection
                if not self.auto_queen: #TODO or holding down ctrl key
                    if event.key == pygame.K_1:
                        self.promote_pawn(Queen(pos, turn))
                    elif event.key == pygame.K_2:
                        self.promote_pawn(Bishop(pos, turn))
                    elif event.key == pygame.K_3:
                        self.promote_pawn(Knight(pos, turn))
                    elif event.key == pygame.K_4:
                        self.promote_pawn(Rook(pos, turn))
                else:
                    self.promote_pawn(Queen(pos, turn))

        # Player Turn
        if event.type == pygame.USEREVENT:
            self.player_to_move.move()
                    
            if self.is_board_to_rotate:
                if self.delay > 0:
                    self.delay -= 1
                else:
                    self.next_turn()
                    self.is_board_to_rotate = False
                    self.delay = 1
                    pygame.time.set_timer(pygame.USEREVENT, 1000)


    ####
    # Draw the Board
    ###
    def draw(self, screen):
        '''Draws the board.'''
        # Render Board with Dynamic Sizing
        screen_center = (screen.get_width()/2, screen.get_height()/2)
        board_width = screen.get_height()
        board_height = board_width
        playing_field_width = board_width/1.2
        playing_field_height = board_height/1.2
        board = pygame.Rect(0, 0, board_width, board_height)
        playing_field = pygame.Rect(0, 0, playing_field_width, playing_field_height)
        playing_field.center = board.center = screen_center
        self.panel = playing_field

        pygame.draw.rect(screen, BROWN, board) #TODO Make colors based on theme
        pygame.draw.rect(screen, OAK, playing_field)

        # Draw Squares on the Board #TODO Clean up, lighter weight, combine with piece drawing?
        sq_width, sq_height = playing_field.width/8, playing_field.height/8
        square = pygame.Rect(self.panel.left, self.panel.top, sq_width, sq_height)
        for x, y in self.blocks:
            sq_left = x * sq_width + playing_field.x
            sq_top = y * sq_height + playing_field.y
            sq = pygame.Rect(sq_left, sq_top, sq_width, sq_height)
            
            if (x + y) % 2 == 0: #TODO coordinate with color options for theme
                pygame.draw.rect(screen, OAK, sq)
            else:
                pygame.draw.rect(screen, BROWN, sq)
            if (x, y) in self.colored_squares:
                pygame.draw.rect(screen, self.colored_squares[(x, y)], sq)
            elif (x, y) == self.selected_block:
                self.draw_rect(screen, LIGHT_GREEN, sq, 300)
            if (x, y) in self.movable_blocks:
                self.draw_rect(screen, LIGHT_GREEN, sq, 300)
            if (x, y) in self.capturables:
                pygame.draw.rect(screen, RED, sq, 3)
            if (x, y) == self.en_passant_block:
                pygame.draw.rect(screen, RED, sq)
              
        # Draw the board square labels  
        letters = ["A", "B", "C", "D", "E", "F", "G", "H"]
        if self.current_turn != 0 and self.rotation:
            letters.reverse()
        label_font = pygame.font.SysFont('arial', 36, bold = True)
        number_font = pygame.font.SysFont('arial', 40, bold = True)

        for i in range (0, 8):
            label_text = label_font.render(letters[i], True, DARK_OAK) #TODO Make consistent with theme colors
            label_rect = label_text.get_rect()
            label_rect.centerx = square.centerx
            label_rect.centery = self.board_panel.top - square.height / 2
            screen.blit(label_text, label_rect)
            square.left += square.width
            
            number_text = number_font.render(str(8 - i) if self.current_turn == 0 and self.rotation else str(i + 1), True, DARK_OAK)
            number_rect = number_text.get_rect()
            number_rect.centerx = playing_field.left - playing_field.width * 0.05
            number_rect.centery = square.centery
            screen.blit(number_text, number_rect)
            square.top += square.height
        
        square.topleft = playing_field.topleft
        
        # Add board texture
        texture = pygame.image.load(TEXTURE_PATH + "wood_grain.png")
        texture = pygame.transform.scale(texture, (board.width, board.height))
        texture_rect = texture.get_rect()
        texture.set_alpha(80)
        texture_rect.topleft = board.topleft
        screen.blit(texture, texture_rect)
        
        # Add board borders
        border = pygame.Rect(0, 0, playing_field.width, playing_field.height)
        border.top = playing_field.top-2
        border.left = playing_field.left - 2
        pygame.draw.rect(screen, GOLD, border, 4)
        shadow = pygame.Rect(0, 0, playing_field.width, playing_field.height)
        shadow.top = border.top + 2
        shadow.left = border.left + 2
        pygame.draw.rect(screen, GOLD_SHADOW, shadow, 2)
        highlight = pygame.Rect(0, 0, playing_field.width, playing_field.height)
        highlight.top = playing_field.top - 3
        highlight.left = playing_field.left - 3
        pygame.draw.rect(screen, WHITE, highlight, 1)
        
        # Draw each piece
        sprite_width = self.panel.width / 8 - 10
        sprite_height = self.panel.height / 8 - 10
        for piece in self.pieces_on_board:
            piece.update(self.pieces_on_board, self.rotation)
            if piece == self.selected_piece: #TODO why?
                continue

            # Make knight face proper direction
            if isinstance(piece, Knight):
                if self.rotation: #TODO rewrite this
                    if self.current_turn == 0:
                        piece.draw(screen, (sprite_width, sprite_height), self.panel, 180 if piece.is_players_turn == 0 else 0)
                    else:
                        piece.draw(screen, (sprite_width, sprite_height), self.panel, 0 if piece.is_players_turn == 0 else 180)
                else:
                    piece.draw(screen, (sprite_width, sprite_height), self.panel, 180 if piece.is_players_turn == 0 else 0)
                continue
            
            piece.draw(screen, (sprite_width, sprite_height), self.panel)
        
        # Add effect to selected piece
        if self.selected_piece != None:
            self.selected_piece.draw(screen, (sprite_width, sprite_height), self.panel)
        
        # Transition Between Turns #TODO move to Scene somehow
        if self.is_board_to_rotate and self.rotation and not self.pause:
            r = pygame.Rect(0, 0, 400, 200)
            r.center = screen.get_rect().center
            pygame.draw.rect(screen, OAK, r, 0, 10)
            text = GET_FONT('elephant', 40).render("White's turn!" if self.current_turn == 1 else "Black's turn!", True, WHITE)
            screen.blit(text, text.get_rect(center=(screen.get_rect().centerx, screen.get_rect().centery)))
        
        if not self.rotation and self.current_turn != 0 and self.get_game_state('1','2','3') != '3' and self.ai_delay <= 0:
            if self.selected_piece == None:
                selected_piece = random.sample(self.ai_pieces, 1)[0]
                self.select_block(None, (selected_piece.current_pos[0], selected_piece.current_pos[1]))
            drop_pos = random.sample(self.selected_piece.get_movement(self.pieces_on_board) + self.selected_piece.get_capturables(self.pieces_on_board), 1)[0]
            self.select_block(None, (drop_pos[0], drop_pos[1]))

        
    
    def square_highlighter(self, xy: (int, int), color, reset_feedbacks):
        '''Highlights squares.'''
        if reset_feedbacks:
            self.colored_squares = {xy: color}
        else:
            self.colored_squares[xy] = color

    def draw_rect(self, screen, color, rect: pygame.Rect, opacity = 255):
        s = pygame.Surface(rect.size)
        s.set_alpha(opacity)        
        s.fill(color)
        screen.blit(s, (rect.x, rect.y))


    def select_block(self, pos: tuple, grid_pos: tuple = None):
        if self.pause or (pos == None and grid_pos == None):
            return
        if pos != None: x, y = pos
        piece_positions = [i.current_pos for i in self.pieces_on_board]
        if self.drop_piece(pos, grid_pos) or self.board_panel == None:
            return
        if grid_pos == None:
            x, y = self._get_grid_position(x, y)
        else:
            x, y = grid_pos
        if (x, y) not in self.movable_blocks or (x, y) not in self.capturables:
            self._reset_selected()
        if (x >= 0 and x <= 7) and (y >= 0) and (y <= 7):
            self.selected_block = (x, y)
            if self.selected_block in piece_positions:
                if (self.pieces_on_board[piece_positions.index(self.selected_block)].turn == self.current_turn):
                    self.selected_piece = self.pieces_on_board[piece_positions.index(self.selected_block)]
                    self.handle_check()
                    if isinstance(self.selected_piece, Pawn):
                        self.check_enpassant(self.selected_piece)
                        print('Got Here A')
                        print(self.en_passant_block)
                    if isinstance(self.selected_piece, King):
                        if self.selected_piece.check_castling(self.pieces_on_board):
                            for block in self.selected_piece.castling_blocks:
                                self.castling_blocks += [tuple(block)]
                                self.square_highlighter(block, PURPLE, False)

                    self.movable_blocks = self.selected_piece.get_movement(self.pieces_on_board)
                    self.capturables = self.selected_piece.get_capturables(self.pieces_on_board)
                else:
                    self.square_highlighter(self.selected_block, RED, True)
                    self._reset_selected(True)
        return (x, y)
 
    ###
    # Drag and Drop
    ###
    def drag(self, x, y): #TODO view
        '''Changes the position of the held piece to the mouse position until dropped.'''

        if self.board_panel == None or self.pause:
            return
        
        block_size = self.board_panel.width / 8
        x = (x - self.board_panel.x) / block_size - 0.5
        y = (y - self.board_panel.y) / block_size - 0.5
        
        for i in self.pieces_on_board:
            if (self.selected_block == i.current_pos and not self.is_player_holding_piece and not i.captured):
                self.is_player_holding_piece = True
                self.selected_piece = i
                return
        
        if self.selected_piece is not None:
            self.selected_piece.pos = (x, y)


    
    def drop(self, x, y, grid_pos: tuple = None): #TODO view
        """Calculates the grid point of the mouse position, after this method called
        it will set the piece position to the grid point. which will give the snap effect."""

        if self.board_panel == None:
            return False
        # converts x, y to grid position
        if grid_pos == None:
            block_x, block_y = self._get_grid_position(x, y)
        else:
            block_x, block_y = grid_pos
        
        if self.selected_piece == None:
            return False
        
        if (block_x, block_y) in self.castling_blocks:
            self.selected_piece.do_castling((block_x, block_y))
            self.pawn_at_end(self.selected_piece)
            # self.next_turn()
            if self.rotation: 
                self.is_board_to_rotate = True
                pygame.time.set_timer(pygame.USEREVENT, self.delay_speed)
            else: self.next_turn()
            self._reset_selected()
            return True
        
        if isinstance(self.selected_piece, Pawn) and (block_x, block_y) == self.en_passant_block:
            self.captured_pieces.append(self.selected_piece.en_passant)
            self.selected_piece.do_enpassant()
            if self.rotation: 
                self.is_board_to_rotate = True
                pygame.time.set_timer(pygame.USEREVENT, self.delay_speed)
            else: self.next_turn()
            self._reset_selected()
            return True
        
        piece_positions = [p.current_pos for p in self.pieces_on_board]
        prev_pos = self.selected_piece.real_time_position
        
        self.selected_piece.move_piece(block_x, block_y, self.current_turn, self.pieces_on_board)
        
        if self.selected_piece.real_time_position == prev_pos:
            return False

        if (block_x, block_y) in self.capturables:
            self.captured_pieces.append(self.pieces_on_board[piece_positions.index((block_x, block_y))])
            self.pieces_on_board[piece_positions.index((block_x, block_y))].destroy_piece()
            self.pawn_at_end(self.selected_piece)
            # self.next_turn()
            if self.rotation: 
                self.is_board_to_rotate = True
                pygame.time.set_timer(pygame.USEREVENT, self.delay_speed)
            else: self.next_turn()
            self._reset_selected()
            return True
        
        if (block_x, block_y) != self.selected_block:
            self.pawn_at_end(self.selected_piece)
            # self.next_turn()
            if self.rotation: 
                self.is_board_to_rotate = True
                pygame.time.set_timer(pygame.USEREVENT, self.delay_speed)
            else: self.next_turn()
            self._reset_selected()
            return True
        
        self._reset_selected()
        return False       

    def select_block(self, pos: tuple, grid_pos: tuple = None): #TODO view
        x, y = pos
        piece_positions = [i.current_pos for i in self.pieces_on_board]
        if self.pause:
            return
        if self.drop(x, y, grid_pos) or self.board_panel == None:
            return
        if grid_pos == None:
            x, y = self._get_grid_position(x, y)
        else:
            x, y = grid_pos
        if (x, y) not in self.movable_blocks or (x, y) not in self.capturables:
            self._reset_selected()
        if (x >= 0 and x <= 7) and (y >= 0) and (y <= 7):
            self.selected_block = (x, y)
            if self.selected_block in piece_positions:
                if (self.pieces_on_board[piece_positions.index(self.selected_block)].turn == self.current_turn):
                    self.selected_piece = self.pieces_on_board[piece_positions.index(self.selected_block)]
                    self.check()
                    if isinstance(self.selected_piece, King):
                        if self.selected_piece.check_castling(self.pieces_on_board):
                            for block in self.selected_piece.castling_blocks:
                                self.castling_blocks += [tuple(block)]
                                self.square_highlighter(block, PURPLE, False)

                    self.movable_blocks = self.selected_piece.get_movement(self.pieces_on_board)
                    self.capturables = self.selected_piece.get_capturables(self.pieces_on_board)
                else:
                    self.square_highlighter(self.selected_block, RED, True)
                    self._reset_selected(True)
        return (x, y)

    
    ###
    # Game States
    ###
    def get_game_state(self): #TODO view
        '''Returns the status of the game.'''
        return self.game_state
        if self.check_state == None:
            return 'Playing'
        elif any([len(piece.get_movement(self.pieces_on_board)) > 1 or len(piece.get_capturables(self.pieces_on_board)) > 0 for piece in self.pieces_on_board if piece.turn == self.current_turn]):
            return 'Check'
        elif False: #TODO stalemate
            pass
        else:
            return 'Check-Mate'
    
    def check(self): #TODO view
        '''Executes when the king is in check.'''
        for piece in self.pieces_on_board:
            if piece is King:
                if piece.turn == self.current_turn:
                    piece.set_disabled_moves(self.pieces_on_board)
                if piece.is_check(self.pieces_on_board, piece.current_pos):
                    self.check_state = piece.turn
    
    
    
    ### Pawn Promotion ###
    def pawn_at_end(self, piece): #TODO move to Pawn class?
        target_pos_y = 0
        if not self.rotation:
            target_pos_y = 0 if self.current_turn == 0 else 7
        if isinstance(piece, Pawn) and piece.real_time_position != None and piece.is_players_turn == self.current_turn and piece.real_time_position[1] == target_pos_y:
            self.promoting_pawn = piece
            return True
        return False
    
    
    def promote_pawn(self, piece):
        if self.promoting_pawn == None or self.promoting_pawn not in self.pieces_on_board: # Unnecessary Safeguard
            return
        piece.current_pos = self.promoting_pawn.real_time_position
        self.pieces_on_board.remove(self.promoting_pawn)
        self.pieces_on_board.append(piece)
        
        self.promoting_pawn = None
        
        self.next_turn()

    def next_turn(self): #TODO view
        if self.pause or self.promoting_pawn != None:
            return
        if self.current_turn < max(self.turns):
            self.current_turn += 1
        else:
            self.current_turn = min(self.turns)
        if self.rotation: self.flip_places()

        else:
            self.handle_ai()

        self.handle_check()

    ### Flip Board ###
    def flip_places(self): #TODO view
        for piece in self.pieces_on_board:
            piece.reflect_place()
            
    def _get_grid_position(self, x: float, y: float): #TODO view
        block_size = self.board_panel.width / 8
        if x > self.board_panel.x and y > self.board_panel.y:
            x = int((x - self.board_panel.x) / block_size)
            y = int((y - self.board_panel.y) / block_size)
        return x, y
    
    def _grid_to_screen_pos(self, x: float, y: float): #TODO view
        block_size = self.board_panel.width / 8
        x = x + self.board_panel.x * block_size
        y = y + self.board_panel.y * block_size
        return x, y
    
    def _reset_selected(self, keep_feedback=False): #TODO view
        self.selected_piece = None
        self.is_player_holding_piece = False
        self.selected_block = None
        
        self.movable_blocks = []
        self.capturables = []
        self.castling_blocks = []
        self.en_passant_block = []

        if not keep_feedback:
            self.colored_squares = {}
    
    def set_theme(self, theme):
        if theme in THEMES:
            self.theme = theme
            for piece in self.pieces_on_board:
                piece.set_theme(self.theme)
                
    def set_view(self, view):
        '''Changes the board's view.'''
        if view in VIEWS:
            self.view = view
            for piece in self.pieces_on_board:
                piece.set_view(self.view)
    
    def handle_check(self):
        self.check_state = None
        for piece in self.pieces_on_board:
            if isinstance(piece, King):
                if piece.is_players_turn == self.current_turn:
                    piece.set_disabled_moves(self.pieces_on_board)
                if piece.is_check(self.pieces_on_board, piece.current_pos):
                    self.check_state = piece.is_players_turn
                
    def get_game_state(self):
        '''Returns text reflecting the state of the game.'''
        if self.check_state == None:
            return 'Playing'
        if any([len(piece.get_movement(self.pieces_on_board)) > 1 or len(piece.get_capturables(self.pieces_on_board)) > 0 for piece in self.pieces_on_board if piece.turn == self.current_turn]):
            return 'Check'
        else:
            return 'Check-Mate'
