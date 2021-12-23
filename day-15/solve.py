from pathlib import Path
from typing import List
import numpy as np


EXAMPLE_DATA_PATH = Path.cwd() / "example-data.dat"
TEST_DATA_PATH = Path.cwd() / "test-data.dat"

STORED_RISKS = None
SIZE = None


def risk(cavern: np.ndarray) -> int:
    (n_row, n_col) = cavern.shape
    stored_risks = -1 * np.ones((n_row, n_col), dtype=int)
    stored_risks[0, 0] = 0

    for i in range(n_row):
        for j in range(n_col):
            if (i == 0) and (j == 0):
                continue
            risks = []
            if i > 0:
                risks.append(stored_risks[i - 1, j])
            if j > 0:
                risks.append(stored_risks[i, j - 1])
            stored_risks[i, j] = min(risks) + cavern[i, j]

    n_sweep = 2
    for _ in range(n_sweep):
        for i in range(n_row):
            for j in range(n_col):
                if (i == 0) and (j == 0):
                    continue
                risks = []
                if i > 0:
                    risks.append(stored_risks[i - 1, j])
                if j > 0:
                    risks.append(stored_risks[i, j - 1])
                if i < n_row - 1:
                    risks.append(stored_risks[i + 1, j])
                if j < n_col - 1:
                    risks.append(stored_risks[i, j + 1])
                stored_risks[i, j] = min(risks) + cavern[i, j]

    current_risk = stored_risks[-1, -1]
    return current_risk


def solve_pt1(cavern: np.ndarray) -> int:
    lowest_risk = risk(cavern)
    return lowest_risk


def solve_pt2(cavern: np.ndarray) -> int:
    def mod_b1(x: np.ndarray, b: int) -> np.ndarray:
        return ((x - 1) % b) + 1

    def get_tile_slices(i_tile: int, j_tile: int) -> List[slice]:
        (offset_i, offset_j) = (i_tile * n_row, j_tile * n_col)
        (slice_x, slice_y) = (slice(offset_i + 0, offset_i + n_row),
                              slice(offset_j + 0, offset_j + n_col))
        return slice_x, slice_y

    (n_row, n_col) = cavern.shape
    n_tiles = (5, 5)
    tiled_cavern = np.tile(cavern, n_tiles)
    for i_tile in range(n_tiles[0]):
        for j_tile in range(n_tiles[1]):
            (slice_x, slice_y) = get_tile_slices(i_tile, j_tile)
            tiled_cavern[slice_x, slice_y] = mod_b1(
                tiled_cavern[slice_x, slice_y] + i_tile + j_tile, b=9)
    lowest_risk = risk(tiled_cavern)
    return lowest_risk


def load_cavern(fpath: str) -> np.ndarray:
    cavern = None
    with open(fpath, "r") as f:
        cavern = f.read().splitlines()
    cavern = np.array([list(map(int, line)) for line in cavern])
    return cavern


def main() -> int:
    example_cavern = load_cavern(EXAMPLE_DATA_PATH)
    (example_answer1, example_answer2) = (40, 315)
    print(f"Number of entries in cavern: {len(example_cavern)}")
    answer1 = solve_pt1(example_cavern)
    answer2 = solve_pt2(example_cavern)
    print(f"Answer to Part 1: {answer1}")
    print(f"Answer to Part 2: {answer2}")
    assert answer1 == example_answer1
    assert answer2 == example_answer2

    have_test_data = True
    if have_test_data:
        test_cavern = load_cavern(TEST_DATA_PATH)
        answer1 = solve_pt1(test_cavern)
        answer2 = solve_pt2(test_cavern)
        print(f"Answer to Part 1: {answer1}")
        print(f"Answer to Part 2: {answer2}")


if __name__ == "__main__":
    main()
