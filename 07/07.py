import dataclasses
from time import perf_counter_ns as timestamp_nano
from functools import cached_property


@dataclasses.dataclass
class AbstractFile:
    name: str
    parent: 'Dir'


@dataclasses.dataclass
class File(AbstractFile):
    size: int


@dataclasses.dataclass
class Dir(AbstractFile):
    children: list = dataclasses.field(default_factory=list)

    @cached_property
    def size(self) -> int:
        return sum(child.size for child in self)

    def __iter__(self):
        return iter(self.children)


def file_system(data: str) -> Dir:
    root = Dir('/', None)
    cwd = root

    lines = data.splitlines()
    n_lines = len(lines)
    # first line is '$ cd /' so skip that
    i = 1
    while i < n_lines:
        match lines[i].split(' '):
            case ['$', 'cd', target]:
                if target == '/':
                    cwd = root
                elif target == '..':
                    cwd = cwd.parent
                else:
                    for child in cwd:
                        if child.name == target:
                            cwd = child
                            # we only cd to known dirs
                            break
                i += 1
            case ['$', 'ls']:
                i += 1
                while i < n_lines and not lines[i].startswith('$ '):
                    match lines[i].split(' '):
                        case ['dir', name]:
                            cwd.children.append(Dir(name, cwd))
                        case [size, name]:
                            cwd.children.append(File(name, cwd, int(size)))
                    i += 1
    
    return root


def part1(root: Dir, max_size: int) -> int:
    def rec_size(cwd):
        if isinstance(cwd, Dir):
            size = 0
            if (s := cwd.size) <= max_size:
                size += s
            for child in cwd:
                size += rec_size(child)

            return size
        return 0

    return rec_size(root)


def part2(root: Dir, disk_space_total: int, disk_space_min: int) -> int:
    to_free = disk_space_min - (disk_space_total - root.size)

    def gen_sizes(cwd: Dir | File):
        if isinstance(cwd, Dir):
            yield cwd.size
            for child in cwd:
                yield from gen_sizes(child)

    return min(s for s in gen_sizes(root) if s >= to_free)


if __name__ == '__main__':
    start = timestamp_nano()

    with open('07/input.txt') as in_file:
        data = in_file.read()

    tree = file_system(data)
    print(f'part1: {part1(tree, int(100e3))}')
    print(f'part2: {part2(tree, int(70e6), int(30e6))}')

    end = timestamp_nano()
    print(f'time: {(end - start) / 1000:.3f}µs')
