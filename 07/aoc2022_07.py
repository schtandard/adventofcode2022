
import re

def get_currdir(filesys, loc):
    currdir = filesys
    for d in loc:
        currdir = currdir[d]
    return currdir

def parse_line(line, filesys, loc):
    if line.startswith('$'):
        parse_cmdline(line, filesys, loc)
    else:
        parse_lsline(line, filesys, loc)

def parse_cmdline(line, filesys, loc):
    lineparts = line.split(' ')
    cmd = lineparts[1]
    if cmd == 'cd':
        arg = lineparts[2]
        if arg == '..':
            loc.pop()
        elif arg == '/':
            while loc:
                loc.pop()
        else:
            loc.append(arg)
    elif cmd == 'ls':
        return
    else:
        raise ValueError(f"Invalid command line: '{line}'")

def parse_lsline(line, filesys, loc):
    info, name = line.split(' ')
    d = get_currdir(filesys, loc)
    if info == 'dir':
        d[name] = {}
    else:
        d[name] = int(info)

def parse_shell(strm):
    filesys = {}
    loc = []
    for line in strm:
        parse_line(line.strip(), filesys, loc)
    return filesys

def find_dir_sizes(currdir):
    subdirs = {'': 0}
    for name, obj in currdir.items():
        if isinstance(obj, dict):
            # obj is a directory dict.
            subsubdirs = find_dir_sizes(obj)
            subdirs[''] += subsubdirs['']
            for n, s in subsubdirs.items():
                subdirs[f'{name}/{n}'] = s
        else:
            # obj is a file size.
            subdirs[''] += obj
    return subdirs

def get_dir_sizes(fname):
    with open(fname) as strm:
        filesys = parse_shell(strm)
    return find_dir_sizes(filesys)

def find_small_dir_sum(sizes):
    res = 0
    for path, s in sizes.items():
        if s <= 100000:
            res += s
    return res

def find_deletion_size(sizes):
    target = sizes[''] - 40000000
    candidates = [s for s in sizes.values()
                  if s >= target]
    return min(candidates)

if __name__ == '__main__':
    testsizes = get_dir_sizes('testinput')
    sizes = get_dir_sizes('input')

    assert find_small_dir_sum(testsizes) == 95437
    print(find_small_dir_sum(sizes))

    assert find_deletion_size(testsizes) == 24933642
    print(find_deletion_size(sizes))
