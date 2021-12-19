from collections import namedtuple, defaultdict, deque

mod = namedtuple("mod", ["flip", "rotate", "shift"])

f = open('data/prob19.dat')

inf = float('inf')
scanner_reads = []
for line in f.readlines():
    if line.startswith("---"):
        scanner_reads.append(set())
    elif line.strip():
        scanner_reads[-1].add(tuple(map(int, line.replace(' ', '').strip().split(','))))

def overlap(m1, m2, D):
    overlaps = 0
    next_hop = inf
    i, j = 0, 0
    lenM1 = len(m1)
    lenM2 = len(m2)
    while i < lenM1 and j < lenM2:
        n = m2[j] + D
        if m1[i] > n:
            next_hop = min(next_hop, m1[i] - n)
            j += 1
        elif m1[i] < n:
            next_hop = min(next_hop, n - m1[i])
            i += 1
        else:
            overlaps += 1
            j += 1
            i += 1
    return overlaps, D + next_hop


def axis_metric(data, key):
    return sorted([key(point) for point in data])


def axes_all(s):
    yield False, 0, axis_metric(scanner_reads[s], key=lambda point: point[0]),
    yield True, 0, axis_metric(scanner_reads[s], key=lambda point: -point[0]),
    yield False, 1, axis_metric(scanner_reads[s], key=lambda point: point[1]),
    yield True, 1, axis_metric(scanner_reads[s], key=lambda point: -point[1]),
    yield False, 2, axis_metric(scanner_reads[s], key=lambda point: point[2]),
    yield True, 2, axis_metric(scanner_reads[s], key=lambda point: -point[2]),

def axes_positive(s):
    yield 0, axis_metric(scanner_reads[s], key=lambda point: point[0]),
    yield 1, axis_metric(scanner_reads[s], key=lambda point: point[1]),
    yield 2, axis_metric(scanner_reads[s], key=lambda point: point[2]),


def find_modification_set(scannerA, scannerB):
    mods = {}
    for o1, m1 in axes_positive(scannerA):
        for r2, o2, m2 in axes_all(scannerB):
            d_min, d_max = -2002, 2002
            d = d_min
            while d < d_max:
                i, next_d = overlap(m1, m2, d)
                if i < 12:
                    d = next_d
                else:
                    mods[o1] = mod(r2, o2, d)
                    d = d_max
    return mods


def modify(points, modification):
    return {(
        p[modification[0].rotate] * (-1 if modification[0].flip else 1) + modification[0].shift,
        p[modification[1].rotate] * (-1 if modification[1].flip else 1) + modification[1].shift,
        p[modification[2].rotate] * (-1 if modification[2].flip else 1) + modification[2].shift)
        for p in points}

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
        x = find_modification_set(i, j)
        if x:
            transfers[j, i] = x
            graph[i].add(j)
            to_reach.remove(j)
            work.append(j)
            print('reached', j, 'from', i, 'remaining', to_reach)


points = {i: scanner_reads[i] for i in range(len(scanner_reads))}
scanner_loc = {i: {(0, 0, 0), } for i in range(len(scanner_reads))}


visited = set()
def dfs(c, p=None):
    visited.add(c)
    for n in graph[c]:
        if n not in visited:
            dfs(n, c)

    if p is not None:
        print("migrating from", c, "to", p)
        points[p].update(modify(points[c], transfers[c, p]))
        scanner_loc[p].update(modify(scanner_loc[c], transfers[c, p]))

dfs(0)
print(len(points[0]))

def manhattan(point1, point2):
    return abs(point1[0] - point2[0]) + abs(point1[1] - point2[1]) + abs(point1[2] - point2[2])

best = -1
for point1 in scanner_loc[0]:
    for point2 in scanner_loc[0]:
        d = manhattan(point1, point2)
        best = max(best, d)

print(best)
