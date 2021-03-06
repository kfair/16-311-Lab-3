import math
from shapely.geometry import LineString
import copy
# Measurements in inches
l1 = 3.75
l2 = 2.5

start = (0, 0) #(t1, t2) degrees
A = (3.75, 2.5) #(x, y) inches
B = (-3.75, 2.5) #(x, y) inches

obstacle = [LineString([(-2.5, 8.5), (2.5, 8.5)]),
            LineString([(2.5, 8.5), (2.5, 5)]),
            LineString([(2.5, 5), (-2.5, 5)]),
            LineString([(-2.5, 5), (-2.5, 8.5)]),
            # Workspace boundaries:
            LineString([(-7.1, 8.1), (7.1, 8.1)]),
            LineString([(7.1, 8.1), (7.1, -0.1)]),
            LineString([(7.1, -0.1), (-7.1, -0.1)]),
            LineString([(-7.1, -0.1), (-7.1, 8.1)])
            ]

t1range, t2range = 180, 360;
cspace = [[0 for y in range(0, t2range)] for x in range(0, t1range)] 

def t1_to_i(t):
    return round(t)

def t2_to_i(t):
    return round(t + 180)

def i_to_t1(i):
    return i

def i_to_t2(i):
    return i - 180

for t1 in range(0, 180):
    for t2 in range(-180, 180):
        t1r = math.radians(t1)
        t2r = math.radians(t2)
        x2 = l1 * math.cos(t1r) + l2 * math.cos(t1r + t2r)
        y2 = l1 * math.sin(t1r) + l2 * math.sin(t1r + t2r)
        x1 = l1 * math.cos(t1r)
        y1 = l1 * math.sin(t1r)
        ls1 = LineString([(0, 0), (x1, y1)])
        ls2 = LineString([(x1, y1), (x2, y2)])
        # If either linestring intersects a line in the rectangle, we know the
        # point is invalid.
        valid = 0
        for ol in obstacle:
            if ol.crosses(ls1) or ol.crosses(ls2):
                valid = 1
        cspace[t1_to_i(t1)][t2_to_i(t2)] = valid
            
def inv_kinematics(p):
    t21 = math.acos((p[0] * p[0] + p[1] * p[1] - l1 * l1 - l2 * l2) \
            /(2 * l1 * l2))
    t22 = -t21
    t11 = math.atan2(p[1], p[0]) \
            - math.asin(l2 * math.sin(t21)/math.sqrt(p[0]*p[0] + p[1] * p[1]))
    t12 = math.atan2(p[1], p[0]) \
            - math.asin(l2 * math.sin(t22)/math.sqrt(p[0]*p[0] + p[1] * p[1]))
    return [(t11, t21), (t12, t22)]

# t11, t21, t12, t22 are the endpoint coordinates
# st1, st2 are the starting angles.
def pick_better_config(points, start):
    [(t11, t21), (t12, t22)] = points
    (st1, st2) = start
    firstValid = 0 <= t11 and t11 < 180 and cspace[t1_to_i(t11)][t2_to_i(t21)] == 1
    secondValid = 0 <= t12 and t12 < 180 and cspace[t1_to_i(t12)][t2_to_i(t22)] == 1
    if firstValid and not secondValid:
        return (t11, t21)
    elif not firstValid and secondValid:
        return (t21, t22)
    else:
        # We'll use the L1 metric wrt the configuration space for closest point.
        d1 = abs(t11 - st1) + abs(t21 - st2)
        d2 = abs(t12 - st1) + abs(t22 - st2)
        if d1 < d2:
            return (t11, t21)
        else:
            return (t12, t22)
print(inv_kinematics(B))
(At1, At2) = pick_better_config(inv_kinematics(A), start)
(Bt1, Bt2) = pick_better_config(inv_kinematics(B), (At1, At2))
(Ct1, Ct2) = pick_better_config(inv_kinematics(A), (Bt1, Bt2))

At1 = math.degrees(At1)
At2 = math.degrees(At2)
Bt1 = math.degrees(Bt1)
Bt2 = math.degrees(Bt2)
Ct1 = math.degrees(Ct1)
Ct2 = math.degrees(Ct2)

def wavefront(startAngles, endAngles):
    (st1, st2) = startAngles
    (et1, et2) = endAngles
    # Get the starting indices
    st1i = t1_to_i(st1)
    st2i = t2_to_i(st2)
    startOnGrid = i_to_t1(st1i) == st1 and i_to_t2(st2i) == st2
    et1i = t1_to_i(et1)
    et2i = t2_to_i(et2)
    endOnGrid = i_to_t1(et1i) == et1 and i_to_t2(et2i) == et2
    # Make a copy of the space.
    cspace2 = copy.deepcopy(cspace)
    cspace2[et1i][et2i] = 2
    while cspace2[st1i][st2i] == 0:
        for t1 in range(0, len(cspace2)):
            for t2 in range(0, len(cspace2[t1])):
                v = cspace2[t1][t2]
                if v >= 2:
                    # 4 point connectivity.
                    if t1 + 1 < t1range and cspace2[t1 + 1][t2] == 0:
                        cspace2[t1 + 1][t2] = v + 1
                    if t1 - 1 >= 0 and cspace2[t1 - 1][t2] == 0:
                        cspace2[t1 - 1][t2] = v + 1
                    if t2 + 1 < t2range and cspace2[t1][t2 + 1] == 0:
                        cspace2[t1][t2 + 1] = v + 1
                    if t2 - 1 >= 0 and cspace2[t1][t2 - 1] == 0:
                        cspace2[t1][t2 - 1] = v + 1

    direction = None
    (t1, t2) = (st1i, st2i)
    positions = [startAngles]
    if not startOnGrid:
        positions.append((i_to_t1(st1i), i_to_t2(st2i)))
    v = cspace2[t1][t2];
    while v > 2:
        v = v-1
        if not((direction=='t1+1' and t1+1<t1range and cspace2[t1+1][t2]==v) or\
            (direction=='t1-1' and t1-1>=0 and cspace2[t1-1][t2]==v) or \
            (direction=='t2+1' and t2+1<t2range and cspace2[t1][t2+1]==v) or \
            (direction=='t2-1' and t2-1>=0 and cspace2[t1][t2-1]==v)):
            # Change directions.
            if t1+1<t1range and cspace2[t1+1][t2] == v:
                if direction is not None:
                    positions.append((i_to_t1(t1), i_to_t2(t2)))
                direction = 't1+1'
                t1 = t1+1
            elif t1-1>=0 and cspace2[t1-1][t2] == v:
                if direction is not None:
                    positions.append((i_to_t1(t1), i_to_t2(t2)))
                direction = 't1-1'
                t1 = t1-1
            elif t2+1<t2range and cspace2[t1][t2+1] == v:
                if direction is not None:
                    positions.append((i_to_t1(t1), i_to_t2(t2)))
                direction = 't2+1'
                t2 = t2+1
            elif t2-1>=0 and cspace2[t1][t2-1] == v:
                if direction is not None:
                    positions.append((i_to_t1(t1), i_to_t2(t2)))
                direction = 't2-1'
                t2 = t2-1
            else:
                print("Error changing direction")
                print(t1, t2)
                break
        else:
            if direction == 't1+1':
                t1 = t1 + 1
            elif direction == 't1-1':
                t1 = t1 - 1
            elif direction == 't2+1':
                t2 = t2 + 1
            elif direction == 't2-1':
                t2 = t2 - 1
            else:
                print("Error going in same direction")
                print(direction)
                break
    positions.append((i_to_t1(et1i), i_to_t2(et2i)))
    if not endOnGrid:
        positions.append(endAngles)
    return positions

moves1 = wavefront(start, (At1, At2))
moves2 = wavefront((At1, At2), (Bt1, Bt2))
moves3 = wavefront((Bt1, Bt2), (Ct1, Ct2))
# Moves 4 gets us back to (0, 0)
moves4 = wavefront((Ct1, Ct2), (0, 0))
for a, b in moves1:
    if abs(a) < 0.01:
        a = 0
    if abs(b) < 0.01:
        b = 0
    print("move(" + str(a) + ", " + str(b) + ");")
print("wait1Msec(3000);")
print("// At point A")
for a, b in moves2:
    if abs(a) < 0.01:
        a = 0
    if abs(b) < 0.01:
        b = 0
    print("move(" + str(a) + ", " + str(b) + ");")
print("wait1Msec(3000);")
print("// At point B")
for a, b in moves3:
    if abs(a) < 0.01:
        a = 0
    if abs(b) < 0.01:
        b = 0
    print("move(" + str(a) + ", " + str(b) + ");")
print("wait1Msec(3000);")
print("// At point A")
for a, b in moves4:
    if abs(a) < 0.01:
        a = 0
    if abs(b) < 0.01:
        b = 0
    print("move(" + str(a) + ", " + str(b) + ");")
