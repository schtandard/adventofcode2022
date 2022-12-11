
def load_startingitems(strm):
    items = strm.readline().strip().removeprefix("Starting items: ")
    return [int(x) for x in items.split(', ')]

def load_operation(strm):
    op = strm.readline().strip().removeprefix("Operation: new = ")
    def operation(old):
        new = eval(op)
        return new
    return operation

def load_test(strm):
    n = int(strm.readline().strip().removeprefix("Test: divisible by "))
    a = int(strm.readline().strip().removeprefix("If true: throw to monkey "))
    b = int(strm.readline().strip().removeprefix("If false: throw to monkey "))
    return n, lambda x: b if x % n else a

def load_monkeys(fname):
    monkeys = []
    operations = []
    tests = []
    mod = 1
    with open(fname) as strm:
        while strm.readline():
            # We just read the monkey number, which we don't need.
            monkeys.append(load_startingitems(strm))
            operations.append(load_operation(strm))
            n, test = load_test(strm)
            tests.append(test)
            mod *= n
            # There is an empty line between monkeys.
            strm.readline()
    return monkeys, operations, tests, mod

def monkeyturn(i, monkeys, operations, tests, inspections, mod=0):
    while monkeys[i]:
        itm = monkeys[i].pop(0)
        itm = operations[i](itm)
        if mod:
            itm %= mod
        else:
            itm //= 3
        monkeys[tests[i](itm)].append(itm)
        inspections[i] += 1

def monkeyround(monkeys, operations, tests, inspections, mod=0):
    for i in range(len(monkeys)):
        monkeyturn(i, monkeys, operations, tests, inspections, mod)

def find_monkeybusinesslevel(fname, rounds=20, relief=True):
    monkeys, operations, tests, mod = load_monkeys(fname)
    if relief:
        mod = 0
    inspections = [0] * len(monkeys)
    for i in range(rounds):
        monkeyround(monkeys, operations, tests, inspections, mod)
    topinspectors = sorted(inspections)[-2:]
    return topinspectors[0] * topinspectors[1]

if __name__ == '__main__':
    assert find_monkeybusinesslevel('testinput') == 10605
    print(find_monkeybusinesslevel('input'))

    assert find_monkeybusinesslevel('testinput', 10000, False) == 2713310158
    print(find_monkeybusinesslevel('input', 10000, False))
