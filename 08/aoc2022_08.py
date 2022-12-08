
import numpy as np

def load_trees(fname):
    return np.genfromtxt(fname, dtype=int, delimiter=1)

def topvisible(trees):
    highest = -np.ones(trees[0].shape, dtype=int)
    vis = []
    for row in trees:
        vis.append(row > highest)
        highest = np.maximum(row, highest)
    return np.array(vis)

def vertvisible(trees):
    return topvisible(trees) | np.flip(topvisible(np.flip(trees, 0)), 0)

def visible(trees):
    return vertvisible(trees) | vertvisible(trees.T).T

def topview(trees):
    view = []
    key = -np.ones([10, trees.shape[1]], dtype=int)
    row_idx = np.indices(key.shape)[0]
    for row in trees:
        key += 1
        view.append(np.select(row == row_idx, key, -1))
        key[row_idx <= row] = 0
    return np.array(view)

def viewscore(trees):
    return (topview(trees)
            * np.flip(topview(np.flip(trees, 0)), 0)
            * topview(trees.T).T
            * np.flip(topview(np.flip(trees.T, 0)), 0).T)

if __name__ == '__main__':
    testtrees = load_trees('testinput')
    trees = load_trees('input')

    assert np.count_nonzero(visible(testtrees)) == 21
    print(np.count_nonzero(visible(trees)))

    assert viewscore(testtrees).max() == 8
    print(viewscore(trees).max())
