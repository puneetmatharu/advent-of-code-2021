from pathlib import Path
from typing import List


DATAFILE_PATH = Path.cwd() / "data.dat"


def solve_pt1(measurements: List[int]) -> int:
    counter = 0
    for i in range(len(measurements) - 1):
        counter += (measurements[i + 1] > measurements[i])
    return counter


def solve_pt2(measurements: List[int]) -> int:
    def sum_sliding_window(arr: List[int], start_index: int) -> int:
        return arr[start_index] + arr[start_index + 1] + arr[start_index + 2]
    counter = 0
    for i in range(len(measurements) - 3):
        counter += (sum_sliding_window(measurements, i + 1) > sum_sliding_window(measurements, i))
    return counter


def load_measurements() -> List[int]:
    measurements = None
    with open(DATAFILE_PATH, "r") as f:
        measurements = f.readlines()
    measurements = list(map(int, measurements))
    return measurements


def main() -> int:
    measurements = load_measurements()
    print(f"Number of measurements: {len(measurements)}")
    print(f"Answer to Part 1: {solve_pt1(measurements)}")
    print(f"Answer to Part 2: {solve_pt2(measurements)}")


if __name__ == "__main__":
    main()
