import random
import sys
from dataclasses import dataclass

import pygame


CELL_SIZE = 30
GRID_WIDTH = 10
GRID_HEIGHT = 20
SIDE_PANEL = 180
SCREEN_WIDTH = GRID_WIDTH * CELL_SIZE + SIDE_PANEL
SCREEN_HEIGHT = GRID_HEIGHT * CELL_SIZE
FPS = 60
FALL_INTERVAL_MS = 500

BLACK = (18, 18, 24)
WHITE = (245, 245, 245)
GRAY = (60, 60, 70)

COLORS = [
    (0, 240, 240),   # I
    (0, 0, 240),     # J
    (240, 160, 0),   # L
    (240, 240, 0),   # O
    (0, 240, 0),     # S
    (160, 0, 240),   # T
    (240, 0, 0),     # Z
]

SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 0, 0], [1, 1, 1]],  # J
    [[0, 0, 1], [1, 1, 1]],  # L
    [[1, 1], [1, 1]],  # O
    [[0, 1, 1], [1, 1, 0]],  # S
    [[0, 1, 0], [1, 1, 1]],  # T
    [[1, 1, 0], [0, 1, 1]],  # Z
]


@dataclass
class Piece:
    shape: list[list[int]]
    color: tuple[int, int, int]
    x: int
    y: int

    def rotated(self) -> list[list[int]]:
        return [list(row) for row in zip(*self.shape[::-1])]


class Tetris:
    def __init__(self) -> None:
        self.grid: list[list[tuple[int, int, int] | None]] = [
            [None for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)
        ]
        self.score = 0
        self.game_over = False
        self.current_piece = self._new_piece()
        self.next_piece = self._new_piece()

    def _new_piece(self) -> Piece:
        idx = random.randrange(len(SHAPES))
        shape = [row[:] for row in SHAPES[idx]]
        x = (GRID_WIDTH - len(shape[0])) // 2
        return Piece(shape=shape, color=COLORS[idx], x=x, y=0)

    def _collision(self, piece: Piece, x_offset: int = 0, y_offset: int = 0) -> bool:
        for y, row in enumerate(piece.shape):
            for x, value in enumerate(row):
                if value == 0:
                    continue
                new_x = piece.x + x + x_offset
                new_y = piece.y + y + y_offset
                if new_x < 0 or new_x >= GRID_WIDTH or new_y >= GRID_HEIGHT:
                    return True
                if new_y >= 0 and self.grid[new_y][new_x] is not None:
                    return True
        return False

    def move(self, dx: int, dy: int) -> bool:
        if not self._collision(self.current_piece, x_offset=dx, y_offset=dy):
            self.current_piece.x += dx
            self.current_piece.y += dy
            return True
        if dy == 1:
            self._lock_piece()
        return False

    def rotate(self) -> None:
        rotated_shape = self.current_piece.rotated()
        original_shape = self.current_piece.shape
        self.current_piece.shape = rotated_shape
        if self._collision(self.current_piece):
            self.current_piece.shape = original_shape

    def drop(self) -> None:
        while self.move(0, 1):
            pass

    def _lock_piece(self) -> None:
        piece = self.current_piece
        for y, row in enumerate(piece.shape):
            for x, value in enumerate(row):
                if value == 0:
                    continue
                gy = piece.y + y
                gx = piece.x + x
                if gy < 0:
                    self.game_over = True
                    return
                self.grid[gy][gx] = piece.color
        self._clear_lines()
        self.current_piece = self.next_piece
        self.next_piece = self._new_piece()
        if self._collision(self.current_piece):
            self.game_over = True

    def _clear_lines(self) -> None:
        cleared = 0
        new_grid = []
        for row in self.grid:
            if all(cell is not None for cell in row):
                cleared += 1
            else:
                new_grid.append(row)
        for _ in range(cleared):
            new_grid.insert(0, [None for _ in range(GRID_WIDTH)])
        self.grid = new_grid
        self.score += [0, 100, 300, 500, 800][cleared]

    def draw(self, screen: pygame.Surface, font: pygame.font.Font) -> None:
        screen.fill(BLACK)
        self._draw_grid(screen)
        self._draw_piece(screen, self.current_piece)
        self._draw_side_panel(screen, font)
        pygame.display.flip()

    def _draw_grid(self, screen: pygame.Surface) -> None:
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                cell = self.grid[y][x]
                rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(screen, GRAY, rect, 1)
                if cell:
                    pygame.draw.rect(screen, cell, rect.inflate(-2, -2))

    def _draw_piece(self, screen: pygame.Surface, piece: Piece) -> None:
        for y, row in enumerate(piece.shape):
            for x, value in enumerate(row):
                if value == 0:
                    continue
                px = (piece.x + x) * CELL_SIZE
                py = (piece.y + y) * CELL_SIZE
                rect = pygame.Rect(px, py, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(screen, piece.color, rect.inflate(-2, -2))

    def _draw_side_panel(self, screen: pygame.Surface, font: pygame.font.Font) -> None:
        panel_x = GRID_WIDTH * CELL_SIZE
        pygame.draw.rect(
            screen,
            (28, 28, 36),
            pygame.Rect(panel_x, 0, SIDE_PANEL, SCREEN_HEIGHT),
        )
        title = font.render("TETRIS", True, WHITE)
        score = font.render(f"Score: {self.score}", True, WHITE)
        hint_1 = font.render("Arrows: move", True, WHITE)
        hint_2 = font.render("Up: rotate", True, WHITE)
        hint_3 = font.render("Space: drop", True, WHITE)
        screen.blit(title, (panel_x + 30, 24))
        screen.blit(score, (panel_x + 20, 80))
        screen.blit(hint_1, (panel_x + 20, 150))
        screen.blit(hint_2, (panel_x + 20, 180))
        screen.blit(hint_3, (panel_x + 20, 210))

        preview = font.render("Next:", True, WHITE)
        screen.blit(preview, (panel_x + 20, 280))
        preview_piece = self.next_piece
        for y, row in enumerate(preview_piece.shape):
            for x, value in enumerate(row):
                if value == 0:
                    continue
                rect = pygame.Rect(panel_x + 20 + x * 22, 320 + y * 22, 20, 20)
                pygame.draw.rect(screen, preview_piece.color, rect)


def run_game() -> None:
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Python Tetris")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 24)

    game = Tetris()
    fall_event = pygame.USEREVENT + 1
    pygame.time.set_timer(fall_event, FALL_INTERVAL_MS)

    running = True
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == fall_event and not game.game_over:
                game.move(0, 1)
            elif event.type == pygame.KEYDOWN and not game.game_over:
                if event.key == pygame.K_LEFT:
                    game.move(-1, 0)
                elif event.key == pygame.K_RIGHT:
                    game.move(1, 0)
                elif event.key == pygame.K_DOWN:
                    game.move(0, 1)
                elif event.key == pygame.K_UP:
                    game.rotate()
                elif event.key == pygame.K_SPACE:
                    game.drop()

        game.draw(screen, font)

        if game.game_over:
            over = font.render("Game Over! Press ESC", True, (255, 80, 80))
            screen.blit(over, (24, SCREEN_HEIGHT // 2 - 20))
            pygame.display.flip()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                running = False

    pygame.quit()
    sys.exit(0)


if __name__ == "__main__":
    run_game()
