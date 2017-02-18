import math

START = (10, 10)
END = (95, 47)

blocks = [
    (12, 36, 36, 38), # Block 1
    (47, 48, 49, 26), # Block 2
    (38, 24, 58, 26), # Block 3
    (66, 48, 82.75, 28.5), # Block 4
    (60, 12, 73.25, 20.5), # Block 5
    (12, 24, 31.25, 13.5) # Block 6
]

WR = 4
waypoints = {
    # Block 1 waypoints
    'w11': (blocks[0][0]-WR, blocks[0][3]+WR),
    'w12': (blocks[0][2]+WR, blocks[0][3]+WR),
    'w13': (blocks[0][2]+WR, blocks[0][1]-WR),
    'w14': (blocks[0][0]-WR, blocks[0][1]-WR),
    # No waypoints for block 2
    # Block 3 waypoints
    'w31': (blocks[2][0]-WR, blocks[2][3]+WR),
    'w32': (blocks[2][2]+WR, blocks[2][3]+WR),
    'w33': (blocks[2][2]+WR, blocks[2][1]-WR),
    'w34': (blocks[2][0]-WR, blocks[2][1]-WR),
    # Block 4 waypoints
    'w41': (86, 28),
    'w42': (82.75, 24.5),
    # Block 5 waypoints
    'w51': (56, 12),
    'w52': (70, 26),
    'w53': (78, 20.5),
    'w54': (62, 6),
    # Block 6 waypoints
    'w61': (12, 28),
    'w62': (35, 16),
    'w63': (31, 7),
    'w64': (6, 22)
}

connections = {
    # Block 1 waypoints
    'w11': ['w12', 'w14'],
    'w12': ['w13', 'w11'],
    'w13': ['w12', 'w31', 'w61', 'w14'],
    'w14': ['w11', 'w13', 'w31', 'w34', 'w62', 'w61', 'w64'],
    # No waypoints for block 2
    # Block 3 waypoints
    'w31': ['w13', 'w34', 'w61', 'w14'],
    'w32': ['w42', 'w52', 'w33'],
    'w33': ['w32', 'w52', 'w51', 'w34'],
    'w34': ['w31', 'w33', 'w51', 'w62', 'w61', 'w14'],
    # Block 4 waypoints
    'w41': ['w42'],
    'w42': ['w41', 'w53', 'w52', 'w32'],
    # Block 5 waypoints
    'w51': ['w33', 'w52', 'w54', 'w63', 'w62', 'w61', 'w34'],
    'w52': ['w42', 'w53', 'w33', 'w32'],
    'w53': ['w42', 'w54', 'w52'],
    'w54': ['w53', 'w63', 'w62', 'w34', 'w51'],
    # Block 6 waypoints
    'w61': ['w13', 'w31', 'w34', 'w51', 'w62', 'w64', 'w14'],
    'w62': ['w34', 'w51', 'w54', 'w63', 'w61', 'w14'],
    'w63': ['w62', 'w51', 'w54', 'w64'],
    'w64': ['w14', 'w61', 'w63']
}

nodes = {
    'w11':([], -1), 'w12':([], -1), 'w13':([], -1), 'w14':([], -1),
    'w31':([], -1), 'w32':([], -1), 'w33':([], -1), 'w34':([], -1),
    'w41':([], -1), 'w42':([], -1),
    'w51':([], -1), 'w52':([], -1), 'w53':([], -1), 'w54':([], -1),
    'w61':([], -1), 'w62':([], -1), 'w63':([], -1), 'w64':([], -1)
}

def distance(a, b):
    return math.sqrt((a[0]-b[0])**2 +(a[1]-b[1])**2)

startW = None
endW = None
minStart = 0
minEnd = 0
for w, coord in waypoints.items():

    d = distance(START, coord)
    if startW is None or d < minStart:
        startW = w
        minStart = d
    d = distance(END, coord)
    if endW is None or d < minEnd:
        endW = w
        minEnd = d
assert(startW is not None and endW is not None)

nodes[startW] = ([startW], 0)
while nodes[endW][1] < 0:
    closestNewNode = ('', [], -1)
    for key, _ in nodes.items():
        # Get our discovered and check their connections.
        if (nodes[key][1] != -1):
            for edge in connections[key]:
                edgeLen = distance(waypoints[key], waypoints[edge])
                dist = nodes[key][1] + edgeLen
                # If this node is the closest and the endpoint is a point that
                # is not yet discovered.
                if ((closestNewNode[2] == -1 or dist < closestNewNode[2]) and
                    nodes[edge][1] == -1):
                    path = nodes[key][0][:]
                    path.append(edge)
                    closestNewNode = (edge, path, dist)
    nodes[closestNewNode[0]] = (closestNewNode[1], closestNewNode[2])

print(nodes[endW])
