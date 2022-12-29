
dec_digits = {'2': 2, '1': 1, '0': 0, '-': -1, '=': -2}
snafu_digits = {v: k for k, v in dec_digits.items()}

def snafu2dec(snafu):
    if not snafu:
        return 0
    return 5 * snafu2dec(snafu[:-1]) + dec_digits[snafu[-1]]

def dec2snafu(dec):
    if not dec:
        return ''
    rem = dec % 5
    if rem > 2:
        rem -= 5
    return dec2snafu((dec - rem) // 5) + snafu_digits[rem]

def fuel_sum(fname):
    fuel = 0
    with open(fname) as strm:
        for line in strm:
            fuel += snafu2dec(line.strip())
    return dec2snafu(fuel)

if __name__ == '__main__':
    assert fuel_sum('testinput') == '2=-1=0'
    print(fuel_sum('input'))
