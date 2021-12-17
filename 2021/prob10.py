from collections import deque
from statistics import median

with open('data/prob10.dat') as f:
    points1 = {')': 3, ']': 57, '}': 1197, '>': 25137}
    points2 = {'(': 1,'[': 2,'{': 3,'<': 4}

    def match(L, R):
        return L + R in ['()', '[]', '{}', '<>']

    illegal = []
    pts_list = []
    for line in f.readlines():
        pending = deque()

        for c in line.strip():
            if c in points2.keys():
                pending.append(c)
            elif not match(pending.pop(), c):
                illegal.append(c)
                pending.clear()
                break

        if pending:
            pts_list.append(sum(map(lambda i: points2[pending[i]] * 5**i, range(len(pending)))))

    print(median(pts_list))
    print(sum(points1[i] for i in illegal))