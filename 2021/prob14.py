from collections import OrderedDict, defaultdict

f = open('data/prob14.dat')

lines = f.readlines()
start = lines[0].strip()
rules = {k: v for k, v in map(lambda x:x.strip().split(' -> '), lines[2:])}

pairs = defaultdict(int)

for i in range(len(start) - 1):
    L, R = start[i], start[i + 1]
    pairs[L+R] += 1

def grow(pairs):
    new_pairs = defaultdict(int)
    for L, R in pairs:
        M = rules[L + R]
        new_pairs[L + M] += pairs[L + R]
        new_pairs[M + R] += pairs[L + R]
    return new_pairs

for i in range(40):
    pairs = grow(pairs)

counts = defaultdict(lambda:0)
for L, R in pairs:
    counts[L] += pairs[L + R]
counts[start[-1]] += 1

most_common = max(counts.items(), key=lambda x: x[1])
least_common = min(counts.items(), key=lambda x: x[1])
print((most_common[1] - least_common[1]))
