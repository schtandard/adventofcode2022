
def find_startindex(signal, marklen=4):
    seq = [None] * marklen
    n = 0
    for c in signal:
        n += 1
        seq[n % marklen] = c
        if None in seq:
            continue
        if len(set(seq)) == marklen:
            return n

def startindex(fname, marklen=4):
    idx = []
    with open(fname) as strm:
        for line in strm:
            idx.append(find_startindex(line.strip(), marklen=marklen))
    if len(idx) == 0:
        return None
    if len(idx) == 1:
        return idx[0]
    return idx

if __name__ == '__main__':
    assert startindex('testinput') == [7, 5, 6, 10, 11]
    print(startindex('input'))

    assert startindex('testinput', marklen=14) == [19, 23, 23, 29, 26]
    print(startindex('input', marklen=14))
