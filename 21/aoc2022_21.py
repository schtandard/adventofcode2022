
import sympy

def load_monkeys(fname):
    with open(fname) as strm:
        return dict(line.strip().split(': ') for line in strm)

def _dress(monkeys):
    for m, job in monkeys.items():
        jobparts = job.split(' ')
        if len(jobparts) == 3:
            job = f"res['{jobparts[0]}'] {jobparts[1]} res['{jobparts[2]}']"
        monkeys[m] = job

def _solve(monkeys):
    res = {m: None for m in monkeys}
    while res['root'] is None:
        for m, job in monkeys.items():
            try:
                res[m] = eval(job)
            except TypeError:
                continue
    return res

def solve_root(fname):
    monkeys = load_monkeys(fname)
    _dress(monkeys)
    return int(_solve(monkeys)['root'])

def _fix_monkeys(monkeys):
    first, _, second = monkeys['root'].split(' ')
    monkeys['root'] = f'{first} - {second}'
    monkeys['humn'] = "sympy.symbols('x')"

def solve_humn(fname):
    monkeys = load_monkeys(fname)
    _dress(monkeys)
    _fix_monkeys(monkeys)
    sltn = _solve(monkeys)
    print(sltn['root'])
    return sympy.solve(sltn['root'], sltn['humn'])[0]

if __name__ == '__main__':
    assert solve_root('testinput') == 152
    print(solve_root('input'))

    assert solve_humn('testinput') == 301
    print(solve_humn('input'))
