import math
resolution = 2
HEIGHT = 4 * 12
WIDTH = 8 * 12
START = (10, 10)
END = (95, 47)

ROBOT_RADIUS = 1
BLOCK_WIDTH = 2

WIDTH_IDX = WIDTH // resolution
HEIGHT_IDX = HEIGHT // resolution

def inToIdx(x):
    return int(x/resolution)

grid = [[0 for x in range(WIDTH_IDX)] for y in range(HEIGHT_IDX)]
blocks = [
    (12, 36, 36, 38),
    (47, 48, 49, 26),
    (38, 24, 58, 26),
    (66, 48, 82.75, 28.5),
    (60, 12, 73.25, 20.5),
    (12, 24, 31.25, 13.5)
]
for row in range(len(grid)):
    for col in range(len(grid[row])):
        x0 = col * resolution
        y0 = row * resolution
        wall = 0
        for (x1, y1, x2, y2) in blocks:
            d = (abs((x2 - x1) * (y1 - y0) - (x1 - x0) * (y2 - y1)) /
                math.sqrt((x2 - x1)**2 + (y2 - y1)**2))
            if (d < BLOCK_WIDTH + ROBOT_RADIUS and
                min(x1, x2) <= x0 and x0 <= max(x1, x2) and
                min(y1, y2) <= y0 and y0 <= max(y1, y2)):
                wall = -1
                break
        grid[row][col] = wall

grid[inToIdx(END[1])][inToIdx(END[0])] = 2
counter = 2
formatS = ' '.join(['%03d ' for x in range(WIDTH_IDX)])

for row in range(len(grid)-1, -1, -1):
    print(formatS % tuple(grid[row]))
print('\n\n')
while grid[inToIdx(START[1])][inToIdx(START[0])] == 0:
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            if grid[row][col] == counter:
                for i in range(0, 3):
                    for j in range(0, 3):
                        if (i != j and
                            0 <= col + i - 1 and col + i - 1 < WIDTH_IDX and
                            0 <= row + j - 1 and row + j - 1 < HEIGHT_IDX and
                            grid[row + j - 1][col + i - 1] == 0):
                            grid[row + j - 1][col + i - 1] = counter + 1
    counter = counter + 1


for row in range(len(grid)-1, -1, -1):
    print(formatS % tuple(grid[row]))
