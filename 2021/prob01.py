
with open('data/prob01.dat') as f:
    result = 0
    prv = float('inf')
    for line in f.readlines():
        cur = int(line)
        if cur > prv:
            result += 1
        prv = cur
    print(result)


with open('data/prob01.dat') as f:
    result = 0
    a, b, c = float('inf'),float('inf'),float('inf')
    for line in f.readlines():
        cur = int(line)
        if cur > a:
            result += 1
        a, b, c = b, c, cur
    print(result)