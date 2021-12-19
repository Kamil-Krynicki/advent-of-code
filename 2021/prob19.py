from collections import namedtuple, defaultdict, deque
from datetime import datetime

mod = namedtuple("mod", ["flip", "rotate", "shift"])

f = open('data/prob19.dat')

visibility = 1000

scanner_reads = []
for line in f.readlines():
    if line.startswith("---"):
        scanner_reads.append(set())
    elif line.strip():
        scanner_reads[-1].add(tuple(map(int, line.replace(' ', '').strip().split(','))))

def axis_metric(data, key):
    return sorted([key(point) for point in data])

def overlap(m1, m2, delta):
    ans = 0
    next_hop = 10 ** 10
    i, j = 0, 0
    while i < len(m1) and j < len(m2):
        if m1[i] == (m2[j] + delta):
            ans, i, j = ans + 1, i+1, j+1
        elif m1[i] > (m2[j] + delta):
            next_hop = min(next_hop, abs(m1[i] - m2[j] - delta))
            j = j + 1
        elif m1[i] < (m2[j] + delta):
            next_hop = min(next_hop, abs(m2[j] + delta - m1[i]))
            i = i + 1
    return ans, delta + next_hop


def axesB(scanner):
    yield False, 0, axis_metric(scanner, key=lambda point: point[0])
    yield True, 0, axis_metric(scanner, key=lambda point: -point[0])
    yield False, 1, axis_metric(scanner, key=lambda point: point[1])
    yield True, 1, axis_metric(scanner, key=lambda point: -point[1])
    yield False, 2, axis_metric(scanner, key=lambda point: point[2])
    yield True, 2, axis_metric(scanner, key=lambda point: -point[2])

def axesA(scanner):
    yield False, 0, axis_metric(scanner, key=lambda point: point[0])
    yield False, 1, axis_metric(scanner, key=lambda point: point[1])
    yield False, 2, axis_metric(scanner, key=lambda point: point[2])


def find_modification_set(from_points, to_points):
    mods = {}
    for _, o1, m1 in axesA(from_points):
        for r2, o2, m2 in axesB(to_points):
            max_i = 11
            max_d = -1
            d = -(2 * visibility + 2)
            while d < 2 * visibility:
                i, next_d = overlap(m1, m2, d)
                if i > max_i:
                    max_i = i
                    max_d = d
                d = next_d

            if max_i > 11:
                mods[o1] = mod(r2, o2, max_d)
                print(max_d, max_i)

    return mods


def modify(points, modification):
    return {(
        p[modification[0].rotate] * (-1 if modification[0].flip else 1) + modification[0].shift,
        p[modification[1].rotate] * (-1 if modification[1].flip else 1) + modification[1].shift,
        p[modification[2].rotate] * (-1 if modification[2].flip else 1) + modification[2].shift)
        for p in points}


t1 = datetime.now()

graph = defaultdict(set)
transfers = {}

work = deque()
work.append(0)

to_reach = set(range(len(scanner_reads)))
to_reach.remove(0)

while to_reach:
    i = work.pop()
    if i in graph:
        continue
    for j in set(to_reach):
        print('i =', i, 'j =', j)
        x = find_modification_set(scanner_reads[i], scanner_reads[j])
        if x:
            transfers[j, i] = x
            graph[i].add(j)
            to_reach.remove(j)
            work.append(j)
            print('reached', j, 'from', i, 'remaining', to_reach)

out = set()
visited = set()

points = {i: scanner_reads[i] for i in range(len(scanner_reads))}
scanner_loc = {i: {(0, 0, 0), } for i in range(len(scanner_reads))}


def dfs(c, p=None):
    visited.add(c)
    for n in graph[c]:
        if n in visited:
            continue
        visited.add(n)
        dfs(n, c)

    if p is not None:
        print("migrating from", c, "to", p)
        points[p].update(modify(points[c], transfers[c, p]))
        scanner_loc[p].update(modify(scanner_loc[c], transfers[c, p]))

dfs(0)
sanity = {(-892,524,684), (-876,649,763), (-838,591,734), (-789,900,-551), (-739,-1745,668), (-706,-3180,-659), (-697,-3072,-689), (-689,845,-530), (-687,-1600,576), (-661,-816,-575), (-654,-3158,-753), (-635,-1737,486), (-631,-672,1502), (-624,-1620,1868), (-620,-3212,371), (-618,-824,-621), (-612,-1695,1788), (-601,-1648,-643), (-584,868,-557), (-537,-823,-458), (-532,-1715,1894), (-518,-1681,-600), (-499,-1607,-770), (-485,-357,347), (-470,-3283,303), (-456,-621,1527), (-447,-329,318), (-430,-3130,366), (-413,-627,1469), (-345,-311,381), (-36,-1284,1171), (-27,-1108,-65), (7,-33,-71), (12,-2351,-103), (26,-1119,1091), (346,-2985,342), (366,-3059,397), (377,-2827,367), (390,-675,-793), (396,-1931,-563), (404,-588,-901), (408,-1815,803), (423,-701,434), (432,-2009,850), (443,580,662), (455,729,728), (456,-540,1869), (459,-707,401), (465,-695,1988), (474,580,667), (496,-1584,1900), (497,-1838,-617), (527,-524,1933), (528,-643,409), (534,-1912,768), (544,-627,-890), (553,345,-567), (564,392,-477), (568,-2007,-577), (605,-1665,1952), (612,-1593,1893), (630,319,-379), (686,-3108,-505), (776,-3184,-501), (846,-3110,-434), (1135,-1161,1235), (1243,-1093,1063), (1660,-552,429), (1693,-557,386), (1735,-437,1738), (1749,-1800,1813), (1772,-405,1572), (1776,-675,371), (1779,-442,1789), (1780,-1548,337), (1786,-1538,337), (1847,-1591,415), (1889,-1729,1762), (1994,-1805,1792)}
print(sanity == points[0])
print(scanner_loc[0])

def manhattan(point1, point2):
    return abs(point1[0] - point2[0]) + abs(point1[1] - point2[1]) + abs(point1[2] - point2[2])

best = -1
for point1 in scanner_loc[0]:
    for point2 in scanner_loc[0]:
        d = manhattan(point1, point2)
        best = max(best, d)

print(best)

t2 = datetime.now()

print(t2 - t1)

