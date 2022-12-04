
def get_priority(itemtype):
    n = ord(itemtype)
    if 65 <= n <= 90:
        # Uppercase letter.
        return n - 38
    if 97 <= n <= 122:
        # Lowercase letter.
        return n - 96
    raise ValueError(f"Non-letter item type: {itemtype}")

def get_common_item(*compartments):
    candidates = set.intersection(*[set(comp) for comp in compartments])
    if len(candidates) == 1:
        return candidates.pop()
    raise ValueError(f"Found the following common items: {candidates}")

def load_prioritysum(fname):
    prio = 0
    with open(fname) as strm:
        for line in strm:
            line = line.strip()
            compartments = (line[:len(line) // 2], line[len(line) // 2:])
            prio += get_priority(get_common_item(*compartments))
    return prio

def load_badgesum(fname):
    prio = 0
    with open(fname) as strm:
        rucksacks = []
        for line in strm:
            rucksacks.append(line.strip())
            if len(rucksacks) == 3:
                prio += get_priority(get_common_item(*rucksacks))
                rucksacks = []
    return prio

if __name__ == '__main__':
    assert load_prioritysum('testinput') == 157
    print(load_prioritysum('input'))

    assert load_badgesum('testinput') == 70
    print(load_badgesum('input'))
