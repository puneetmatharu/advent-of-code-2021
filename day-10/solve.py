from pathlib import Path
from typing import List, Tuple


EXAMPLE_DATA_PATH = Path.cwd() / "example-data.dat"
TEST_DATA_PATH = Path.cwd() / "test-data.dat"


MATCHING_OPEN_BRACKET = {")": "(", "]":  "[", "}":  "{", ">":  "<"}
MATCHING_CLOSE_BRACKET = {"(": ")", "[":  "]", "{":  "}", "<":  ">"}


def is_corrupted(s: str) -> Tuple[bool, str, List[str]]:
    is_corrupt = False
    illegal_char = None
    stack = []
    for c in s:
        if c in "([{<":
            stack.append(c)
        else:
            open_bracket = stack.pop()
            if open_bracket != MATCHING_OPEN_BRACKET[c]:
                is_corrupt = True
                illegal_char = c
                break
    return (is_corrupt, illegal_char, stack)


def solve_pt1(report: List[str]) -> int:
    penalty = {")": 3, "]": 57, "}": 1197, ">": 25137}
    corruptions = []
    for line in report:
        (is_corrupt, illegal_char, _) = is_corrupted(line)
        if is_corrupt:
            corruptions.append(illegal_char)

    costs = list(map(lambda x: penalty[x], corruptions))
    return sum(costs)


def solve_pt2(report: List[str]) -> int:
    score_map = {")": 1, "]": 2, "}": 3, ">": 4}

    legal_lines = [x for x in report if not is_corrupted(x)[0]]

    scores = []
    for l in legal_lines:
        bracket_scores = None
        (_, _, stack) = is_corrupted(l)
        if len(stack) > 0:
            required_closing_brackets = list(
                map(lambda x: MATCHING_CLOSE_BRACKET[x], reversed(stack)))
            bracket_scores = list(
                map(lambda x: score_map[x], required_closing_brackets))

        score = 0
        for b in bracket_scores:
            score *= 5
            score += b
        scores.append(score)

    mid = (len(scores) - 1) / 2
    return sorted(scores)[int(mid)]


def load_report(fpath: str) -> List[str]:
    report = None
    with open(fpath, "r") as f:
        report = f.read().splitlines()
    return report


def main() -> int:
    example_report = load_report(EXAMPLE_DATA_PATH)
    (example_answer1, example_answer2) = (26397, 288957)
    print(f"Number of entries in report: {len(example_report)}")
    print(f"Answer to Part 1: {solve_pt1(example_report)}")
    print(f"Answer to Part 2: {solve_pt2(example_report)}")
    assert solve_pt1(example_report) == example_answer1
    assert solve_pt2(example_report) == example_answer2

    have_test_data = False
    if have_test_data:
        test_report = load_report(TEST_DATA_PATH)
        print(f"Number of entries in report: {len(test_report)}")
        print(f"Answer to Part 1: {solve_pt1(test_report)}")
        print(f"Answer to Part 2: {solve_pt2(test_report)}")


if __name__ == "__main__":
    main()
