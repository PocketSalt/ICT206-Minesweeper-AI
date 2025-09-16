import pygame

from game import GRID_SIZE, GameState
from enum import Enum
from tile import Tile

WIDTH = HEIGHT = 1280
FPS = 30
game = GameState()

CELL_SIZE = 158
MARGIN = 2

class State(Enum):
    PLAYING = 0
    WIN = 1
    LOSE = 2

global currentState

def draw_board(screen, grid):
    font = pygame.font.SysFont(None, 30)
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            x = c * (CELL_SIZE + MARGIN)
            y = r * (CELL_SIZE + MARGIN)

            rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, (200, 200, 200), rect)  # light gray background

            val = grid[r][c].value
            vis = grid[r][c].visible
            flag = grid[r][c].flagged

            if flag:
                text = font.render("F", True, (255, 0, 0))  # flagggg
            elif vis and val >= 0:
                text = font.render(str(val), True, (0, 0, 0))  # just the number
            else:
                text = font.render(" ", True, (0, 0, 0))  # empty

            text_rect = text.get_rect(center=rect.center)
            screen.blit(text, text_rect)

def main():
    global currentState, running
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Minesweeper")
    clock = pygame.time.Clock()
    running = True

    currentState = State.PLAYING

    while running:
        screen.fill((255, 255, 255))

        if currentState == State.PLAYING:
            get_keys()

        if currentState == State.LOSE:
            print("GAME OVER | press R to restart")
            get_restart()
            Tile.correct_flag_count = 0

        if game.bomb_count == Tile.correct_flag_count:
            print("YOU WIN | press R to restart")
            get_restart()
            Tile.correct_flag_count = 0

        draw_board(screen, game.grid)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

def get_restart():
    global currentState
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                game.restart()
                currentState = State.PLAYING


def get_keys():
    global currentState, running
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                print("A")
                game.reveal(5, 5)

        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            rel_x = x // (CELL_SIZE + MARGIN)
            rel_y = y // (CELL_SIZE + MARGIN)

            if event.button == 1:  # left click
                if not game.grid[rel_y][rel_x].flagged:
                    game.reveal(rel_y, rel_x)

                    if game.grid[rel_y][rel_x].value == -1:
                        currentState = State.LOSE

            if event.button == 3:  # flag
                if not game.grid[rel_y][rel_x].visible:
                    game.grid[rel_y][rel_x].toggle_flag()

if __name__ == "__main__":
    main()
