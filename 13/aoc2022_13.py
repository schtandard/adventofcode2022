
class Packet(list):
    def __init__(self, iterable=()):
        super().__init__()
        for x in iterable:
            if isinstance(x, list):
                self.append(type(self)(x))
            else:
                self.append(x)

    def __lt__(self, x):
        if isinstance(x, int):
            return self.__lt__(type(self)([x]))
        return super().__lt__(x)

    def __gt__(self, x):
        if isinstance(x, int):
            return self.__gt__(type(self)([x]))
        return super().__gt__(x)

    def __eq__(self, x):
        if isinstance(x, int):
            return self.__eq__(type(self)([x]))
        return super().__eq__(x)

def load_pairs(fname):
    pairs = []
    with open(fname) as strm:
        while True:
            pairs.append(tuple(Packet(eval(strm.readline().strip()))
                               for i in range(2)))
            # There are blank lines separating pairs.
            if not strm.readline():
                break
    return pairs

def find_correctindexsum(pairs):
    res = 0
    for i, (left, right) in enumerate(pairs, 1):
        if left < right:
            res += i
    return res

def find_decoderkey(pairs):
    dividers = [Packet([[2]]), Packet([[6]])]
    packets = sorted([p for pair in pairs for p in pair] + dividers)
    res = 1
    for d in dividers:
        res *= packets.index(d) + 1
    return res

if __name__ == '__main__':
    testpairs = load_pairs('testinput')
    pairs = load_pairs('input')

    assert find_correctindexsum(testpairs) == 13
    print(find_correctindexsum(pairs))

    assert find_decoderkey(testpairs) == 140
    print(find_decoderkey(pairs))
