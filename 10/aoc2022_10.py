
def Xregister(fname):
    X = 1
    with open(fname) as strm:
        for line in strm:
            yield X
            if line == 'noop\n':
                continue
            yield X
            X += int(line.strip().split(' ')[1])

def find_signalstrengthsum(fname):
    strength = 0
    for i, X in enumerate(Xregister(fname), 1):
        if i % 40 == 20:
            strength += i * X
    return strength

def draw_screen(fname):
    line = ''
    for i, X in enumerate(Xregister(fname)):
        pos = i % 40
        line += '#' if abs(X - pos) < 2 else '.'
        if pos == 39:
            print(line)
            line = ''

if __name__ == '__main__':
    assert find_signalstrengthsum('testinput') == 13140
    print(find_signalstrengthsum('input'))

    # draw_screen('testinput')
    draw_screen('input')
