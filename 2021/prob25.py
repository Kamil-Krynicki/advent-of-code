  f = open('data/prob25.dat')
  lines = f.readlines()
  pos = {}
  C, R = len(lines[0].strip()), len(lines)
  for r, line in enumerate(lines):
    for c, val in enumerate(line.strip()):
      if not val == '.':
        pos[r, c] = val

  def step(pos):
    new_pos = {}
    moved = False
    for r, c in pos:
      if pos[r, c] == '>' and (r, (c + 1) % C) not in pos:
        new_pos[r, (c + 1) % C] = '>'
        moved = True
      else:
        new_pos[r, c] = pos[r, c]
    pos, new_pos = new_pos, {}
    for r, c in pos:
      if pos[r, c] == 'v' and ((r + 1) % R, c) not in pos:
        new_pos[(r + 1) % R, c] = 'v'
        moved = True
      else:
        new_pos[r, c] = pos[r, c]
    return new_pos, moved

  i, moved = 0, True
  while moved:
    i += 1
    pos, moved = step(pos)
  print(i)
