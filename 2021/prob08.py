lines = open('data/prob08.dat').readlines()

ans = 0
for line in lines:
    train, real = line.split('|')

    models = [set()] * 10
    for digit in train.split():
        L = len(digit)
        model = set(digit)
        if L == 2:
            models[1] = model
        if L == 3:
            models[7] = model
        if L == 4:
            models[4] = model
        if L == 7:
            models[8] = model

    # now we have models fro 1, 4, 7, 8
    for digit in train.split():
        L = len(digit)
        model = set(digit)
        if L == 6:
            if models[4].issubset(model):
                models[9] = model
            elif models[7].issubset(model):
                models[0] = model
            else:
                models[6] = model

    # now we have models for 0, 1, 4, 6, 7, 8, 9
    for digit in train.split():
        L = len(digit)
        model = set(digit)
        if L == 5:
            if models[1].issubset(model):
                models[3] = model
            elif model.issubset(models[6]):
                models[5] = model
            else:
                models[2] = model

    inverse_models = {''.join(sorted(e)): str(i) for i, e in enumerate(models)}

    ans += int(''.join(map(lambda v: inverse_models[''.join(sorted(v))], real.split())))

print(ans)