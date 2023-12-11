import pygame
from .piece import Piece
from .constants import *

class Board:
    def __init__(self):
        self.board = []
        self.white_left = self.black_left = 8
        self.white_kings = self.black_kings = 0
        self.create_board()

    def draw_background(self, window):
        window.fill(CREAM)
        for row in range(ROWS):
            for col in range(row % 2, ROWS, 2):
                pygame.draw.rect(window, BROWN, (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def move(self, piece, row, col):
        # swap
        self.board[piece.row_pos][piece.col_pos], self.board[row][col] = self.board[row][col], self.board[piece.row_pos][piece.col_pos]
        piece.move(row, col)
        if (row == ROWS - 1 or row == 0) and not piece.is_king:
            piece.promote()
            if piece.color == WHITE:
                self.white_kings += 1
            else:
                self.black_kings += 1

    def get_piece(self, row, col):
        return self.board[row][col]

    def draw_pieces(self, window):
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece:
                    piece.draw(window)

    def create_board(self):
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if col % 2 == ((row + 1) % 2):
                    if row < 2:
                        self.board[row].append(Piece(WHITE, False, row, col))
                    elif row > ROWS - 3:
                        self.board[row].append(Piece(BLACK, False, row, col))
                    else:
                        self.board[row].append(None)
                else:
                    self.board[row].append(None)

    def evaluate(self):
        # heuristic function
        return self.white_left - self.black_left + (self.white_kings * 0.5 - self.black_kings * 0.5)
    
    def get_all_pieces(self, color):
        pieces = []
        for row in self.board:
            for piece in row:
                if piece != None and piece.color == color:
                    pieces.append(piece)
        return pieces
    
    def get_board(self):
        return self.board
    
    def ai_move(self, board):
        self.board = board

    
    def get_valid_moves(self, piece):
        moves = {}
        left = piece.col_pos - 1
        right = piece.col_pos + 1
        row = piece.row_pos
        if piece.color == BLACK or piece.is_king:
            moves.update(self._traverse_left(row - 1, max(row - 3, -1), -1, piece.color, left))
            moves.update(self._traverse_right(row - 1, max(row - 3, -1), -1, piece.color, right))
        if piece.color == WHITE or piece.is_king:
            moves.update(self._traverse_left(row + 1, min(row + 3, ROWS), 1, piece.color, left))
            moves.update(self._traverse_right(row + 1, min(row + 3, ROWS), 1, piece.color, right))
        return moves
    
    def _traverse_left(self, start, stop, step, color, left, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if left < 0:
                break
            current = self.board[r][left]
            if current is None:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, left)] = last + skipped
                else:
                    moves[(r, left)] = last
                if last:
                    if step == -1:
                        row = max(r - 3, 0)
                    else:
                        row = min(r + 3, ROWS)
                    moves.update(self._traverse_left(r + step, row, step, color, left - 1, skipped=last))
                    moves.update(self._traverse_right(r + step, row, step, color, left + 1, skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]
            left -= 1
        return moves
    
    def _traverse_right(self, start, stop, step, color, right, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if right >= COLS:
                break
            current = self.board[r][right]
            if current is None:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, right)] = last + skipped
                else:
                    moves[(r, right)] = last
                if last:
                    if step == -1:
                        row = max(r - 3, 0)
                    else:
                        row = min(r + 3, ROWS)
                    moves.update(self._traverse_left(r + step, row, step, color, right - 1, skipped=last))
                    moves.update(self._traverse_right(r + step, row, step, color, right + 1, skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]
            right += 1
        return moves
    
    def remove(self, pieces):
        for piece in pieces:
            self.board[piece.row_pos][piece.col_pos] = None
            if piece != None:
                if piece.color == BLACK:
                    self.black_left -= 1
                else:
                    self.white_left -= 1

    def get_winner(self):
        if self.black_left <= 0:
            return "The winner is white"
        elif self.white_left <= 0:
            return "The winner is black"
        return None
    