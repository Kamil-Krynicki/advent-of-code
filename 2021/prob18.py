from itertools import product


class SnailFish:
    def __init__(self, val=-1, L=None, R=None, P=None):
        self.val = val
        self.L, self.R, self.P = L, R, P
        if L:
            self.L.P = self
        if R:
            self.R.P = self

    def magnitude(self):
        if self.val < 0:
            return 3 * self.L.magnitude() + 2 * self.R.magnitude()
        else:
            return self.val

    def explode(self, D=1):
        if self.__is_number():
            return False
        if D > 4 and self.L.__is_number() and self.R.__is_number():
            self.__prv().val += self.L.val
            self.__nxt().val += self.R.val
            self.val, self.L, self.R = 0, None, None
            return True
        return self.L.explode(D + 1) or self.R.explode(D + 1)

    def __is_number(self):
        return self.L is None and self.R is None

    def __prv(self):
        if not self.P:
            return SnailFish(0)
        if self == self.P.L:
            return self.P.__prv()
        cur = self.P.L
        while cur.R:
            cur = cur.R
        return cur

    def __nxt(self):
        if not self.P:
            return SnailFish(0)
        if self == self.P.R:
            return self.P.__nxt()
        cur = self.P.R
        while cur.L:
            cur = cur.L
        return cur

    def split(self):
        if self.val > 9:
            self.L = SnailFish(self.val // 2, P=self)
            self.R = SnailFish((self.val + 1) // 2, P=self)
            self.val = -1
            return True
        if self.val >= 0:
            return False
        return self.L.split() or self.R.split()

    def add(self, other):
        ans = SnailFish(L=self.copy(), R=other.copy())
        while ans.explode() or ans.split():
            pass
        return ans

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

best = -float('inf')
numbers = [parse(line.strip()) for line in open('data/prob18.dat').readlines()]
for a, b in product(numbers, repeat=2):
    best = max(best, a.add(b).magnitude())
print(best)
