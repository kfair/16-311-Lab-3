import pprint
import math
resolution = 2
HEIGHT = 4 * 12
WIDTH = 8 * 12
START = (10, 10)
END = (95, 47)

WIDTH_IDX = WIDTH // resolution
HEIGHT_IDX = HEIGHT // resolution

def inToIdx(x):
    return int(x/resolution)

grid = [[0 for y in range(HEIGHT_IDX)] for x in range(WIDTH_IDX)]
blocks = [
    (12, 36, 36, 38),
    (47, 48, 49, 26),
    (38, 24, 58, 26),
    (66, 48, 82.75, 28.5),
    (60, 12, 73.25, 20.5),
    (12, 24, 31.25, 13.5)
]
for col in range(len(grid)):
    for row in range(len(grid[col])):
        x0 = col * resolution
        y0 = row * resolution
        wall = 0
        for (x1, y1, x2, y2) in blocks:
            d = (abs((x2 - x1) * (y1 - y0) - (x1 - x0) * (y2 - y1)) /
                math.sqrt((x2 - x1)**2 + (y2 - y1)**2))
            if (d < resolution and min(x1, x2) <= x0 and x0 <= max(x1, x2)
                and min(y1, y2) <= y0 and y0 <= max(y1, y2)):
                wall = 1
                break
        grid[col][row] = wall

grid[inToIdx(END[0])][inToIdx(END[1])] = 2
counter = 2


while grid[inToIdx(START[0])][inToIdx(START[1])] == 0:
    for col in range(len(grid)):
        for row in range(len(grid[col])):
            if grid[col][row] == counter:
                for i in range(0, 3):
                    for j in range(0, 3):
                        if (i != j and
                            0 <= col + i - 1 and col + i - 1 < WIDTH_IDX and
                            0 <= row + j - 1 and row + j - 1 < HEIGHT_IDX and
                            grid[col + i - 1][row + j - 1] == 0):
                            grid[col + i - 1][row + j - 1] = counter + 1
    counter = counter + 1
pp = pprint.PrettyPrinter(depth=6, width=10000)
for i in grid:
    pp.pprint(i)
