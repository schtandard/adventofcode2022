
def parse_line(line):
    ranges = line.strip().split(',')
    return [tuple(int(x) for x in rng.split('-')) for rng in ranges]

def fully_contained(rngs):
    return ((rngs[0][0] <= rngs[1][0] and rngs[0][1] >= rngs[1][1])
            or (rngs[0][0] >= rngs[1][0] and rngs[0][1] <= rngs[1][1]))

def overlap(rngs):
    return rngs[0][0] <= rngs[1][1] and rngs[0][1] >= rngs[1][0]

def count_ranges(fname, condition):
    n = 0
    with open(fname) as strm:
        for line in strm:
            n += condition(parse_line(line))
    return n

def count_fully_contained(fname):
    return count_ranges(fname, fully_contained)

def count_overlap(fname):
    return count_ranges(fname, overlap)

if __name__ == '__main__':
    assert count_fully_contained('testinput') == 2
    print(count_fully_contained('input'))

    assert count_overlap('testinput') == 4
    print(count_overlap('input'))
