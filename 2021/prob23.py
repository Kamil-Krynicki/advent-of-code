from collections import defaultdict
import heapq

def manhatan(A, B):
  return abs(A[1] - B[1]) + abs(A[0] - B[0])

costs = [1, 10, 100, 1000]
room_points = [3, 5, 7, 9]
upper_points = [1, 2, 4, 6, 8, 10, 11]

class State:
  def __init__(self, points, cost = 0, limits = (5, 5, 5, 5)):
    self.cost = cost
    self.points = points
    self.limits = limits

  def move(self, t, old_point, new_point):
    new_points = dict(self.points)
    del new_points[old_point]
    if new_point[0] > 1:
      new_limits = list(self.limits)
      new_limits[t] -= 1
      new_limits = tuple(new_limits)
    else:
      new_points[new_point] = t
      new_limits = self.limits
    return State(new_points, self.cost + costs[t] * manhatan(old_point, new_point), new_limits)

  def __lt__(self, other):
    return self.cost < other.cost

  def __hash__(self):
    return hash(frozenset(self.points.items())) * hash(self.limits)

  def __eq__(self, other):
    return other.points == self.points

  def is_done(self):
    return not self.points

  def next_states(self):
    for P, t in self.points.items():
      if P[0] == 1:
        r, c = self.limits[t], room_points[t]
        if (r, c) not in self.points:
          if self.can_reach(P[1], c):
            return [self.move(t, P, (r, c))]
    ans = []
    for P, t in self.points.items():
      if P[0] > 1:
        if (P[0] - 1, P[1]) not in self.points:
          for c in self.all_reachable(P[1]):
            ans.append(self.move(t, P, (1, c)))
    return ans

  def all_reachable(self, C):
    for c in upper_points:
      if c > C:
        if (1, c) not in self.points:
          yield c
        else:
          break
    for c in reversed(upper_points):
      if c < C:
        if (1, c) not in self.points:
          yield c
        else:
          break

  def can_reach(self, c1, c2):
    c1, c2 = min(c1 + 1, c2), max(c1, c2 + 1)
    for r, c in self.points:
      if r == 1 and c1 < c < c2:
        return False
    return True

f = open('data/prob23.dat')
lines = f.readlines()

space = list(list(line.replace(' ', '#')) for line in lines)
start_position = {}
for r, line in enumerate(space):
  for c, t in enumerate(line):
    if t not in {'.', '#'}:
      start_position[r, c] = ord(t) - ord('A')

s = State(start_position)
best = defaultdict(lambda:float('inf'))
best[s] = 0

states = [s]
while states:
  cur_state = heapq.heappop(states)
  if cur_state.is_done():
    print("found!", cur_state.cost)
    break
  for new_state in cur_state.next_states():
    if best[new_state] > new_state.cost:
      best[new_state] = new_state.cost
      heapq.heappush(states, new_state)
