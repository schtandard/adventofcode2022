
import numpy as np

directions = {'R': (1, 0),
              'U': (0, 1),
              'L': (-1, 0),
              'D': (0, -1)}

def step_rope(rope, heading):
    rope[0] += directions[heading]
    for i in range(1, len(rope)):
        if np.all(np.abs(rope[i - 1] - rope[i]) < 2):
            continue
        rope[i] += np.sign(rope[i - 1] - rope[i])

def count_tailpos(fname, ropelen=2):
    rope = np.zeros((ropelen, 2))
    tailpositions = set()
    with open(fname) as strm:
        for line in strm:
            heading, steps = line.strip().split(' ')
            for i in range(int(steps)):
                step_rope(rope, heading)
                tailpositions.add(tuple(rope[-1]))
    return len(tailpositions)

if __name__ == '__main__':
    assert count_tailpos('testinput') == 13
    print(count_tailpos('input'))

    assert count_tailpos('testinput', 10) == 1
    assert count_tailpos('testinput2', 10) == 36
    print(count_tailpos('input', 10))
