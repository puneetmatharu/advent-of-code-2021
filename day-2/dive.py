from pathlib import Path
from typing import List, Tuple


DATAFILE_PATH = Path.cwd() / "data.dat"


def solve_pt1(commands: List[Tuple[str, int]]) -> int:
    (h_pos, v_pos) = (0, 0)
    for (command, size) in commands:
        if command == "forward":
            h_pos += size
        if command == "down":
            v_pos += size
        if command == "up":
            v_pos -= size
    return h_pos * v_pos


def solve_pt2(commands: List[Tuple[str, int]]) -> int:
    (aim, h_pos, v_pos) = (0, 0, 0)
    for (command, size) in commands:
        if command == "down":
            aim += size
        if command == "up":
            aim -= size
        if command == "forward":
            h_pos += size
            v_pos += (size * aim)
    return h_pos * v_pos


def load_commands() -> List[Tuple[str, int]]:
    commands = None
    with open(DATAFILE_PATH, "r") as f:
        commands = f.readlines()
    commands = list((s.split()[0], int(s.split()[1])) for s in commands)
    return commands


def main() -> int:
    commands = load_commands()
    print(f"Number of commands: {len(commands)}")
    print(f"Answer to Part 1: {solve_pt1(commands)}")
    print(f"Answer to Part 2: {solve_pt2(commands)}")


if __name__ == "__main__":
    main()
