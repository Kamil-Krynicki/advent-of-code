import re
f = open('data/prob17.dat')
x_min, x_max, y_min, y_max = map(int, re.search('target area: x=(.*)\\.\\.(.*), y=(.*)\\.\\.(.*)', f.read()).group(1, 2, 3, 4))

inf = float('inf')
def in_target(p):
    return x_min <= p[0] <= x_max and y_min <= p[1] <= y_max

def has_missed(p):
    return p[0] > x_max or p[1] < y_min

def trajetory(x, y, vx, vy):
    while not has_missed((x, y)):
        yield x, y
        x = x + vx
        vx = max(0, vx - 1)
        y = y + vy
        vy = vy - 1

def max_Y(T):
    return max(map(lambda p:p[1], T))

def hits(T):
    return any(map(in_target, T))

best = -inf
scored_hit = True
total = 0
vy = min(y_min, y_max)
while scored_hit:
    scored_hit = vy < max(abs(y_min), abs(y_max))
    for vx in range(x_max + 1):
        T = list(trajetory(0, 0, vx, vy))
        if hits(T):
            scored_hit = True
            total += 1
            best = max(best, max_Y(T))
    vy += 1

print(best, total)