class SnailFish:
    def __init__(self, val=None, L=None, R=None, P=None):
        self.val = val
        self.L, self.R, self.P = L, R, P
        if L:
            self.L.P = self
        if R:
            self.R.P = self

    def magnitude(self):
        if self.__is_number(self):
            return self.val
        else:
            return 3 * self.L.magnitude() + 2 * self.R.magnitude()

    @staticmethod
    def __is_number(fish):
        return fish and fish.val is not None

    def can_explode(self):
        return SnailFish.__is_number(self.L) and SnailFish.__is_number(self.R)

    def explode(self, D=1):
        if D > 4 and self.can_explode():
            self.prv().val += self.L.val
            self.nxt().val += self.R.val
            self.val, self.L, self.R = 0, None, None
            return True
        if self.L and self.L.explode(D + 1):
            return True
        if self.R and self.R.explode(D + 1):
            return True
        return False

    def prv(self):
        if not self.P:
            return SnailFish(0)
        if self == self.P.L:
            return self.P.prv()
        c = self.P.L
        while c.R:
            c = c.R
        return c

    def nxt(self):
        if not self.P:
            return SnailFish(0)
        if self == self.P.R:
            return self.P.nxt()
        c = self.P.R
        while c.L:
            c = c.L
        return c

    def split(self):
        if self.val is not None and self.val > 9:
            self.L = SnailFish(self.val // 2, P=self)
            self.R = SnailFish((self.val + 1) // 2, P=self)
            self.val = None
            return True
        if self.val is None:
            if self.L.split():
                return True
            if self.R.split():
                return True
        return False

    def copy(self):
        L = self.L.copy() if self.L else self.L
        R = self.R.copy() if self.R else self.R
        return SnailFish(val=self.val, L=L, R=R, P=self.P)


def parse(input):
    i = 0

    def inner():
        nonlocal i
        if input[i] == ',' or input[i] == ']':
            i += 1
            return inner()

        if input[i].isdigit():
            output = 0
            while input[i].isdigit():
                output *= 10
                output += int(input[i])
                i+=1
            return SnailFish(output)

        if input[i] == '[':
            i += 1
            L = inner()
            R = inner()
            return SnailFish(L=L, R=R)

    return inner()


def add(A, B):
    s = SnailFish(L=A.copy(), R=B.copy())
    while s.explode() or s.split():
        pass
    return s


best = -float('inf')
numbers = [parse(line.strip()) for line in open('data/prob18.dat').readlines()]
for a in numbers:
    for b in numbers:
        if b == a:
            continue
        best = max(best, add(a, b).magnitude())
print(best)

