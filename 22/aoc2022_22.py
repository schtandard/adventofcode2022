
import re
import numpy as np

legend = {' ': -1,
          '.': 0,
          '#': 1}
facings = [np.array(coords, dtype=int) for coords in [(0, 1), (1, 0), (0, -1), (-1, 0)]]

def load_notes(fname):
    territory = np.zeros((0, 0), dtype=int)
    with open(fname) as strm:
        while line := strm.readline().removesuffix('\n'):
            row = np.array([legend[c] for c in line], dtype=int, ndmin=2)
            mismatch = row.shape[1] - territory.shape[1]
            if mismatch < 0:
                row = np.concatenate((row, -np.ones((1, -mismatch), dtype=int)),
                                     axis=1)
            elif mismatch > 0:
                territory = np.concatenate((territory, -np.ones((territory.shape[0], mismatch),
                                                                dtype=int)),
                                           axis=1)
            territory = np.concatenate((territory, row), axis=0)
        path = re.split(r'([RL])', strm.readline().strip())
    for i in range(0, len(path), 2):
        path[i] = int(path[i])
    return territory, path

def get_nextpos_flat(territory, pos, fac):
    res = tuple((pos + facings[fac]) % territory.shape)
    while territory[res] == -1:
        res = tuple((res + facings[fac]) % territory.shape)
    return res, fac

def get_nextpos_testcube(territory, pos, fac):
    size = 4
    res = tuple(pos + facings[fac])
    try:
        if territory[res] != -1:
            return res, fac
    except IndexError:
        pass
    face = tuple(np.array(pos) // size)
    if face == (0, 2):
        if fac == 0:
            return (3 * size - 1 - pos[0], 15), 2
        if fac == 2:
            return (size, size + pos[0]), 1
        if fac == 3:
            return (size, 3 * size - 1 - pos[1]), 1
    if face == (1, 0):
        if fac == 1:
            return (3 * size - 1, 3 * size - 1 - pos[1]), 3
        if fac == 2:
            return (3 * size - 1, 5 * size - 1 - pos[0]), 3
        if fac == 3:
            return (0, 3 * size - 1 - pos[1]), 1
    if face == (1, 1):
        if fac == 1:
            return (4 * size - 1 - pos[1], 2 * size), 0
        if fac == 3:
            return (pos[1] - size, 2 * size), 0
    if face == (1, 2):
        if fac == 0:
            return (2 * size, 5 * size - 1 - pos[0]), 1
    if face == (2, 2):
        if fac == 1:
            return (2 * size - 1, 3 * size - 1 - pos[1]), 3
        if fac == 2:
            return (2 * size - 1, 4 * size - 1 - pos[0]), 3
    if face == (2, 3):
        if fac == 0:
            return (3 * size - 1 - pos[0], 3 * size - 1), 2
        if fac == 1:
            return (5 * size - 1 - pos[1], 0), 0
        if fac == 3:
            return (5 * size - 1 - pos[1], 3 * size), 2
    raise Exception(f"Could not find next pos: pos = {pos}, fac = {fac}")

def get_nextpos_cube(territory, pos, fac):
    size = 50
    res = tuple(pos + facings[fac])
    try:
        if territory[res] != -1:
            return res, fac
    except IndexError:
        pass
    face = tuple(np.array(pos) // size)
    if face == (0, 1):
        if fac == 2:
            return (3 * size - 1 - pos[1], 0), 0
        if fac == 3:
            return (pos[1] + 2 * size, 0), 0
    if face == (0, 2):
        if fac == 0:
            return (3 * size - 1 - pos[0], 2 * size - 1), 2
        if fac == 1:
            return (pos[1] - size, 2 * size - 1), 2
        if fac == 3:
            return (4 * size - 1, pos[1] - 2 * size), 3
    if face == (1, 1):
        if fac == 0:
            return (size - 1, pos[0] + size), 3
        if fac == 2:
            return (2 * size, pos[0] - size), 1
    if face == (2, 0):
        if fac == 2:
            return (3 * size - 1 - pos[0], size), 0
        if fac == 3:
            return (pos[1] + size, size), 0
    if face == (2, 1):
        if fac == 0:
            return (3 * size - 1 - pos[0], 3 * size - 1), 2
        if fac == 1:
            return (pos[1] + 2 * size, size - 1), 2
    if face == (3, 0):
        if fac == 0:
            return (3 * size - 1, pos[0] - 2 * size), 3
        if fac == 1:
            return (0, pos[1] + 2 * size), 1
        if fac == 2:
            return (0, pos[0] - 2 * size), 1
    raise Exception(f"Could not find next pos: pos = {pos}, fac = {fac}")

def walk(territory, pos, fac, nsteps, get_nextpos=get_nextpos_flat):
    for i in range(nsteps):
        nextpos, nextfac = get_nextpos(territory, pos, fac)
        if territory[nextpos]:
            # The way is blocked.
            break
        # The way is not blocked.
        pos = nextpos
        fac = nextfac
    return pos, fac

def walk_path(territory, path, get_nextpos=get_nextpos_flat):
    pos, _ = get_nextpos_flat(territory, (0, -1), 0)
    fac = 0
    for p in path:
        if isinstance(p, int):
            if pos == (199, 47):
                pass
            pos, fac = walk(territory, pos, fac, p, get_nextpos)
        else:
            fac = (fac + (1 if p == 'R' else -1)) % len(facings)
    return 1000 * (pos[0] + 1) + 4 * (pos[1] + 1) + fac

if __name__ == '__main__':
    testnotes = load_notes('testinput')
    notes = load_notes('input')

    assert walk_path(*testnotes) == 6032
    print(walk_path(*notes))

    assert walk_path(*testnotes, get_nextpos_testcube) == 5031
    print(walk_path(*notes, get_nextpos_cube))
