
def rps_score(opponent, myself):
    # Input should be integers: 0 for rock, 1 for paper, 2 for scissors.
    if opponent == myself:
        return myself + 4
    if opponent == (myself + 1) % 3:
        return myself + 1
    if opponent == (myself - 1) % 3:
        return myself + 7
    raise ValueError(f"Invalid rps choices: {opponent} vs {myself}")

def rps_realscore(opponent, result):
    # Input should be integers: 0 for rock, 1 for paper, 2 for scissors
    # and 0 for lose, 1 for draw, 2 for win.
    myself = (opponent + result - 1) % 3
    return 3 * result + myself + 1

key = {'A': 0, 'B': 1, 'C': 2,
       'X': 0, 'Y': 1, 'Z': 2}
def load_rps_strategy(fname):
    rounds = []
    with open(fname) as strm:
        for line in strm:
            op, me = line.strip().split(' ')
            rounds.append((key[op], key[me]))
    return rounds

def total_rps_score(strategy):
    return sum([rps_score(*rnd) for rnd in strategy])

def total_rps_realscore(strategy):
    return sum([rps_realscore(*rnd) for rnd in strategy])

if __name__ == '__main__':
    teststrat = load_rps_strategy('testinput')
    strat = load_rps_strategy('input')

    assert total_rps_score(teststrat) == 15
    print(total_rps_score(strat))

    assert total_rps_realscore(teststrat) == 12
    print(total_rps_realscore(strat))
