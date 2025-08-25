# https://www.youtube.com/watch?v=-L-WgKMFuhE
from time import perf_counter

class Tile:

    def __init__(self, x, y):
        self.x, self.y = x, y
        self.g = None  # distance from starting tile
        self.h = None  # distance from end node
        self.f = None  # g + h
        self.parent = None

    def update(self, potential_parent, start, end):
        if self.h is None:
            self.calc_h(end)

        # NOTE: Could probably just create a distance function that can be used for this and also calc_h
        if abs(self.x - potential_parent.x) == 1 and abs(self.y - potential_parent.y) == 1:
            parent_dist = 14  # diagonal
        else:
            parent_dist = 10  # straight

        if potential_parent is start:
            potential_g = parent_dist
        else:
            potential_g = potential_parent.g + parent_dist

        if self.g is None or potential_g < self.g:
            self.parent = potential_parent
            self.g = potential_g
            self.f = self.g + self.h

    def calc_h(self, end):
        end_dist = (abs(self.x - end.x), abs(self.y - end.y))
        if end_dist[0] > end_dist[1]:
            big = end_dist[0]
            small = end_dist[1]
        else:
            big = end_dist[1]
            small = end_dist[0]
        diagonals = small
        cardinals = big - small
        self.h = (diagonals * 14 + cardinals * 10) * 1.001  # https://theory.stanford.edu/~amitp/GameProgramming/Heuristics.html#breaking-ties

    def __repr__(self):
        return f'Tile({self.x}, {self.y})'

def get_grid(grid_inp):
    grid = []
    for y, row in enumerate(grid_inp):
        grid.append([])
        for x, tile_num in enumerate(row):
            if tile_num == 1:
                tile = False
            else:
                tile = Tile(x, y)
                if tile_num == 2:
                    start = tile
                elif tile_num == 3:
                    end = tile
            grid[y].append(tile)
    return grid, start, end

def calc_path(grid, start, end, grid_size):
    t0 = perf_counter()

    open_tiles = {start}
    close_tiles = set()

    while True:
        current = next(iter(open_tiles))
        for tile in open_tiles:
            if tile.f is None: continue
            if tile.f == current.f:
                if tile.g < current.g:
                    current = tile
            elif tile.f < current.f:
                current = tile
        
        open_tiles.remove(current) # NOTE: Can be optimized with pop
        close_tiles.add(current)

        if current is end:
            t1 = perf_counter()
            time_taken = round(t1 - t0, 4)
            print(f'close_tiles explored {len(close_tiles)} ({time_taken} s)')
            return

        for offset in neighbor_offset:
            x, y = current.x - offset[0], current.y - offset[1]

            if x < 0 or y < 0 or x == grid_size[0] or y == grid_size[1]:
                continue

            neighbor_tile = grid[y][x]
            if not neighbor_tile or neighbor_tile in close_tiles:
                continue
            neighbor_tile.update(current, start, end)
            open_tiles.add(neighbor_tile)

def get_path(start, end):
    path = []
    current = end
    while True:
        path.append(current.parent)
        current = current.parent
        if current is start:
            return path
        
neighbor_offset = set()
for x in range(-1, 2):
    for y in range(-1, 2):
        coord = (x, y)
        if coord == (0, 0):
            continue
        neighbor_offset.add(coord)
