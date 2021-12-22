from pathlib import Path
from typing import List
from itertools import product
import numpy as np


EXAMPLE_DATA_PATH = Path.cwd() / "example-data.dat"
TEST_DATA_PATH = Path.cwd() / "test-data.dat"


class OctopusGrid:
    def __init__(self, grid: List[List[int]], nrow: int, ncol: int):
        self.grid = np.array(grid)
        self.gridsize = (nrow, ncol)
        assert self.grid.shape == self.gridsize
        self.nflash = self._count_flashes()
        self.nround = 0

    def nflash(self) -> int:
        return self.nflash

    def synchronised(self) -> bool:
        return np.sum(self.grid == 0) == (self.gridsize[0] * self.gridsize[1])

    def _count_flashes(self) -> int:
        return np.sum(self.grid > 9)

    def step(self) -> None:
        self.grid += 1

        are_new_flashes = True
        all_highlighted = np.zeros(self.gridsize, dtype=bool)
        new_flashes = np.zeros(self.gridsize, dtype=bool)
        while are_new_flashes:
            # Find new flashes
            new_flashes = (all_highlighted ^ (self.grid > 9))
            all_highlighted = (self.grid > 9)

            # Update the neighbours of new flashes
            (flash_i, flash_j) = np.where(new_flashes)
            for (fi, fj) in zip(flash_i, flash_j):
                self._update_neighbours(fi, fj)

            # If there are no new flashes, we're done
            if np.sum(all_highlighted ^ (self.grid > 9)) == 0:
                are_new_flashes = False

        # Count number of flashes in this round and zero out flashing octopuses
        self.nflash += np.sum(self.grid > 9)
        self.grid[self.grid > 9] = 0

        # Move onto the next round
        self.nround += 1

    def _valid_ij(self, i: int, j: int) -> bool:
        (nrow, ncol) = self.gridsize
        return (i >= 0) & (i < nrow) & (j >= 0) & (j < ncol)

    def _update_neighbours(self, i: int, j: int) -> None:
        for (di, dj) in product((-1, 0, 1), (-1, 0, 1)):
            if ((di, dj) != (0, 0)) and self._valid_ij(i + di, j + dj):
                self.grid[i + di, j + dj] += 1


def solve_pt1(data: List[str]) -> int:
    ogrid = OctopusGrid(data, nrow=10, ncol=10)
    for i in range(100):
        ogrid.step()
    return ogrid.nflash


def solve_pt2(data: List[str]) -> int:
    ogrid = OctopusGrid(data, nrow=10, ncol=10)
    while not ogrid.synchronised():
        ogrid.step()
    return ogrid.nround


def load_data(fpath: str) -> List[List[int]]:
    data = None
    with open(fpath, "r") as f:
        data = f.read().splitlines()
    grid = [list(map(int, list(row))) for row in data]
    return grid


def main():
    example_data = load_data(EXAMPLE_DATA_PATH)
    (example_answer1, example_answer2) = (1656, 195)
    print(f"Number of entries in data: {len(example_data)}")
    print(f"Answer to Part 1: {solve_pt1(example_data)}")
    print(f"Answer to Part 2: {solve_pt2(example_data)}")
    assert solve_pt1(example_data) == example_answer1
    assert solve_pt2(example_data) == example_answer2

    test_data = load_data(TEST_DATA_PATH)
    print(f"Number of entries in data: {len(test_data)}")
    print(f"Answer to Part 1: {solve_pt1(test_data)}")
    print(f"Answer to Part 2: {solve_pt2(test_data)}")


if __name__ == "__main__":
    main()
