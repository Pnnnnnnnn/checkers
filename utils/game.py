import pygame
from .constants import *
from .board import Board

class Game:
    def __init__(self, window):
        self.window = window
        self.board = Board()
        self.turn = BLACK
        self.selected_piece = None
        self.valid_moves = {}

    def update(self):
        self.board.draw_background(self.window)
        self.board.draw_pieces(self.window)
        self.draw_valid_moves(self.valid_moves.keys())
        pygame.display.update()

    def click(self, row, col):
        if self.selected_piece:
            success = self._move(row, col)
            if not success:
                self.selected_piece = None
                self.click(row, col)
        piece = self.board.get_piece(row, col)
        if piece and piece.color == self.turn:
            self.selected_piece = piece
            self.valid_moves = self.board.get_valid_moves(piece)
            return True
        return False
    
    def _move(self, row, col):
        piece = self.board.get_piece(row, col)
        if self.selected_piece and piece == None and (row, col) in self.valid_moves:
            self.board.move(self.selected_piece, row, col)
            skipped = self.valid_moves[(row, col)]
            if skipped:
                self.board.remove(skipped)
            self._change_turn()
        else:
            return False
        return True
    
    def draw_valid_moves(self, moves):
        for move in moves:
            row, col = move
            pygame.draw.circle(self.window, GOLD, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), 15)

    def _change_turn(self):
        self.valid_moves = {}
        if self.turn == WHITE:
            self.turn = BLACK
        else:
            self.turn = WHITE

    def get_winner(self):
        return self.board.get_winner()
    
    def ai_move(self, board):
        self.board = board
        self._change_turn()

    def get_board(self):
        return self.board