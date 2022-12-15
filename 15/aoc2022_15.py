
import re
import numpy as np

def sensor_beacons(fname):
    with open(fname) as strm:
        for line in strm:
            m = re.fullmatch(r'Sensor at x=(.+), y=(.+): closest beacon is at x=(.+), y=(.+)\n',
                             line)
            yield np.reshape([int(x) for x in m.groups()], (2, 2))

def dist(a, b):
    return np.sum(np.abs(b - a))

def excludefromline(line, exclusion):
    # line is a sorted list of pairs of coordinates where every pair marks an
    # excluded segment. The start coordinate belongs to the segment, the end
    # coordinate does not.
    # exclusion is just a pair of coordinates marking a new segment to be excluded.
    # print(line, exclusion)
    before = [pair for pair in line if pair[1] < exclusion[0]]
    after = [pair for pair in line if pair[0] > exclusion[1]]
    during = [pair for pair in line if pair not in before and pair not in after]
    if not during:
        newpair = tuple(exclusion)
    else:
        newpair = (min(during[0][0], exclusion[0]), max(during[-1][1], exclusion[1]))
    return before + [newpair] + after

def count_excluded(fname, rownum):
    line = []
    beacons = set()
    for sensor, closest in sensor_beacons(fname):
        if closest[1] == rownum:
            beacons.add(tuple(closest))
        size = dist(sensor, closest) - abs(rownum - sensor[1])
        if size >= 0:
            line = excludefromline(line, (sensor[0] - size, sensor[0] + size + 1))
    return sum([b - a for a, b in line]) - len(beacons)

def transform(coord, maxcoord):
    # Transforms the line into a rotated coordinate system where the allowed
    # coordinates form a square with corners [0, +-maxcoord] and [+-maxcoord, 0].
    return np.array([[1, 1], [-1, 1]]) @ coord - [maxcoord, 0]

def untransform(coord, maxcoord):
    # The reverse transformation.
    return np.array([[1, -1], [1, 1]]) @ (np.array(coord) + [maxcoord, 0]) // 2

def edges(sensor, size):
    # Returns pairs of edges of the a sensor viewfield.
    last = [0, -size]
    for spoke in [[size, 0], [0, size], [-size, 0], last]:
        yield sensor + last, sensor + spoke
        last = spoke

def _find_freeedgepos(i, pos, edge, sensors, maxcoord):
    # Expects transformed coordinates.
    if edge[1] < edge[0]:
        # No edge in legal area, nothing to do.
        return None
    # Create a line having everything but the edge excluded.
    line = [(-np.inf, edge[0]), (edge[1] + 1, np.inf)]
    for sensor, size in sensors:
        # Calculate the minimal and maximal u/v coordinates for the viewfield of the sensor.
        # Add 1 to the maximum values in order to accomodate what excludefromline expects.
        square = np.sort([transform(sensor + x, maxcoord)
                          for x in [[size, 0], [-size, 0]]],
                         axis=0).T + [0, 1]
        if square[i][0] <= pos < square[i][1]:
            # The edge is inside the sensor's viewfield.
            line = excludefromline(line, square[1 - i])
        if len(line) == 1:
            # All of the edge is unavailable (the line is [(-inf, inf)]).
            return None
    # There should be two coordinates left, both of which untransform to the same value.
    sol = pos * np.ones(2)
    sol[1 - i] = line[0][-1]
    return untransform(sol, maxcoord)

def find_freeedgepos(edge, sensors, maxcoord):
    a, b = (transform(x, maxcoord) for x in edge)
    # a and b have one coordinate in common.
    for i in range(2):
        if a[i] == b[i]:
            # Determine the common coordinate and the limits of the edge coordinate.
            # Attention: The last value of edge is included in the edge!
            pos = a[i]
            edge = sorted([a[1 - i], b[1 - i]])
            # Remove parts of the edge exceeding the legal area.
            edge[0] = max(edge[0], abs(pos) - maxcoord)
            edge[1] = min(edge[1], maxcoord - abs(pos))
            return _find_freeedgepos(i, pos, edge, sensors, maxcoord)

def find_freepos(fname, maxcoord):
    sensors = [(s, dist(s, b)) for s, b in sensor_beacons(fname)]
    for sens, size in sensors:
        for e in edges(sens, size + 1):
            sol = find_freeedgepos(e, sensors, maxcoord)
            if sol is not None:
                return sol

def find_tuningfrequency(fname, maxcoord):
    coord = find_freepos(fname, maxcoord)
    return 4000000 * int(coord[0]) + int(coord[1])

if __name__ == '__main__':
    assert count_excluded('testinput', 10) == 26
    print(count_excluded('input', 2000000))

    assert find_tuningfrequency('testinput', 20) == 56000011
    print(find_tuningfrequency('input', 4000000))
