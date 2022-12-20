
import numpy as np

def load_cipher(fname, key=1):
    with open(fname) as strm:
        numbers = np.array([line.strip() for line in strm], dtype='int64') * key
    indices = np.arange(numbers.size)
    return numbers, indices

def mix_cipher(numbers, indices):
    for i, n in enumerate(numbers):
        old = indices[i]
        new = (old + n) % (numbers.size - 1)
        if old == new:
            continue
        if old < new:
            indices[(old < indices) & (indices <= new)] -= 1
        else:
            indices[(old > indices) & (indices >= new)] += 1
        indices[i] = new

def read_cipher(numbers, indices):
    numbers = numbers[np.argsort(indices)]
    idc = (np.where(numbers == 0)[0] + [1000, 2000, 3000]) % numbers.size
    return np.sum(numbers[idc])

def decrypt(fname, key=1, mixnum=1):
    cipher = load_cipher(fname, key)
    for i in range(mixnum):
        mix_cipher(*cipher)
    return read_cipher(*cipher)

if __name__ == '__main__':

    assert decrypt('testinput') == 3
    print(decrypt('input'))

    assert decrypt('testinput', 811589153, 10) == 1623178306
    print(decrypt('input', 811589153, 10))
