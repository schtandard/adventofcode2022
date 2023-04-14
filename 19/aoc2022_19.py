
import numpy as np
import re

def load_blueprints(fname):
    with open(fname) as strm:
        return np.array([load_blueprint(line.strip()) for line in strm], dtype=int)

def load_blueprint(line):
    line = line.split(': ')[1]
    return [load_costs(phrase.strip(' .')) for phrase in line.split('. ')]

def load_costs(phrase):
    phrase = phrase.split('costs ')[1]
    m = re.fullmatch(r'(\d+) ore(?: and (\d+) clay)?(?: and (\d+) obsidian)?', phrase)
    return [int(x) if x is not None else 0
            for x in m.groups()] + [0]

def _wait_and_make_robot(rob, blueprint, resources, robots):
    costs = blueprint[rob]
    materials = costs > 0
    time = np.ceil(np.max((costs - resources)[materials] / robots[materials]))
    time = max(int(time), 0) + 1
    resources = resources + time * robots - costs
    robots = robots.copy()
    robots[rob] += 1
    return time, resources, robots

def _rob_options(blueprint, robots):
    options = [3, 2, 1, 0]
    for i in [1, 2, 3]:
        if not robots[i - 1]:
            options.remove(i)
    for i in [0, 1, 2]:
        if robots[i] >= max(blueprint[:,i]):
            options.remove(i)
    return options

def _find_max_geodes(blueprint, resources, robots, time, nextrob, currmin):
    if resources[3] + robots[3] * time + time * (time - 1) / 2 <= currmin:
        # Even producing a geode robot every minute we cannot surpass currmin.
        return currmin
    t, rsrcs, rbts = _wait_and_make_robot(nextrob, blueprint, resources, robots)
    if t > time:
        return resources[3] + robots[3] * time
    time -= t
    resources = rsrcs
    robots = rbts
    for rob in _rob_options(blueprint, robots):
        currmin = max(currmin, _find_max_geodes(blueprint, resources, robots, time, rob, currmin))
    return currmin

def find_max_geodes(blueprint, time=24):
    currmin = 0
    resources = np.zeros(4, dtype=int)
    robots = np.array([1, 0, 0, 0])
    for rob in _rob_options(blueprint, robots):
        currmin = max(currmin, _find_max_geodes(blueprint, resources, robots, time, rob, currmin))
    return currmin

def find_quality_level_sum(blueprints, time=24):
    score = 0
    for i, b in enumerate(blueprints, 1):
        score += i * find_max_geodes(b, time)
    return score

def find_max_geode_product(blueprints, time=32):
    score = 1
    for b in blueprints:
        score *= find_max_geodes(b, time)
    return score

if __name__ == '__main__':
    test_bps = load_blueprints('testinput')
    bps = load_blueprints('input')

    assert find_quality_level_sum(test_bps) == 33
    print(find_quality_level_sum(bps))

    bps = bps[:3]

    assert find_max_geode_product(test_bps) == 3472
    print(find_max_geode_product(bps))
