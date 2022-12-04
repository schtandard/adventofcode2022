
def load_inventory(fname):
    inventory = [0]
    with open(fname) as strm:
        if not fname:
            return []
        for line in strm:
            if line == '\n':
                inventory.append(0)
            else:
                inventory[-1] += int(line.strip())
    return inventory

if __name__ == '__main__':
    testinv = sorted(load_inventory('testinput'))
    inv = sorted(load_inventory('input'))


    assert testinv[-1] == 24000
    print(inv[-1])

    assert(sum(testinv[-3:])) == 45000
    print(sum(inv[-3:]))
