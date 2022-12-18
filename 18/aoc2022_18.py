
import numpy as np

def load_droplet(fname):
    # Returns the droplet as a boolean array with a padding of width 1 at all sides.
    pixels = []
    maxidx = np.zeros(3, int)
    with open(fname) as strm:
        for line in strm:
            pixels.append(np.array(line.strip().split(','), dtype=int))
            maxidx = np.maximum(maxidx, pixels[-1])
    droplet = np.zeros(maxidx + 3, dtype=bool)
    for pix in pixels:
        droplet[tuple(pix + 1)] = True
    return droplet

def surface(droplet):
    faces = 0
    for dim in range(len(droplet.shape)):
        faces += np.sum(np.roll(droplet, 1, dim) ^ droplet)
    return faces

def filled(droplet):
    # We will need the inverted droplet, so we invert it once here.
    droplet = ~droplet
    # Initialize the known outside with fields on the edge of the droplet, which is empty padding.
    outside = np.min(np.indices(droplet.shape), 0) == 0
    size = 0
    while size < (size := np.count_nonzero(outside)):
        for dim in range(len(droplet.shape)):
            for s in [-1, 1]:
                outside |= np.roll(outside, s, dim) & droplet
    return ~outside

if __name__ == '__main__':
    testdrop = load_droplet('testinput')
    drop = load_droplet('input')

    assert surface(testdrop) == 64
    print(surface(drop))

    testdrop = filled(testdrop)
    drop = filled(drop)

    assert surface(testdrop) == 58
    print(surface(drop))
