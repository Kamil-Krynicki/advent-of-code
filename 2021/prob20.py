from itertools import product

f = open('data/prob20.dat')
decode = f.readline()
f.readline()

image = set()
for i, line in enumerate(f.readlines()):
    for j, c in enumerate(line.strip()):
        if c == '#':
            image.add((i, j),)

def process_image(image, background):
    x_max, x_min, y_max, y_min = edges(image)

    def is_lit(x, y):
        if x > x_max or x < x_min or y > y_max or y < y_min:
            return background == '#'
        else:
            return (x, y) in image

    def read_pixels(x, y):
        ans = 0
        for dx, dy in product([-1, 0, 1], repeat=2):
            ans *= 2
            if is_lit(x + dx, y + dy):
                ans += 1
        return ans

    new_image = set()
    for i in range(x_min - 1, x_max + 2):
        for j in range(y_min - 1, y_max + 2):
            if decode[read_pixels(i, j)] == '#':
                new_image.add((i, j), )

    return new_image


def edges(image):
    x_min = min(map(lambda x: x[0], image))
    x_max = max(map(lambda x: x[0], image))
    y_min = min(map(lambda x: x[1], image))
    y_max = max(map(lambda x: x[1], image))
    return x_max, x_min, y_max, y_min

N = 50
B = '.'
for _ in range(N):
    image = process_image(image, B)
    B = decode[-1] if B == '#' else decode[0]

print(len(image))
