import pygame

class Location:
    def __init__(self, xCoord: int, yCoord: int):
        self.xCoord = xCoord # 0 - 7
        self.yCoord = yCoord # 0 - 7

class Piece:
    move_count = 0 # Keeps track of the moves of the game.

    def __init__(self, start_pos: (int, int), piece_name: str, player_number: int):
        self.pos = start_pos # realtime position when moving piece
        self.board_pos = start_pos # position as in grid coordinates #current_pos
        self.player_number = player_number # number of the piece, either 0 or 1 for chess (black or white)

        self.sprite = self.set_sprite(player_number) # for the image
        self.piece_name = piece_name # name of the piece (prob unnecessary)

        self.piece_moves = None
        self.piece_attacks = None
        self.jumps = False

    def set_sprite(self, player_number: int):
        return None
