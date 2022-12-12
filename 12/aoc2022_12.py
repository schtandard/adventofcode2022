
import numpy as np

def load_terrain(fname):
    terrain = np.genfromtxt(fname, dtype=str, delimiter=1)
    terrain = np.vectorize(ord)(terrain)
    start = next(zip(*np.where(terrain == ord('S'))))
    goal = next(zip(*np.where(terrain == ord('E'))))
    terrain[start] = ord('a')
    terrain[goal] = ord('z')
    return terrain, start, goal

def find_shortest_path(terrain, start, goal):
    pathlens = -np.ones_like(terrain)
    pathlens[start] = 0
    feelers = [np.array(start)]
    while pathlens[goal] == -1:
        pos = feelers.pop(0)
        for neighbor in [pos + [1, 0],
                         pos + [0, 1],
                         pos + [-1, 0],
                         pos + [0, -1]]:
            if np.any(neighbor < 0) or np.any(neighbor >= pathlens.shape):
                continue
            if pathlens[tuple(neighbor)] != -1:
                continue
            if terrain[tuple(neighbor)] > terrain[tuple(pos)] + 1:
                continue
            pathlens[tuple(neighbor)] = pathlens[tuple(pos)] + 1
            feelers.append(neighbor)
    return pathlens[goal]

def find_shortest_apath(terrain, _, goal):
    pathlens = -np.ones_like(terrain)
    pathlens[goal] = 0
    feelers = [np.array(goal)]
    while feelers:
        pos = feelers.pop(0)
        for neighbor in [pos + [1, 0],
                         pos + [0, 1],
                         pos + [-1, 0],
                         pos + [0, -1]]:
            if np.any(neighbor < 0) or np.any(neighbor >= pathlens.shape):
                continue
            if pathlens[tuple(neighbor)] != -1:
                continue
            if terrain[tuple(neighbor)] < terrain[tuple(pos)] - 1:
                continue
            if terrain[tuple(neighbor)] == ord('a'):
                return pathlens[tuple(pos)] + 1
            pathlens[tuple(neighbor)] = pathlens[tuple(pos)] + 1
            feelers.append(neighbor)

if __name__ == '__main__':
    testterrain = load_terrain('testinput')
    terrain = load_terrain('input')

    assert find_shortest_path(*testterrain) == 31
    print(find_shortest_path(*terrain))

    assert find_shortest_apath(*testterrain) == 29
    print(find_shortest_apath(*terrain))
