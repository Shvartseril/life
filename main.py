import pygame
from typing import Tuple, List, Set


WIDTH = 400
HEIGHT = 400
FPS = 100
TURN_TIME = 200


def redraw(surface, squares):
    surface.fill((0, 0, 0))
    # pygame.draw.rect(surface, (255, 0, 0), pygame.Rect(100, 50, 200, 250))
    for square in squares:
        pygame.draw.rect(surface, (255, 0, 0), pygame.Rect(square[0] * 10, square[1] * 10, 10, 10))
        # pygame.draw.circle(surface, (255, 0, 0), ((square[0] + 1) * 10, (square[1] + 1) * 10), 2)
    draw_field(surface)
    pygame.display.flip()


def make_turn(squares: Set[Tuple[int, int]]) -> Set[Tuple[int, int]]:
    new_squares = set()
    for i in range(40):
        for j in range(40):
            square = i, j
            alive_neighbours = count_alive_neighbours(square, squares)
            if alive_neighbours == 2 and square in squares:
                new_squares.add(square)
            if alive_neighbours == 3:
                new_squares.add(square)
    return new_squares


def count_alive_neighbours(pos: Tuple[int, int], squares: Set[Tuple[int, int]]) -> int:
    alive_neighbours = 0
    for offset in [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (1, 1), (0, 1), (-1, 1)]:
        neighbour = (pos[0] + offset[0]) % 40, (pos[1] + offset[1]) % 40
        if neighbour in squares:
            alive_neighbours += 1
    return alive_neighbours


def draw_field(surface):
    for i in range(0, WIDTH, 10):
        pygame.draw.line(surface, (201, 200, 200), (0, i), (WIDTH, i))
    for i in range(0, HEIGHT, 10):
        pygame.draw.line(surface, (201, 200, 200), (i, 0), (i, HEIGHT))


def get_cell_by_coordinates(coordinates: Tuple[int, int]) -> Tuple[int, int]:
    x = coordinates[0]
    y = coordinates[1]
    return x // 10, y // 10


def main():
    squares = set()
    pygame.init()
    pygame.display.init()
    screen = pygame.display.set_mode((400, 400))
    last_redraw = -1000
    last_make_turn = -1000
    running = True
    stop = False
    while running:
        if pygame.time.get_ticks() - last_make_turn > TURN_TIME and not stop:
            squares = make_turn(squares)
            last_make_turn = pygame.time.get_ticks()
        if pygame.time.get_ticks() - last_redraw > 1000 // FPS:
            redraw(screen, squares)
            last_redraw = pygame.time.get_ticks()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                squares.add(get_cell_by_coordinates(event.pos))
                # print(event.pos)
                # print(get_cell_by_coordinates(event.pos))
            if event.type == pygame.KEYDOWN:
                if event.key == 13:
                    squares = set()
                elif event.key == 32:
                    stop = not stop
            # print(event)
    pygame.display.quit()


if __name__ == '__main__':
    main()
