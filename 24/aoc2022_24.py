
import numpy as np

def load_blizzards(fname):
    with open(fname) as strm:
        line = strm.readline().strip('\n')
        width = len(line) - 2
        blizzards = {sym: np.zeros((0, width), dtype=bool)
                     for sym in ['>', '<', '^', 'v']}
        while line := strm.readline().strip('\n#'):
            if len(line) != width:
                break
            for sym in blizzards:
                blizzards[sym] = np.concatenate((blizzards[sym],
                                                 np.array(list(line), ndmin=2) == sym))
    return blizzards

def advance(blizzards):
    for sym, axis, shift in [('>', 1, 1), ('<', 1, -1), ('^', 0, -1), ('v', 0, 1)]:
        blizzards[sym] = np.roll(blizzards[sym], shift, axis)

def _find_path(blizzards, entrance=(0, 0), target=(-1, -1)):
    positions = np.zeros_like(blizzards['>'], dtype=bool)
    steps = 0
    while not positions[target]:
        steps += 1
        advance(blizzards)
        candidates = positions.copy()
        for shift in [-1, 1]:
            vert = np.roll(positions, shift, 0)
            vert[(shift - 1) // 2, :] = False
            hor = np.roll(positions, shift, 1)
            hor[:, (shift - 1) // 2] = False
            candidates |= vert | hor
        # We can always come in from the start field.
        candidates[entrance] = True
        positions = candidates & ~np.bitwise_or.reduce(list(blizzards.values()))
    # We need to take another step because the real target is one field outside the area.
    advance(blizzards)
    return steps + 1

def find_path(fname, returns=0):
    blizzards = load_blizzards(fname)
    steps = _find_path(blizzards)
    for i in range(returns):
        steps += _find_path(blizzards, (-1, -1), (0, 0))
        steps += _find_path(blizzards)
    return steps

if __name__ == '__main__':
    assert find_path('testinput') == 18
    print(find_path('input'))

    assert find_path('testinput', 1) == 54
    print(find_path('input', 1))
