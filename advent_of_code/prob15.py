from datetime import datetime
from collections import deque

f = open('data/prob15.dat')

from collections import defaultdict
import heapq

inf = float('inf')

risks = []
for line in f.readlines():
    risks.append(list(map(int, list(line.strip()))))
C = len(risks[0])
R = len(risks)

memo = defaultdict(lambda: inf)
memo[0, 0] = 0
edge = deque([deque() for _ in range(10)])
edge[0].append((0, 0),)
# heapq.heappush(edge, (0, 0, 0))


dirs = list(zip([1, -1, 0, 0], [0, 0, 1, -1]))

def iter_dirs(x, y):
    for i, j in dirs:
        yield x + i, y + j

scale = 5
def get_risk(x, y):
    if 0 <= x < scale * C and 0 <= y < scale * R:
        return (risks[x % C][y % R] + x//C + y//R - 1) % 9 + 1
    return inf

t1 = datetime.now()

E = 0
edge_size = 1
while edge_size:
    while not edge[E % 10]:
        E += 1
    x, y = edge[E % 10].pop()
    edge_size -= 1
    v = memo[x, y]
    for i, j in iter_dirs(x, y):
        d = get_risk(i, j)
        if memo[i, j] > (v + d):
            memo[i, j] = v + d
            # print(edge, d)
            edge[(E + d) % 10].append((i, j),)
            edge_size += 1
            # heapq.heappush(edge, (memo[i, j], i, j))


print(memo[scale * C - 1, scale * R - 1])

t2 = datetime.now()

print(t2 - t1)






