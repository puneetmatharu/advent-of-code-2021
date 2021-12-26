from pathlib import Path
from typing import List
import numpy as np


EXAMPLE_DATA_PATH = Path.cwd() / "example-data.dat"
TEST_DATA_PATH = Path.cwd() / "test-data.dat"


class Grid:
    EMPTY = 0
    EAST_MOVING = 1
    SOUTH_MOVING = 2

    def __init__(self, initial_state: List[str]):
        self._state = self.parse_state(initial_state)
        self._size = self._state.shape
        self.grid_locked = False

    def parse_state(self, state: List[str]) -> np.ndarray:
        char_map = {
            ".": Grid.EMPTY,
            ">": Grid.EAST_MOVING,
            "v": Grid.SOUTH_MOVING,
        }
        state_as_ints_list = [[char_map[c] for c in line] for line in state]
        state = np.array(state_as_ints_list, dtype=int)
        return state

    def step(self) -> None:
        east_moving = (self._state == Grid.EAST_MOVING)
        south_moving = (self._state == Grid.SOUTH_MOVING)

        # If a cucumber is moving east and has an empty spot to move into
        east_moveable = east_moving.copy()
        east_moveable &= (np.roll(self._state, shift=-1, axis=1) == Grid.EMPTY)
        east_not_moveable = east_moving.copy() ^ east_moveable

        # First movement; handle east-facing cucumbers
        new_state = np.zeros(self._size, dtype=int)
        new_state[east_not_moveable] = self._state[east_not_moveable]
        new_state[np.roll(east_moveable, shift=1, axis=1)] = Grid.EAST_MOVING

        # Empty spot to move into
        south_moveable = south_moving.copy()
        south_moveable &= (np.roll(new_state, shift=-1, axis=0) == Grid.EMPTY)
        south_moveable &= (np.roll(self._state, shift=-1,
                           axis=0) != Grid.SOUTH_MOVING)
        south_not_moveable = south_moving.copy() ^ south_moveable

        # Second movement; handle south-facing cucumbers
        new_state[south_not_moveable] = self._state[south_not_moveable]
        new_state[np.roll(south_moveable, shift=1, axis=0)] = Grid.SOUTH_MOVING

        self._state = new_state

        n_cuc_moved = np.sum(east_moveable + south_moveable)
        if n_cuc_moved == 0:
            self.grid_locked = True
        return self.grid_locked

    @staticmethod
    def prettify_grid(grid: "Grid"):
        grid_str = str(grid).replace(", ", "")
        grid_str = grid_str.replace(" [", "").replace("[[", "")
        grid_str = grid_str.replace("]", "")
        grid_str = grid_str.replace("0", ".")
        grid_str = grid_str.replace("1", ">")
        grid_str = grid_str.replace("2", "v")
        return grid_str

    def __str__(self):
        return Grid.prettify_grid(self._state)

    def __repr__(self):
        return str(self._state)


def solve_pt1(state: List[str]) -> int:
    grid = Grid(state)
    print(grid)
    n_step_to_gridlock = 0
    while not grid.grid_locked:
        grid.step()
        n_step_to_gridlock += 1
    return n_step_to_gridlock


def solve_pt2(state: List[str]) -> int:
    pass


def load_state(fpath: str) -> List[str]:
    state = None
    with open(fpath, "r") as f:
        state = f.read().splitlines()
    return state


def main() -> int:
    example_state = load_state(EXAMPLE_DATA_PATH)
    (example_answer1, example_answer2) = (58, None)
    print(f"Number of entries in state: {len(example_state)}")
    answer1 = solve_pt1(example_state)
    answer2 = solve_pt2(example_state)
    print(f"Answer to Part 1: {answer1}")
    print(f"Answer to Part 2: {answer2}")
    assert answer1 == example_answer1
    assert answer2 == example_answer2

    have_test_data = True
    if have_test_data:
        test_state = load_state(TEST_DATA_PATH)
        answer1 = solve_pt1(test_state)
        answer2 = solve_pt2(test_state)
        print(f"Answer to Part 1: {answer1}")
        print(f"Answer to Part 2: {answer2}")


if __name__ == "__main__":
    main()
