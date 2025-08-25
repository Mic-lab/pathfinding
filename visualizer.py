import pygame
import sys
from path_finder import calc_path, get_path, get_grid

CELL_SIZE = (32, 32)
GRID_SIZE = (32, 18)
SCREEN_SIZE = CELL_SIZE[0] * GRID_SIZE[0], CELL_SIZE[1] * GRID_SIZE[1]

def update_path():
    formatted_grid, start, end = get_grid(grid)
    calc_path(formatted_grid, start, end, GRID_SIZE)
    path = get_path(start, end)
    return path

pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
clock = pygame.time.Clock()
font = pygame.font.SysFont('Courier New', 16)

grid = [ [0] * GRID_SIZE[0] for i in range(GRID_SIZE[1]) ]

path = []

end_pos = (28, 10)
shift_down = False

mouse_down = False
right_down = False
running = True
while running:

    update = False
    mx, my = pygame.mouse.get_pos()
    if mx < 0: mx = 0
    if my < 0: my = 0
    if mx > SCREEN_SIZE[0]: mx = SCREEN_SIZE[0]
    if my > SCREEN_SIZE[1]: my = SCREEN_SIZE[1]
    grid_pos = mx // CELL_SIZE[0], my//CELL_SIZE[1]

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            update = True
            if event.button == 1:
                mouse_down = True
            if event.button == 3:
                right_down = True

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                mouse_down = False
            if event.button == 3:
                right_down = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LSHIFT:
                update = True
                shift_down = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LSHIFT:
                shift_down = False

    screen.fill((0, 0, 0))

    if shift_down:
        grid[end_pos[1]][end_pos[0]] = 0
        end_pos = grid_pos
        update = True

    if mouse_down:
        if grid[grid_pos[1]][grid_pos[0]] != 1:
            update = True
            grid[grid_pos[1]][grid_pos[0]] = 1
    if right_down:
        if grid[grid_pos[1]][grid_pos[0]] != 0:
            update = True
            grid[grid_pos[1]][grid_pos[0]] = 0

    grid[6][12] = 2
    grid[end_pos[1]][end_pos[0]] = 3

    if update:
        path = update_path()

    for y, row in enumerate(grid):
        y_i = y
        y *= CELL_SIZE[1]
        for x, cell in enumerate(row):
            x_i = x
            x *= CELL_SIZE[0]
            w, h = CELL_SIZE
            r = pygame.Rect(x, y, w, h)
            if cell == 0:
                color = (20, 20, 25)
                for path_cell in path:
                    if (path_cell.x, path_cell.y) == (x_i, y_i):
                        color = (40, 45, 100)
                        break
            elif cell == 1:
                color = (180, 200, 220)
            elif cell == 2:
                color = (100, 180, 100)
            elif cell == 3:
                color = (180, 100, 100)

            pygame.draw.rect(screen, color, r)

            # cell = grid[i][j]

    # for row in grid:
    #     for cell in grid:
    #         if 

    screen.blit(font.render(f'{grid_pos}', False, (0, 255, 255)), (0, 0))

    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()
