from collections import defaultdict, Counter
from itertools import product, cycle

def new_pos(pos, step):
  pos += step
  return ((pos - 1) % 10 + 1)

# part 1

pos1, pos2 = 1, 6

die = cycle(list(range(1, 101)))

def throw():
  return next(die) + next(die) + next(die)

step = 0
pts1, pts2 = 0, 0
while pts2 < 1000:
  step += 3
  pos1 = new_pos(pos1, throw())
  pts1 += pos1
  pts1, pts2 = pts2, pts1
  pos1, pos2 = pos2, pos1
print(pts1 * step)

# part 2

pos1, pos2 = 1, 6

memo = defaultdict(int)
memo[0, 0, pos1, pos2] = 1

victories = [0, 0]
cur = 0
throw_combinations = Counter([sum(t) for t in list(product([1, 2, 3], repeat=3))])

while memo:
  new_memo = defaultdict(int)
  
  for pts_me, pts_him, pos_me, pos_him in memo:
    val = memo[pts_me, pts_him, pos_me, pos_him]
    if pts_him >= 21:
      victories[cur % 2] += val
      continue
    for t, c in throw_combinations.items():
      my_new_pos = new_pos(pos_me, t)
      new_memo[pts_him, pts_me + my_new_pos, pos_him, my_new_pos] += c * val
  memo = new_memo
  cur += 1

print(victories)
print(max(victories))
