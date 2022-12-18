
import numpy as np

def _draw(pic, jet, rows, sep='    '):
    pixels = {0: jet, 1: '#', 2: '@'}
    lines = [''.join([pixels[x] for x in row]) for row in pic]
    merged = [sep.join([lines[j] for j in range(i, len(lines), rows)])
              for i in range(rows)]
    print('\n'.join(merged))

def draw(state, rock=None, pos=None, jet=0, rows=7):
    print()
    jet = {0: '.', 1: '>', -1: '<'}[jet]
    if rock is not None:
        state, staterock = _put(state, rock, pos)
        state = state.astype(int)
        state[staterock] = 2
    _draw(state, jet, rows)

def jetstreams(fname):
    steps = {'>': 1,
             '<': -1}
    with open(fname) as strm:
        line = strm.readline().strip()
    yield len(line)
    while True:
        for x in line:
            yield steps[x]

def rocks():
    a = np.ones((1, 4), dtype=bool)
    b = np.array([[0, 1, 0],
                  [1, 1, 1],
                  [0, 1, 0]], dtype=bool)
    c = np.array([[0, 0, 1],
                  [0, 0, 1],
                  [1, 1, 1]], dtype=bool)
    d = np.ones((4, 1), dtype=bool)
    e = np.ones((2, 2), dtype=bool)
    while True:
        yield a
        yield b
        yield c
        yield d
        yield e

def collides(state, rock, pos):
    if pos[0] < -state.shape[0]:
        raise ValueError("It seems like you chose a too small cave height.")
    if pos[1] < 0:
        return True
    if pos[1] > state.shape[1] - rock.shape[1]:
        return True
    if pos[0] >= 0:
        return False
    row = -pos[0] - rock.shape[0]
    if row < 0:
        return np.any(rock[pos[0]:] & state[:-pos[0], pos[1]:pos[1] + rock.shape[1]])
    else:
        return np.any(rock & state[row:row+rock.shape[0], pos[1]:pos[1]+rock.shape[1]])


def _put(state, rock, pos):
    row = -pos[0] - rock.shape[0]
    if row < 0:
        state = np.roll(state, -row, 0)
        state[:-row] = False
        row = 0
    staterock = np.zeros_like(state)
    staterock[row:row+rock.shape[0], pos[1]:pos[1]+rock.shape[1]] = rock
    return state, staterock

def put(state, rock, pos):
    if pos[0] > 0:
        raise ValueError("This doesn't seem right.")
    state, staterock = _put(state, rock, pos)
    state[staterock] = True
    return state


def droprock(state, rock, jets, startheight=3):
    # Positions are (y, x) where y is the position above the state (i.e. 0 means
    # right on top of the state, -1 means in the first row of the state) and x is
    # the column position (i.e. 0 means at the left edge of the cave).
    pos = np.array([startheight, 2])
    # draw(state, rock, pos)
    # input()
    for numjets, jet in enumerate(jets, 1):
        nextpos = pos + [0, jet]
        if not collides(state, rock, nextpos):
            pos = nextpos
        # draw(state, rock, pos, jet)
        # input()
        nextpos = pos + [-1, 0]
        if collides(state, rock, nextpos):
            break
        pos = nextpos
        # draw(state, rock, pos)
        # input()
    state = put(state, rock, pos)
    gain = max(0, pos[0] + rock.shape[0])
    return state, int(gain), numjets

def _droprocks(state, rcks, jets, n, maxheight=100):
    gain = 0
    numjets = 0
    for i in range(n):
        state, g, nj = droprock(state, next(rcks), jets)
        gain += g
        numjets += nj
    return state, gain, numjets

def droprocks(fname, n=2022, caveheight=42):
    state = np.zeros((caveheight, 7), dtype=bool)
    state[0] = True
    jets = jetstreams(fname)
    jetperiod = next(jets)
    jetidx = 0
    rcks = rocks()
    height = 0
    known_states = []
    looplen = None
    while n > 5 and looplen is None:
        n -= 5
        state, gain, nj = _droprocks(state, rcks, jets, 5)
        height += gain
        jetidx = (jetidx + nj) % jetperiod
        for known_n, known_height, known_jetidx, known_state in known_states:
            if jetidx == known_jetidx and np.array_equal(state, known_state):
                # We've reached a stable loop.
                looplen = known_n - n
                height += n // looplen * (height - known_height)
                n %= looplen
                break
        known_states.append((n, height, jetidx, state.copy()))
    state, gain, _ = _droprocks(state, rcks, jets, n)
    return height + gain

if __name__ == '__main__':
    assert droprocks('testinput') == 3068
    print(droprocks('input'))

    assert droprocks('testinput', 1000000000000) == 1514285714288
    print(droprocks('input', 1000000000000))
