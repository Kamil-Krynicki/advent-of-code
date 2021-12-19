from collections import namedtuple, defaultdict, deque

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


def axes_all(scanner):
    yield False, 0, axis_metric(scanner, key=lambda point: point[0])
    yield True, 0, axis_metric(scanner, key=lambda point: -point[0])
    yield False, 1, axis_metric(scanner, key=lambda point: point[1])
    yield True, 1, axis_metric(scanner, key=lambda point: -point[1])
    yield False, 2, axis_metric(scanner, key=lambda point: point[2])
    yield True, 2, axis_metric(scanner, key=lambda point: -point[2])

def axes_positive(scanner):
    yield False, 0, axis_metric(scanner, key=lambda point: point[0])
    yield False, 1, axis_metric(scanner, key=lambda point: point[1])
    yield False, 2, axis_metric(scanner, key=lambda point: point[2])


def find_modification_set(from_points, to_points):
    mods = {}
    for _, o1, m1 in axes_positive(from_points):
        for r2, o2, m2 in axes_all(to_points):
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
print(len(points[0]))

def manhattan(point1, point2):
    return abs(point1[0] - point2[0]) + abs(point1[1] - point2[1]) + abs(point1[2] - point2[2])

best = -1
for point1 in scanner_loc[0]:
    for point2 in scanner_loc[0]:
        d = manhattan(point1, point2)
        best = max(best, d)

print(best)
