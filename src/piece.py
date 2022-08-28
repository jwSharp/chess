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

from config import *



#####################
# Abstract Class #
#####################
class Piece:
    def __init__(self, position: (int, int), player, view):
        self.player = player
        
        self.piece_name = ''
        self.sprite = None
        self.image_path = None
        self.position, self.real_time_position = position, position
        
        self.piece_moves = []
        self.illegal_moves = []
        
        self.protectors = []

        self.is_captured = False
        
        self.move_count = 0 # move to pawn and king and rook only
    
    def input(self, event: pygame.event):
        if event.type == pygame.VIDEORESIZE:
            self.sprite = pygame.image.load(self.image_path)

    def draw(self, screen, blit_size: (int, int), panel, rotate = 0): #TODO view
        if self.image_path == None or self.position == None:
            return
        self.sprite = pygame.image.load(self.image_path)
        x, y = self.position
        x_pos = x * panel.width / 8 + (panel.x + 5)
        y_pos = y * panel.height / 8 + (panel.y + 5)
        self.sprite = pygame.transform.rotate(self.sprite, rotate)
        self.sprite = pygame.transform.smoothscale(self.sprite, blit_size)
        screen.blit(self.sprite, (x_pos, y_pos))
    
    def set_player(self):
        self.is_players_turn = not self.is_players_turn
    
    ###
    # Piece Movement
    ###
    def move(self, x, y, other_pieces=[]) -> (int, int): #TODO view
        if self.is_valid_move(x, y, other_pieces) and self.is_players_turn:
            self.real_time_position = (x, y)
            self.position = (x, y)
            
        else: # snap back to original position
            self.position = self.real_time_position
        return self.real_time_position

    def is_valid_move(self, target_x, target_y, other_pieces=[]) -> bool: #TODO rewrite partially
        '''Determines whether the piece may move to a selected square given the board state.'''
        if target_x < 0 or target_x > 7 or target_y < 0 or target_y > 7 or (target_x, target_y) == self.real_time_position:
            return False
        return (target_x, target_y) in self.get_movement(other_pieces)
    
    def get_movement(self, other_pieces): #TODO view
        blocks = []
        self.capturables = []
        piece_positions = []
        
        if other_pieces != []:
            piece_positions = [p.current_pos for p in other_pieces]
        
        if self.piece_moves == None:
            return blocks
        
        for move in list(self.piece_moves):
            if self.real_time_position == None:
                continue
            pos = self.add_to_pos(move)
            
            for p in pos:
                if p not in piece_positions:
                    blocks.append(p)
                else:
                    if other_pieces[piece_positions.index(p)].turn != self.is_players_turn:
                        self.capturables.append(p)
                    break
            else:
                blocks += pos
        
        if self.illegal_moves == []:
            return blocks
        self.capturables = [c for c in self.capturables if c not in self.illegal_moves]
        return [b for b in blocks if b not in self.illegal_moves]

    def is_protected(self, pieces) -> bool: #TODO view
        self._change_turn(pieces)
        self.protectors = [p for p in pieces if p.turn == self.is_players_turn and self.real_time_position in p.get_capturables(pieces)]
        self._change_turn(pieces)
        return len(self.protectors) > 0

    def destroy(self): #TODO implement graveyard
        '''Moves a piece from the board to the graveyard.'''
        self.real_time_position = None
        self.position = None
        self.is_captured = True
        
        # Move to graveyard #TODO

    def add_to_pos(self, move: str): #TODO rewrite entirely
        return [
            (self.real_time_position[0] + j[0], self.real_time_position[1] - j[1])
            for j in self.decode_move(move) 
            if self.real_time_position[0] + j[0] in range(0, 8) and self.real_time_position[1] - j[1] in range(0, 8)
        ]
        
    def decode_move(self, area: list) -> [(int, int)]: #TODO view
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
            if pos_x == [] or pos_y == []:
                continue
            x = pos_x[-1] if pos_x.index(pos_x[-1]) < i else pos_x[i]
            y = pos_y[-1] if pos_y.index(pos_y[-1]) < i else pos_y[i]
            blocks.append((x, y))
        return blocks
    
    
    ###
    # Two Player Board Flip
    ###
    def translate(self, x, y) -> (int, int): #TODO view
        '''Translates piece from one location to another.'''
        self.real_time_position = (x, y)
        self.position = (x, y)
        return self.real_time_position
    
    def reflect_place(self): #TODO view
        '''Mirrors the pieces position.'''
        if self.real_time_position == None:
            return
        x = 7 - self.real_time_position[0]
        y = 7 - self.real_time_position[1]
        self.translate(x, y)
        self.piece_moves = self.get_reflected_move(self.piece_moves)
        return (x, y)

    def get_reflected_move(self, old_move:[(str)]) -> [(str)]:
        '''Returns movement of a piece when the board has been flipped.'''
        new_move = []
        for move in old_move:
            new_points = []
            for point in move:
                temp = point
                try:
                    temp = str(int(temp) * -1)
                except: #? Not sure what the except clause is for
                    temp = str(int(temp.split('|')[0]) * -1) + '|' + str(int(temp.split('|')[1]) * -1)
                new_points.append(temp)
            new_move.append(new_points)
        return new_move


    def set_theme(self):
        self.set_sprite()
        #TODO update sprite accordingly
    
    def set_view(self):
        self.set_sprite
        #TODO update sprite accordingly

    def set_sprite(self): #TODO view
        if self.player.color == 'white':
            self.image_path = f'{WHITE_PIECES_PATH}{self.piece_name}/{self.manager.theme}/{self.manager.view}{self.piece_name}'
        else: # black
            self.image_path = f'{BLACK_PIECES_PATH}{self.piece_name}/{self.manager.theme}/{self.manager.view}{self.piece_name}'
    
    def _change_turn(self, pieces): #TODO view
        piece_turns = [piece.turn for piece in pieces]
        if self.is_players_turn < max(piece_turns):
            self.is_players_turn += 1
        else:
            self.is_players_turn = min(piece_turns)
            

    ######
            
    def _get_n2n(self, n2n: str, seperator: str) -> list: #TODO Remove this function
        '''
            Returns list of numbers from n2n by seperating
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


#####################
# Piece Children #
#####################
class Pawn(Piece):
    def __init__(self, pos, turn):
        super().__init__(pos, turn, "pawn")
        self.piece_moves = [('0', '1|2')] if turn == 0 else [('0', '-1|-2')]
        self.piece_attacks = [('-1', '1'), ('1', '1')] if turn == 0 else [('-1', '-1'), ('1', '-1')]
        self._set_sprite(turn, "pawn_top.png", "pawn_top.png")
        
        self.en_passant = None
        
        self.has_moved = False
        self.is_first_move = False
    
    def update(self, board_turns=False): #TODO rename and rewrite
        self.board_turns = board_turns
        if self.has_moved:
            if board_turns:
                self.piece_moves = [('0', '1')]
            else:
                self.piece_moves = [('0', '1')] if self.is_players_turn == 0 else [('0', '-1')]
    
    def move(self, x, y, other_pieces=[]) -> (int, int): #TODO view
        if self.is_valid_move(x, y, other_pieces) and self.is_players_turn:
            self.real_time_position = (x, y)
            self.pos = (x, y)
            
            if self.has_moved:
                self.is_first_move = False
            else:
                self.has_moved = True
                
        else: # snap back to original position
            self.pos = self.real_time_position
        return self.real_time_position
    
    def check_enpassant(self, pieces): #TODO Messy, redo, make one function
        opponent_pawns = [pawn for pawn in pieces if isinstance(pawn, Pawn) and not pawn.is_captured and self.is_players_turn and pawn.is_first_move and pawn.real_time_position[1] in [3, 4]]
        opponents_positions = [p.real_time_position for p in opponent_pawns]
        
        if (self.real_time_position[0] - 1, self.real_time_position[1]) in opponents_positions: # Checks the left side
            opponent_pawns_index = opponents_positions.index((self.real_time_position[0] - 1, self.real_time_position[1]))
            #TODO append to attacks
            self.en_passant = opponent_pawns[opponent_pawns_index]
        if (self.real_time_position[0] + 1, self.real_time_position[1]) in opponents_positions: # Checks the right side
            opponent_pawns_index = opponents_positions.index((self.real_time_position[0] + 1, self.real_time_position[1]))
            #TODO append to attacks
            self.en_passant = opponent_pawns[opponent_pawns_index]
        
        return self.en_passant != None

    def enpassant(self): #TODO Messy, redo, make one function
        if (not self.board_turns and self.is_players_turn == 0) or not self.board_turns:
            self.translate(self.en_passant.real_time_position[0], self.real_time_position[1] + 1)
        else:
            self.translate(self.en_passant.real_time_position[0], self.real_time_position[1] - 1)
        self.en_passant.destroy_piece()

    def translate(self, x, y, count_move = False) -> (int, int): #TODO view
        '''Translates piece from one location to another.'''
        self.real_time_position = (x, y)
        self.pos = (x, y)
        if count_move:
            if self.has_moved:
                self.is_first_move = False
            else:
                self.has_moved = True
        return self.real_time_position
    
    def get_capturables(self, other_pieces): #TODO view
        if self.piece_attacks == None:
            self.get_movement(other_pieces)
        else:
            piece_positions = [p.current_pos for p in other_pieces]

            self.capturables = []
            for attack in list(self.piece_attacks):
                if self.real_time_position == None:
                    continue
                pos = self.add_to_pos(attack)
                for p in pos:
                    if p in piece_positions and p not in self.illegal_moves:
                        piece = other_pieces[piece_positions.index(p)]
                        if piece.turn != self.is_players_turn:
                            self.capturables.append(p)
                        break
        return self.capturables

    def reflect_place(self): #TODO view
        '''Mirrors the pieces position.'''
        if self.real_time_position == None:
            return
        x = 7 - self.real_time_position[0]
        y = 7 - self.real_time_position[1]
        self.translate(x, y)
        self.piece_moves = self.get_reflected_move(self.piece_moves)
        if self.piece_attacks != None:
            self.piece_attacks = self.get_reflected_move(self.piece_attacks)
        return (x, y)

    
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
        self.threats = []
        self.capturables = []
        self.castling_blocks = []
        
        self.check_count = 0
        
        self.has_moved = False
    
    def update(self, pieces=[], board_turns=False):
        self.board_turns = board_turns
    
    def move(self, x, y, other_pieces=[]) -> (int, int): #TODO view
        if self.is_valid_move(x, y, other_pieces) and self.is_players_turn:
            self.current_pos = (x, y)
            self.pos = (x, y)
            
            self.threats = []
            
            self.has_moved = True
        
        else: # snap back to original position
            self.pos = self.current_pos
        return self.current_pos
    
    def set_disabled_moves(self, pieces):
        openents = [p for p in pieces if p.turn != self.is_players_turn]
        opponents_positions = [p.current_pos for p in openents]
        for piece in pieces:
            piece.disabled_moves = []
            hold_pos = piece.current_pos
            destroyed_piece = None
            if piece.turn != self.is_players_turn:
                continue
            for move in (piece.get_movement(pieces) + piece.get_capturables(pieces)):
                piece.translate(move[0], move[1], False)
                if piece.current_pos in opponents_positions:
                    destroyed_piece = openents[opponents_positions.index(move)]
                    pieces.remove(destroyed_piece)
                if self.is_check(pieces, self.current_pos):
                    piece.disabled_moves.append(move)
                if destroyed_piece != None:
                    pieces.append(destroyed_piece)
                    destroyed_piece = None
                piece.translate(hold_pos[0], hold_pos[1], False)
    
    def is_check(self, pieces: Piece, pos) -> bool:
        self.threats = [piece for piece in pieces if piece.turn != self.is_players_turn and pos in piece.get_capturables(pieces)]
        check = len(self.threats) > 0
        if check: self.check_count += 1
        return check
    
    def check_castling(self, pieces):
        self.castling_blocks = []
        self.rooks_can_castle = []
        self.piece_moves = [("1", "1"), ("1", "-1"), ("-1", "1"), ("-1", "-1"), ("1", "0"), ("0", "1"), ("-1", "0"), ("0", "-1")]
        if self.move_count > 0 or self.check_count > 0:
            return False
        rooks = [piece for piece in pieces if piece.turn == self.is_players_turn and piece.piece_name == 'rook']
        if all(rook.move_count > 0 for rook in rooks):
            return False
        change_x = (2, 6)
        point_y = 7 
        if not self.board_turns:
            if self.is_players_turn != 0: point_y = 0
        elif self.is_players_turn != 0:
            change_x = (1, 5)
        for rook in rooks:
            if rook.move_count == 0:
                if rook.current_pos == (0, point_y):
                    self.piece_moves += [('-1|-3', '0')]
                    if rook.is_valid_move(change_x[0] + 1, point_y, pieces) and self.is_valid_move(change_x[0], point_y, pieces):
                        self.castling_blocks += [(change_x[0], point_y)]
                        self.rooks_can_castle.append(rook)
                    self.piece_moves.remove(('-1|-3', '0'))
                elif rook.current_pos == (7, point_y):
                    self.piece_moves += [('1|3', '0')]
                    if rook.is_valid_move(change_x[1] - 1, point_y, pieces) and self.is_valid_move(change_x[1], point_y, pieces):
                        self.castling_blocks += [(change_x[1], point_y)]
                        self.rooks_can_castle.append(rook)
                    self.piece_moves.remove(('1|3', '0'))
        return len(self.castling_blocks) > 0

    def castle(self, block):
        if block not in self.castling_blocks:
            return
        self.translate(block[0], block[1])
        for rook in self.rooks_can_castle:
            print(rook.current_pos)
            if block[0] + 1 == rook.current_pos[0] or block[0] + 2 == rook.current_pos[0]:
                rook.translate(block[0] - 1, block[1], False)
                break
            elif block[0] - 2 == rook.current_pos[0] or block[0] - 1 == rook.current_pos[0]:
                rook.translate(block[0] + 1, block[1], False)
                break
        return

    def translate(self, x, y, count_move = False) -> (int, int): #TODO view
        '''Translates piece from one location to another.'''
        self.current_pos = (x, y)
        self.pos = (x, y)
        if count_move:
            self.has_moved = True
        return self.current_pos
                