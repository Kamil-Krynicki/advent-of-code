def val(p1, p2, p3, w, z):
  x = int(((z % 26) + p2) != w)
  z //= p1
  z *= 25 * x + 1
  z += (w + p3) * x
  return z


f = open('data/prob24.dat')
lines = f.readlines()
p1, p2, p3 = (
    [int(x.split()[-1]) for x in lines[4::18]],
    [int(x.split()[-1]) for x in lines[5::18]],
    [int(x.split()[-1]) for x in lines[15::18]])

max_i = 14
def step(i, z):
  if i >= max_i:
    return '' if z == 0 else None
  if p1[i] == 26:
    w = (z % 26) + p2[i]
    if 1 <= w <= 9:
      new_z = val(p1[i], p2[i], p3[i], w, z)
      result = step(i + 1, new_z)
      if result is not None:
        return str(w) + result
    return None
  for w in reversed(range(1, 10)):
    new_z = val(p1[i], p2[i], p3[i], w, z)
    result = step(i + 1, new_z)
    if result is not None:
      return str(w) + result
print(step(0, 0))
