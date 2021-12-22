from pathlib import Path
from typing import List
from itertools import product
import numpy as np


EXAMPLE_DATA_PATH = Path.cwd() / "example-data.dat"
TEST_DATA_PATH = Path.cwd() / "test-data.dat"


class HeightMap:
    def __init__(self, grid: List[List[int]]):
        self.grid = np.array(grid)
        self.size = self.grid.shape

    def _low_points(self) -> np.ndarray:
        int32_max = np.iinfo(np.int32).max
        temp_grid = np.pad(self.grid, 1, constant_values=int32_max)
        low_points = np.ones(temp_grid.shape, dtype=bool)

        for (di, dj) in ((0, -1), (0, 1), (-1, 0), (1, 0)):
            low_points &= temp_grid < np.roll(
                temp_grid, (di, dj), axis=(0, 1))

        # Strip padding
        return low_points[1:-1, 1:-1]

    def risk_level(self) -> int:
        is_low_point = self._low_points()
        return np.sum(self.grid[is_low_point] + 1)

    def get_largest_basin_size(self) -> int:
        max_basin_size = 0
        low_points = self._low_points()
        zero_mask = np.zeros(low_points.shape, dtype=bool)

        n_low_point = np.sum(self._low_points())
        basin_sizes = np.zeros((n_low_point,))

        (lp_i, lp_j) = np.where(low_points)
        for (index, (i, j)) in enumerate(zip(lp_i, lp_j)):
            low_point_mask = zero_mask.copy()
            low_point_mask[i, j] = True
            basin_sizes[index] = self._get_basin_size(low_point_mask)
        basin_sizes = np.sort(basin_sizes)[-3:]

        return int(basin_sizes[0] * basin_sizes[1] * basin_sizes[2])

    def _valid_ij(self, i: int, j: int) -> bool:
        return (i >= 0) & (i < self.size[0]) & (j >= 0) & (j < self.size[1])

    def _get_basin_size(self, basin_mask: np.ndarray) -> int:
        new_points = basin_mask
        previously_found = (basin_mask * 0).astype(bool)
        while np.sum(new_points) > 0:
            new_points = basin_mask ^ previously_found
            previously_found = basin_mask.copy()
            if np.sum(basin_mask) == (self.size[0] * self.size[1]):
                break

            (lp_i, lp_j) = np.where(new_points)

            for (i, j) in zip(lp_i, lp_j):
                for (di, dj) in ((0, -1), (0, 1), (-1, 0), (1, 0)):
                    if self._valid_ij(i + di, j + dj):
                        # Not marked yet
                        if not basin_mask[i + di, j + dj]:
                            # Not a 9
                            if self.grid[i + di, j + dj] != 9:
                                # Higher than current point
                                if self.grid[i, j] < self.grid[i + di, j + dj]:
                                    basin_mask[i + di, j + dj] = True

            if np.sum(previously_found ^ basin_mask) == 0:
                break
        result = np.sum(basin_mask)
        return result


def solve_pt1(data: List[str]) -> int:
    hmap = HeightMap(data)
    return hmap.risk_level()


def solve_pt2(data: List[str]) -> int:
    hmap = HeightMap(data)
    return hmap.get_largest_basin_size()


def load_data(fpath: str) -> List[List[int]]:
    data = None
    with open(fpath, "r") as f:
        data = f.read().splitlines()
    grid = [list(map(int, list(row))) for row in data]
    return grid


def main():
    example_data = load_data(EXAMPLE_DATA_PATH)
    (example_answer1, example_answer2) = (15, 1134)
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
