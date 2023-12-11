from utils.constants import *

class Piece:
    PADDING = 14
    OUTLINE = 6

    def __init__(self, color, is_king, row_pos, col_pos):
        self.color = color
        self.outline_color = OFF_WHITE if color == WHITE else DARK_GREY
        self.is_king = is_king
        self.row_pos, self.col_pos = row_pos, col_pos
        self.direction = self.color == WHITE and -1 or 1
        self.x, self.y = 0, 0
        self.update_position()
    
    def update_position(self):
        self.x = self.col_pos * SQUARE_SIZE + SQUARE_SIZE // 2
        self.y = self.row_pos * SQUARE_SIZE + SQUARE_SIZE // 2

    def promote(self):
        self.is_king = True
        self.direction = 0
        self.outline_color = GOLD
    
    def draw(self, window):
        radius = SQUARE_SIZE // 2 - self.PADDING
        pygame.draw.circle(window, self.outline_color, (self.x, self.y), radius + self.OUTLINE)
        pygame.draw.circle(window, self.color, (self.x, self.y), radius)
        pygame.draw.circle(window, self.outline_color, (self.x, self.y), radius - self.OUTLINE, 3)

    def move(self, row, col):
        self.row_pos, self.col_pos = row, col
        self.update_position()
    def __repr__(self):
        return f"Piece({self.color}, {self.is_king}, {self.row_pos}, {self.col_pos})"
