import re

class Box:
  def __init__(self, boundaries):
    self.D = len(boundaries) // 2
    self.mins = boundaries[::2]
    self.maxs = boundaries[1::2]

  def size(self):
    ans = 1
    for i in range(self.D):
      ans *= self.maxs[i] - self.mins[i] + 1
    return ans

  def intersects(self, other):
    for i in range(self.D):
      if self.maxs[i] < other.mins[i] or self.mins[i] > other.maxs[i]:
        return False
    return True

  def split(self, other):
    def inner(bounds, d):
      if d == self.D:
        yield Box(bounds)
      else:
        for S, E in zip((min(self.mins[d], other.mins[d]), max(self.mins[d], other.mins[d]), other.maxs[d] + 1),
                        (other.mins[d] - 1, min(self.maxs[d], other.maxs[d]), max(self.maxs[d], other.maxs[d]))):
          if S <= E:
            yield from inner(bounds + [S, E], d + 1)
    yield from inner([], 0)

f = open('data/prob22.dat')
out = []
for line in f.readlines():
  p = re.search('(.*) x=([\\-0-9]+)..([\\-0-9]+)\\,y=([\\-0-9]+)..([\\-0-9]+)\\,z=([\\-0-9]+)..([\\-0-9]+)', line.strip())
  if p:
    p = p.groups()
    out.append((p[0] == 'on', Box(list(map(int, p[1:]))), ))

def small_reboot(out):
    reactor = set()
    def set_cube(state, box):
      for x in range(max(-50, box.mins[0]), 1+ min(50, box.maxs[0])):
        for y in range(max(-50, box.mins[1]), 1+ min(50, box.maxs[1])):
          for z in range(max(-50, box.mins[2]), 1+ min(50, box.maxs[2])):
            if state:
              reactor.add((x, y, z),)
            elif (x, y, z) in reactor:
              reactor.remove((x, y, z),)
    for on, box in out:
      set_cube(on, box)
    print(len(reactor))

def full_reboot(out):
  boxes = []
  for state, new_box in out:
      for box in boxes:
        if new_box.intersects(box):
          boxes.remove(box)
          for box_fragment in box.split(new_box):
            if not box_fragment.intersects(new_box):
              boxes.append(box_fragment)
      if state:
          boxes.append(new_box)
  print(sum(box.size() for box in boxes))

small_reboot(out)
full_reboot(out)
