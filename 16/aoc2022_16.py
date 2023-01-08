
import re
import numpy as np

def load_volcano(fname):
    valves = {}
    tunnels = {}
    with open(fname) as strm:
        for line in strm:
            m = re.fullmatch(r"Valve ([A-Z]{2}) has flow rate=(\d+); tunnels? leads? to valves? (.+)\n",
                             line)
            valves[m[1]] = int(m[2])
            tunnels[m[1]] = m[3].split(', ')
    return valves, tunnels

def simplify_volcano(valves, tunnels):
    n = len(valves)
    outputs = np.zeros(n, dtype=int)
    connections = np.zeros((n, n), dtype=bool)
    # Temporarily remove AA in order to force it to have index 0.
    valves.pop('AA')
    idcs = {k: i for i, k in enumerate(valves.keys(), 1)}
    idcs['AA'] = 0
    valves['AA'] = 0
    # Make arrays containing all the information
    for valve, idx in idcs.items():
        outputs[idx] = valves[valve]
        for other in tunnels[valve]:
            connections[idx, idcs[other]] = True
    # Calculate the distance between any two valves.
    distances = np.zeros((n, n), dtype=int)
    for i in range(n):
        reached = np.zeros(n, dtype=bool)
        reached[i] = True
        d = 0
        while not np.all(reached):
            d += 1
            nextreached = np.any(connections[reached, :], axis=0) | reached
            distances[i][nextreached & ~reached] = d
            reached = nextreached
    # Throw away useless valves.
    useful = outputs > 0
    useful[0] = True
    outputs = outputs[useful]
    distances = distances[np.ix_(useful, useful)]
    # Add 1 to each distance to account for the step necessary to open the valve.
    distances += 1
    return outputs, distances

def _find_max_output(outputs, distances, pos, time, closed):
    if not closed or max(time) == 0:
        return 0
    agent = np.argmax(time)
    outp = []
    for i in range(len(closed)):
        nextpos = pos.copy()
        nextpos[agent] = closed[i]
        nexttime = time.copy()
        nexttime[agent] -= distances[pos[agent], nextpos[agent]]
        if nexttime[agent] < 1:
            continue
        outp.append(outputs[nextpos[agent]] * nexttime[agent]
                    + _find_max_output(outputs, distances,
                                       nextpos, nexttime,
                                       closed[:i] + closed[i+1:]))
    # Maybe this agent just doesn't do anything anymore.
    # If we omit this case, the runtime almost halves (from 34 min to 19 min),
    # but I believe that it is necessary in general.
    nexttime = time.copy()
    nexttime[agent] = 0
    outp.append(_find_max_output(outputs, distances,
                                 pos, nexttime, closed))
    return max(outp, default=0)

def find_max_output(outputs, distances, time=30, agents=1):
    return _find_max_output(outputs, distances,
                            [0] * agents, [time] * agents,
                            tuple(range(1, len(outputs))))

def solve(fname, time=30, agents=1):
    outputs, distances = simplify_volcano(*load_volcano(fname))
    return find_max_output(outputs, distances, time, agents)

if __name__ == '__main__':
    assert solve('testinput') == 1651
    print(solve('input'))

    assert solve('testinput', 26, 2) == 1707
    print(solve('input', 26, 2))
