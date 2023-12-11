import pygame
from utils.constants import WIDTH, HEIGHT, SQUARE_SIZE, BLACK, WHITE
from utils.board import Board
from utils.game import Game
from utils.minimax import minimax

FPS = 60
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Checkers')

def get_pos_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col

def main():
    run = True
    game = Game(WINDOW)
    clock = pygame.time.Clock()

    while run:
        clock.tick(FPS)

        if game.turn == WHITE:
            value, new_board = minimax(game.get_board(), 3, BLACK, game)
            game.ai_move(new_board)

        if game.get_winner():
            print(game.get_winner())
            run = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN and game.turn == BLACK:
                row, col = get_pos_from_mouse(pygame.mouse.get_pos())
                game.click(row, col)
        game.update()
    pygame.quit()

if __name__ == '__main__':
    main()