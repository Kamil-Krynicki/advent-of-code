from collections import defaultdict, namedtuple

point = namedtuple('Point', ['x', 'y'])

f = open('data/problem5.dat')

class Line:
    def __init__(self, rep):
        rep = rep.split(' -> ')
        self.s = point(*list(map(int, rep[0].split(','))))
        self.e = point(*list(map(int, rep[1].split(','))))

    def points(self):
        d_x = self.__delta(self.s.x, self.e.x)
        d_y = self.__delta(self.s.y, self.e.y)

        c_x, c_y = self.s.x, self.s.y
        yield c_x, c_y
        while c_x != self.e.x or c_y != self.e.y:
            c_x += d_x
            c_y += d_y
            yield c_x, c_y

    def __delta(self, s, e):
        return 1 if e > s else -1 if e < s else 0

lines = []
for l in f:
    lines.append(Line(l))

N = 1000

field = defaultdict(int)

for line in lines:
    for x, y in line.points():
        field[y, x] += 1

print(len(list(filter(lambda x:x>1, field.values()))))
#
#
# for line in lines:
#     if line.is_diagonal():
#         for x, y in line.points():
#             field[y, x] += 1
#
# print(len(list(filter(lambda x:x>1, field.values()))))
#
