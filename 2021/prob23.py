from collections import defaultdict
import heapq

def manhatan(A, B):
  return abs(A[1] - B[1]) + abs(A[0] - B[0])

costs = {'A': 1, 'B': 10, 'C': 100, 'D': 1000}
room_points = {'A':3, 'B':5, 'C':7, 'D':9}
upper_points = [1, 2, 4, 6, 8, 10, 11]

class State:
  def __init__(self, points, cost = 0):
    self.cost = cost
    self.points = points

  def move(self, old_point, new_point):
    new_points = dict(self.points)
    t = new_points[old_point]
    del new_points[old_point]
    new_points[new_point] = t
    return State(new_points, self.cost + costs[t] * manhatan(old_point, new_point))

  def __lt__(self, other):
    return self.cost < other.cost

  def __hash__(self):
    return hash(frozenset(self.points.items()))

  def __eq__(self, other):
    return other.points == self.points

  def is_done(self):
    for t, c in room_points.items():
      if (2, c) not in self.points or not self.points[2, c] == t:
        return False
    return True

  def next_states(self):
    ans = []
    for P in self.points:
      t = self.points[P]
      if P[0] == 1:
        r, c = self.lowest_free(room_points[t], t)
        if r > 1:
          if self.can_reach(P[1], c):
            return [self.move(P, (r, c))]
      elif P[0] > 1:
        if  (P[0] - 1, P[1]) not in self.points:
          r, _ = self.lowest_free(P[1], t)
          if r == -1:
            for c in self.all_reachable(P[1]):
              ans.append(self.move(P, (1, c)))
    return ans
  
  def lowest_free(self, c, t):
    if not room_points[t] == c:
      return -1, c
    for r in range(5, 1, -1):
      if (r, c) not in self.points:
        return r, c
      if not self.points[r, c] == t:
        return -1, c
    return 1, c
  
  def all_reachable(self, C):
    ans = set()
    for c in upper_points:
      if c > C:
        if (1, c) not in self.points:
          ans.add(c)
        else:
          break
    for c in reversed(upper_points):
      if c < C:
        if (1, c) not in self.points:
          ans.add(c)
        else:
          break
    return ans

  def can_reach(self, c1, c2):
    for c in range(min(c1 + 1, c2), max(c2 + 1, c1)):
      if (1, c) in self.points:
        return False
    return True

f = open('data/prob23.dat')
lines = f.readlines()

space = list(list(line.replace(' ', '#')) for line in lines)
start_position = {}
for r, line in enumerate(space):
  for c, t in enumerate(line):
    if t not in {'.', '#'}:
      start_position[r, c] = t

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
