from pathlib import Path
from typing import List


EXAMPLE_DATA_PATH = Path.cwd() / "example-data.dat"
TEST_DATA_PATH = Path.cwd() / "test-data.dat"


def solve_pt1(report: List[str]) -> int:
    n_entry = len(report)
    bitwidth = len(report[0])

    one_counts = [0] * bitwidth
    for string in report:
        for i, c in enumerate(string):
            one_counts[i] += (1 if (int(c) == 1) else 0)

    gamma = [None] * bitwidth
    for i in range(len(gamma)):
        gamma[i] = ("1" if ((2 * one_counts[i]) > n_entry) else "0")
    gamma = "".join(gamma)
    gamma = int(gamma, base=2)

    epsilon = (2 ** bitwidth) - 1 - gamma
    return gamma * epsilon


def solve_pt2(report_in: List[str]) -> int:

    def calculate_rating(report_in: List[str], criteria: str) -> str:
        report = report_in.copy()
        (index, bitwidth) = (0, len(report[0]))
        while (len(report) > 1) and (index < bitwidth):
            n_entry = len(report)
            n_one = sum([int(string[index]) for string in report])
            n_zero = n_entry - n_one
            if criteria == "most common":
                filter_value = str(1 if (n_one >= n_zero) else 0)
            if criteria == "least common":
                filter_value = str(0 if (n_zero <= n_one) else 1)
            report = list(filter(lambda s: s[index] == filter_value, report))
            index += 1
        assert len(report) == 1
        return int(report[0], 2)

    report = report_in.copy()
    (oxy_rating, co2_rating) = (0, 0)
    oxy_rating = calculate_rating(report, criteria="most common")
    co2_rating = calculate_rating(report, criteria="least common")
    return oxy_rating * co2_rating


def load_report(fpath: str) -> List[str]:
    report = None
    with open(fpath, "r") as f:
        report = f.readlines()
    report = list(map(lambda x: x.rstrip("\n"), report))
    return report


def main() -> int:
    example_report = load_report(EXAMPLE_DATA_PATH)
    (example_answer1, example_answer2) = (198, 230)
    print(f"Number of entries in report: {len(example_report)}")
    print(f"Answer to Part 1: {solve_pt1(example_report)}")
    print(f"Answer to Part 2: {solve_pt2(example_report)}")
    assert solve_pt1(example_report) == example_answer1
    assert solve_pt2(example_report) == example_answer2

    test_report = load_report(TEST_DATA_PATH)
    print(f"Number of entries in report: {len(test_report)}")
    print(f"Answer to Part 1: {solve_pt1(test_report)}")
    print(f"Answer to Part 2: {solve_pt2(test_report)}")
    (test_answer1, test_answer2) = (693486, 3379326)
    assert solve_pt1(test_report) == test_answer1
    assert solve_pt2(test_report) == test_answer2


if __name__ == "__main__":
    main()
