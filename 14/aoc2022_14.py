
def add_line(occupied, a, b):
    if a[0] == b[0]:
        for y in range(min(a[1], b[1]), max(a[1], b[1]) + 1):
            occupied.add((a[0], y))
    elif a[1] == b[1]:
        for x in range(min(a[0], b[0]), max(a[0], b[0]) + 1):
            occupied.add((x, a[1]))
    else:
        raise ValueError("Lines must be horizontal or vertical!")

def load_cave(fname):
    occupied = set()
    with open(fname) as strm:
        for line in strm:
            points = [[int(x) for x in pair.split(',')]
                       for pair in line.strip().split(' -> ')]
            for i in range(len(points) - 1):
                add_line(occupied, points[i], points[i + 1])
    return occupied

def count_sand(fname, entrance=(500, 0), floored=False):
    occupied = load_cave(fname)
    maxy = max(y for x, y in occupied)
    n = 0
    while entrance not in occupied:
        sand = entrance
        while sand[1] <= maxy:
            if (nxt := (sand[0], sand[1] + 1)) in occupied:
                if (nxt := (sand[0] - 1, sand[1] + 1)) in occupied:
                    if (nxt := (sand[0] + 1, sand[1] + 1)) in occupied:
                        break
            sand = nxt
        if not floored and sand[1] > maxy:
            break
        occupied.add(sand)
        n += 1
    return n

if __name__ == '__main__':
    assert count_sand('testinput') == 24
    print(count_sand('input'))

    assert count_sand('testinput', floored=True) == 93
    print(count_sand('input', floored=True))
