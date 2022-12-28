
def load_elves(fname):
    elves = []
    with open(fname) as strm:
        for r, line in enumerate(strm):
            for c, x in enumerate(line.strip()):
                if x == '#':
                    elves.append((r, c))
    return elves

def draw(elves):
    print()
    rows, cols = zip(*elves)
    for r in range(min(rows), max(rows) + 1):
        line = ''.join(['#' if (r, c) in elves else '.'
                        for c in range(min(cols), max(cols) + 1)])
        print(line)

considerations = [[(-1, 0), (-1, -1), (-1, 1)],
                  [(1, 0), (1, -1), (1, 1)],
                  [(0, -1), (-1, -1), (1, -1)],
                  [(0, 1), (-1, 1), (1, 1)]]

def proposition(elf, elves, rnd):
    props = []
    for i in range(4):
        neighbors = [(elf[0] + cons[0], elf[1] + cons[1]) for cons in considerations[(i + rnd) % 4]]
        if not set(neighbors).intersection(elves):
            props.append(neighbors[0])
        if props and len(props) <= i:
            return props[0]
    return elf

def step(elves, rnd):
    props = []
    conflicts = set()
    for elf in elves:
        p = proposition(elf, elves, rnd)
        if p in props:
            conflicts.add(p)
        props.append(p)
    if props == elves:
        return False
    for i, p in enumerate(props):
        if p not in conflicts:
            elves[i] = p
    return True

def walk(elves, startrnd=0, numrnds=None):
    if numrnds is None:
        rnd = startrnd
        while step(elves, rnd):
            rnd += 1
        return rnd + 1
    else:
        for rnd in range(startrnd, startrnd + numrnds):
            step(elves, rnd)
        return rnd + 1

def score(elves):
    rows, cols = zip(*elves)
    area = (max(rows) - min(rows) + 1) * (max(cols) - min(cols) + 1)
    return area - len(elves)

if __name__ == '__main__':
    testelves = load_elves('testinput')
    elves = load_elves('input')

    walk(testelves, numrnds=10)
    assert score(testelves) == 110

    walk(elves, numrnds=10)
    print(score(elves))

    assert walk(testelves, startrnd=10) == 20
    print(walk(elves, startrnd=10))
