with open('data/prob02.dat') as f:
    p, d, a = 0, 0, 0
    for line in f.readlines():
        dir, val = line. split(' ')
        val = int(val)
        if dir == 'down':
            a += val
        elif dir == 'up':
            a -= val
        else:
            p += val
            d += a * val
    print(d*p)
