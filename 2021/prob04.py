class Board:
  N = 5
  def __init__(self, pos):
    self.vals = {}
    self.marked_cols = [0] * Board.N
    self.marked_rows = [0] * Board.N
    self.marked = []

    for i in range(Board.N):
      tmp = pos[i].strip().split()
      self.vals.update({int(tmp[j]) : (i, j) for j in range(Board.N)})

  def is_done(self):
    return any(map(lambda x:x==Board.N, self.marked_rows + self.marked_cols))

  def mark(self, val):
    if val in self.vals:
      i, j = self.vals[val]
      self.marked_rows[i] += 1
      self.marked_cols[j] += 1
      self.marked.append(val)

lines = open('data/prob04.dat').readlines()

nums = list(map(int, lines[0].split(',')))
boards = set()
i = 2
while i < len(lines):
    boards.add(Board(lines[i:i+5]))
    i += 6

for num in nums:
    for board in set(boards):
      board.mark(num)
      if board.is_done():
        if len(boards) == 1:
          print(num * (sum(board.vals.keys()) - sum(board.marked)))
        boards.remove(board)
