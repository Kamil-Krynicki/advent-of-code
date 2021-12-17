import heapq
from collections import deque
from functools import reduce


def basin_size(space, i, j):
    visited = set()
    queue = deque()
    queue.append((i, j))

    while queue:
        x, y = queue.popleft()
        if (x, y) not in visited and space[x][y] < '9':
            visited.add((x, y))
            queue.append((x + 1, y))
            queue.append((x - 1, y))
            queue.append((x, y + 1))
            queue.append((x, y - 1))

    return len(visited)


with open('data/prob09.dat') as f:
    inf = 'Z'
    lines = f.readlines()
    lines = [list(inf * 300)] + [ list((inf + line.strip() + inf)) for line in lines] + [list(inf * 300)]

    low_points = []
    for i in range(len(lines)):
        for j in range(1, len(lines[i]) - 1):
            if lines[i][j - 1] > lines[i][j] < lines[i][j + 1] and lines[i - 1][j] > lines[i][j] < lines[i + 1][j]:
                low_points.append((i, j))

    basins = [basin_size(lines, *point) for point in low_points]

    ans = reduce(lambda x,y:x*y, heapq.nlargest(3, basins))
    print(ans)


