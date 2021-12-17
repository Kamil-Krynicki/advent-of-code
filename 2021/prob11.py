from itertools import product
from collections import deque, defaultdict

with open('data/prob11.dat') as f:
    lines = f.readlines()
    D = len(lines)

    field = defaultdict(lambda: -float('inf'))
    for i, j in product(range(D), range(D)):
        field[i, j] = int(lines[i][j])

    def step():
        flashable = deque()
        for i, j in product(range(D), range(D)):
            field[i, j] += 1
            if field[i, j] > 9:
                flashable.append((i, j))
        return flashable

    def flash(flashable):
        flashed = set()
        while flashable:
            i, j = flashable.pop()
            if field[i, j] <= 9:
                continue
            for r, c in product([i + 1, i, i - 1], [j + 1, j, j - 1]):
                flashable.append((r, c))
                field[r, c] += 1
            flashed.add((i, j))
            del field[i, j]
        for i, j in flashed:
            field[i, j] = 0
        return len(flashed)

    flashes = 0
    step_no = 0
    cur_flashes = 0
    while cur_flashes < D * D:
        step_no += 1
        flash_these = step()
        cur_flashes = flash(flash_these)
        flashes += cur_flashes
    print("all flashed at", step_no)
    print(flashes)
