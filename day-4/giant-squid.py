from pathlib import Path
from typing import List, Tuple
from copy import deepcopy
import numpy as np
import re

EXAMPLE_DATA_PATH = Path.cwd() / "example-data.dat"
TEST_DATA_PATH = Path.cwd() / "test-data.dat"


class BingoTable:
    def __init__(self, data: List[int]):
        assert len(data) == 25
        self._table = np.array(data).reshape((5, 5))
        self._crossed_boxes = np.zeros((5, 5), dtype=bool)
        self._winning_number = None
        self._have_bingo = False

    def __str__(self) -> str:
        return "\nValues:\n" + str(self._table) + "\nMarked:\n" + str(self._crossed_boxes)

    def __repr__(self) -> str:
        return str(self)

    def check_bingo(self) -> bool:
        bingo = False
        for row in range(5):
            bingo |= np.all(self._crossed_boxes[row, :])
        for col in range(5):
            bingo |= np.all(self._crossed_boxes[:, col])
        self._have_bingo = bingo
        return bingo

    def mark(self, value: int) -> bool:
        have_bingo = self.check_bingo()
        if not self._have_bingo:
            self._crossed_boxes |= (self._table == value)
            have_bingo = self.check_bingo()
            if have_bingo:
                self._winning_number = value
        return have_bingo

    def clear(self) -> bool:
        self._crossed_boxes ^= self._crossed_boxes
        self._have_bingo = False

    def calculate_winning_score(self) -> int:
        unmarked_numbers_sum = np.sum(self._table * ~self._crossed_boxes)
        return self._winning_number * unmarked_numbers_sum


def solve_pt1(drawn_numbers: List[int], tables: List[BingoTable]) -> int:
    finished = False
    for value in drawn_numbers:
        for table in tables:
            finished = table.mark(value)
            if finished:
                return table.calculate_winning_score()
    return None


def solve_pt2(drawn_numbers: List[int], tables: List[BingoTable]) -> int:
    order_of_wins = []
    for value in drawn_numbers:
        for index, table in enumerate(tables):
            finished = table.mark(value)
            if finished and index not in order_of_wins:
                order_of_wins.append(index)
    last_win = order_of_wins[-1]
    return tables[last_win].calculate_winning_score()


def load(fpath: str) -> Tuple[List[int], List[BingoTable]]:
    squeeze_spaces = (lambda s : re.sub(' +', ' ', s))

    with open(fpath, "r") as f:
        data = f.readlines()

    def string_to_table(table_as_str: str) -> BingoTable:
        table_as_str = table_as_str.replace("\n", " ")
        table_as_str = squeeze_spaces(table_as_str).strip()
        table_as_str = table_as_str.split()
        table = list(map(int, table_as_str))
        return BingoTable(table)

    [drawn_numbers, data] = [list(map(int, data[0].split(","))), data[1:]]

    tables = []
    n_table = len(data) // 6
    for _ in range(n_table):
        table = ""

        # Skip empty line
        data = data[1:]

        # Read table
        table = string_to_table(" ".join(data[:5]))
        tables.append(table)
        data = data[5:]

    return [drawn_numbers, tables]


def main() -> int:
    # EXAMPLE DATA

    [drawn_numbers, tables] = load(EXAMPLE_DATA_PATH)
    (tables1, tables2) = (tables, deepcopy(tables))
    (example_answer1, example_answer2) = (4512, 1924)
    print(f"Number of drawn numbers: {len(drawn_numbers)}")
    print(f"Number of tables: {len(tables1)}")
    answer1 = solve_pt1(drawn_numbers, tables1)
    answer2 = solve_pt2(drawn_numbers, tables2)
    print(f"Answer to Part 1: {answer1}")
    print(f"Answer to Part 2: {answer2}")
    assert answer1 == example_answer1
    assert answer2 == example_answer2

    # TEST DATA

    [drawn_numbers, tables] = load(TEST_DATA_PATH)
    (tables1, tables2) = (tables, deepcopy(tables))
    print(f"Number of drawn numbers: {len(drawn_numbers)}")
    print(f"Number of tables: {len(tables1)}")
    answer1 = solve_pt1(drawn_numbers, tables1)
    answer2 = solve_pt2(drawn_numbers, tables2)
    print(f"Answer to Part 1: {answer1}")
    print(f"Answer to Part 2: {answer2}")


if __name__ == "__main__":
    main()
