from pathlib import Path
from typing import Callable, List
import numpy as np


EXAMPLE_DATA_PATH = Path.cwd() / "example-data.dat"
TEST_DATA_PATH = Path.cwd() / "test-data.dat"


def solve_pt1(positions: List[int]) -> int:
    def cost(x: np.ndarray, x_p: int):
        return np.sum(np.abs(x - x_p))
    x_min = round(np.median(positions))
    return cost(positions, x_min)


def newton_raphson(f: Callable) -> int:
    (x, n_iter, dx) = (5, 1000, 1.0e-04)
    for _ in range(n_iter):
        fx = f(x)
        df_dx = (f(x + dx) - fx) / dx
        update = (fx / df_dx)
        if df_dx == 0:
            break
        x -= update
    return x


def solve_pt2(positions: List[int]) -> int:
    def cost(x: np.ndarray, x_p: int) -> int:
        dists = np.abs(x_p - x)
        costs = (dists * (dists + 1)) / 2
        return int(np.sum(costs))

    def dcost_dx_p(x: np.ndarray, x_p: int):
        dc_dx_p = 0.0
        for i in range(len(x)):
            dc_dx_p += np.sign((x_p - x[i]) *
                               (x_p - x[i] + 1)) * (2*x_p - 2*x[i] + 1)
        dc_dx_p /= 2.0
        return dc_dx_p

    # Returns the floating-point minimum
    x_p = newton_raphson(lambda x_pos: dcost_dx_p(positions, x_pos))

    # Check the cost for each integer position either side of the minimum; take
    # the position that leads to the smallest cost
    x_range = (int(np.floor(x_p)), int(np.ceil(x_p)))
    costs = list(map(lambda x: cost(positions, x), x_range))
    fuel = min(costs)
    return fuel


def load_positions(fpath: str) -> List[int]:
    positions = None
    with open(fpath, "r") as f:
        positions = f.readline()
    return np.array(list(map(int, positions.split(","))))


def main() -> int:
    example_positions = load_positions(EXAMPLE_DATA_PATH)
    (example_answer1, example_answer2) = (37, 168)
    print(f"Number of entries in positions: {len(example_positions)}")
    print(f"Answer to Part 1: {solve_pt1(example_positions)}")
    print(f"Answer to Part 2: {solve_pt2(example_positions)}")
    assert solve_pt1(example_positions) == example_answer1
    assert solve_pt2(example_positions) == example_answer2

    test_positions = load_positions(TEST_DATA_PATH)
    print(f"Number of entries in positions: {len(test_positions)}")
    print(f"Answer to Part 1: {solve_pt1(test_positions)}")
    print(f"Answer to Part 2: {solve_pt2(test_positions)}")


if __name__ == "__main__":
    main()
