from __future__ import annotations

import dataclasses
from functools import cached_property
from time import perf_counter_ns as timestamp_nano


@dataclasses.dataclass(slots=True, repr=False, eq=False)
class AbstractFile:
    name: str
    parent: Dir

    @property
    def is_dir(self) -> bool:
        return False


@dataclasses.dataclass(slots=True, repr=False, eq=False)
class File(AbstractFile):
    size: int


@dataclasses.dataclass(repr=False, eq=False)
class Dir(AbstractFile):
    children: dict[str, Dir | File] = dataclasses.field(default_factory=dict)

    # our file-system will not change, so we can cache sizes
    @cached_property
    def size(self) -> int:
        return sum(child.size for child in self)

    @property
    def is_dir(self) -> bool:
        return True

    def __iter__(self) -> iter[AbstractFile]:
        return iter(self.children.values())


def file_system(path: str) -> Dir:
    root = Dir('/', None)
    cwd = root

    with open(path) as in_file:
        try:
            # first line is '$ cd /' so skip that
            next(in_file)
            lines = (line.removesuffix('\n') for line in in_file)

            line = next(lines)
            # read until EOF
            while True:
                match line.split(' '):
                    case ['$', 'cd', '/']:
                        cwd = root
                        line = next(lines)
                    case ['$', 'cd', '..']:
                        cwd = cwd.parent
                        line = next(lines)
                    case ['$', 'cd', target]:
                        # assumption: We're only cd-ing to known targets
                        cwd = cwd.children[target]
                        line = next(lines)
                    case ['$', 'ls']:
                        # read until there's a new command or EOF
                        while (line := next(lines)):
                            match line.split(' '):
                                case ['dir', name]:
                                    cwd.children[name] = Dir(name, cwd)
                                case [size, name]:
                                    cwd.children[name] = File(name, cwd, int(size))
                                case ['$', *_]:
                                    break
        except StopIteration:
            return root


def part1(root: Dir, max_size: int) -> int:
    def rec_size(cwd):
        if cwd.is_dir:
            if (s := cwd.size) <= max_size:
                yield s
            for child in cwd:
                yield from rec_size(child)

    return sum(rec_size(root))


def part2(root: Dir, disk_space_total: int, free_space_min: int) -> int:
    def find_min(cwd: Dir | File):
        nonlocal optim
        if cwd.is_dir:
            if to_free <= cwd.size < optim:
                optim = cwd.size
            for child in cwd:
                find_min(child)
        return optim

    to_free = free_space_min - (disk_space_total - (optim := root.size))
    return find_min(root)


if __name__ == '__main__':
    start = timestamp_nano()

    tree = file_system('07/input.txt')
    print(f'part1: {part1(tree, max_size=int(100e3))}')
    print(f'part2: {part2(tree, disk_space_total=int(70e6), free_space_min=int(30e6))}')

    end = timestamp_nano()
    print(f'time: {(end - start) / 1000:.3f}µs')
