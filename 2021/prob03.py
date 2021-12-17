from collections import defaultdict

lines = open('data/prob03.dat').readlines()

def filter(values, cond):
    bit = 0
    tmp = values
    while len(tmp) > 1:
      new1, new0 = [], []
      for value in tmp:
        if value[bit] == '1':
          new1.append(value)
        else:
          new0.append(value)
      tmp = new1 if cond(len(new1) - len(new0)) else new0
      bit += 1

    return int(tmp[0], 2)

print(filter(lines, lambda x: x>=0) * filter(lines, lambda x: x<0))

counts = defaultdict(lambda:0)
for line in lines:
    for i, v in enumerate(reversed(line.strip())):
      counts[i] += 2 * int(v) - 1

g = 0
e = 0

for val, count in counts.items():
    if count > 0:
      g += 2 ** val
    else:
      e += 2 ** val

print(g * e)