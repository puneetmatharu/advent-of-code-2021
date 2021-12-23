from pathlib import Path
from typing import List
import numpy as np


EXAMPLE_DATA_PATH = Path.cwd() / "example-data.dat"
TEST_DATA_PATH = Path.cwd() / "test-data.dat"


def print_paper(p):
    string = str(p.astype(int))
    string = string.replace(",", "")
    string = string.replace("0", ".")
    string = string.replace("1", "#")
    print(f"\n{string}\n")


def apply_folds(paper: np.ndarray, folds: List[List[int]]) -> np.ndarray:
    for (axis, pos) in folds:
        (p1, _, p2) = np.split(paper, [pos, pos+1], axis=axis)
        p2 = np.flip(p2, axis=axis)
        (p1, p2) = sorted([p1, p2], key=lambda x: x.shape[axis], reverse=True)
        overlap = p2.shape[axis]
        if axis == 0:
            p1[-overlap:, :] |= p2[-overlap:, :]
        elif axis == 1:
            p1[:, -overlap:] |= p2[:, -overlap:]
        paper = p1
    return paper


def solve_pt1(dots: List[List[int]], folds: List[List[int]]) -> int:
    (max_i, max_j) = (-1, -1)
    for (i, j) in dots:
        max_i = max(i, max_i)
        max_j = max(j, max_j)

    paper = np.zeros((max_i + 1, max_j + 1), dtype=bool)
    for (i, j) in dots:
        paper[i, j] = True

    # print_paper(paper)
    paper = apply_folds(paper.copy(), folds[:1])
    # print_paper(paper)
    return paper.sum()


def solve_pt2(dots: List[List[int]], folds: List[List[int]]) -> None:
    (max_i, max_j) = (-1, -1)
    for (i, j) in dots:
        max_i = max(i, max_i)
        max_j = max(j, max_j)

    paper = np.zeros((max_i + 1, max_j + 1), dtype=bool)
    for (i, j) in dots:
        paper[i, j] = True

    paper = apply_folds(paper.copy(), folds)
    with np.printoptions(linewidth=120):
        print_paper(paper)
    return None


def load_report(fpath: str) -> List[List[List[int]]]:
    (dots, folds) = (None, None)
    with open(fpath, "r") as f:
        (dots, folds) = f.read().split("\n\n")
    (dots, folds) = (dots.splitlines(), folds.splitlines())
    dots = [list(map(int, d.split(","))) for d in dots]
    dots = [(i, j) for (j, i) in dots]
    folds = [f.split(" ")[2].split("=") for f in folds]
    dir_map = {"x": 1, "y": 0}
    folds = [[dir_map[c], int(num)] for (c, num) in folds]
    return (dots, folds)


def main() -> int:
    (dots, folds) = load_report(EXAMPLE_DATA_PATH)
    (example_answer1, example_answer2) = (17, None)
    print(f"Number of (dots, folds): {(len(dots), len(folds))}")
    answer1 = solve_pt1(dots, folds)
    answer2 = solve_pt2(dots, folds)
    print(f"Answer to Part 1: {answer1}")
    print(f"Answer to Part 2: {answer2}")
    assert answer1 == example_answer1
    assert answer2 == example_answer2

    have_test_data = True
    if have_test_data:
        (dots, folds) = load_report(TEST_DATA_PATH)
        answer1 = solve_pt1(dots, folds)
        answer2 = solve_pt2(dots, folds)
        print(f"Answer to Part 1: {answer1}")
        print(f"Answer to Part 2: {answer2}")


if __name__ == "__main__":
    main()
