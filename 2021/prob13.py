with open('data/prob13.dat') as f:
    space = set()
    folds = []
    for l in f:
        if ',' in l:
            space.add(tuple(map(int, l.strip().split(','))))
        if '=' in l:
            folds.append(tuple(l.strip().split()[2].split('=')))

    def x_fold(edge):
        for x, y in set(space):
            if x > edge:
                space.remove((x, y))
                space.add((2 * edge - x, y))

    def y_fold(edge):
        for x, y in set(space):
            if y > edge:
                space.remove((x, y))
                space.add((x, 2 * edge - y))


    def print_space():
        xs = [x for x, y in space]
        ys = [y for x, y in space]
        for i in range(min(ys), max(ys) + 1):
            print('')
            for j in range(min(xs), max(xs) + 1):
                print('#' if (j, i) in space else '.', end = '')

    fold = {'x':x_fold, 'y':y_fold}
    for type, edge in folds:
        fold[type](int(edge))
    print_space()