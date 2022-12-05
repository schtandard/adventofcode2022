
import re

def load_crates(strm):
    stacks = []
    for line in strm:
        if line[1] == '1':
            # stacks are over.
            assert strm.readline() == '\n'
            return stacks
        n = len(line) // 4
        for i in range(n - len(stacks)):
            stacks.append([])
        for i in range(n):
            crate = line[1 + 4 * i]
            if crate == ' ':
                continue
            stacks[i] = [crate] + stacks[i]
    raise ValueError("Invalid input file.")

def execute_instruction(line, stacks, multiple=False):
    m = re.fullmatch(r'move (\d+) from (\d+) to (\d+)\n', line)
    n, ogn, tgt = (int(x) for x in m.groups())
    ogn, tgt = ogn - 1, tgt - 1
    if multiple:
        stacks[tgt].extend(stacks[ogn][-n:])
        stacks[ogn] = stacks[ogn][:-n]
    else:
        for i in range(n):
            stacks[tgt].append(stacks[ogn].pop())

def rearrange(strm, stacks, multiple=False):
    for line in strm:
        execute_instruction(line, stacks, multiple)

def find_topcrates(fname, multiple=False):
    with open(fname) as strm:
        stacks =load_crates(strm)
        rearrange(strm, stacks, multiple)
    return ''.join([s[-1] for s in stacks])

if __name__ == '__main__':
    assert find_topcrates('testinput') == 'CMZ'
    print(find_topcrates('input'))

    assert find_topcrates('testinput', True) == 'MCD'
    print(find_topcrates('input', True))
