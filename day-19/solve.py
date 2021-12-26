import re
from pathlib import Path
from typing import Callable, List, Iterator
import numpy as np
from timing import timing


EXAMPLE_DATA_PATH = Path.cwd() / "example-data1.dat"
TEST_DATA_PATH = Path.cwd() / "test-data.dat"


class Scanner:
    def __init__(self, beacons: np.ndarray):
        self.position = np.zeros((3,), dtype=int)
        self.point_cloud = beacons
        self._backup = self.point_cloud.copy()

    def reset_beacon_positions(self) -> None:
        self.point_cloud = self._backup.copy()

    def update_backups(self) -> None:
        self._backup = self.point_cloud.copy()

    def transform(self, f: np.ndarray) -> None:
        self.point_cloud = np.apply_along_axis(f, -1, self.point_cloud)

    def translate(self, shift: np.ndarray) -> None:
        shift = np.atleast_2d(shift)
        assert shift.shape[-1] == 3
        self.point_cloud += shift

    def points(self) -> Iterator:
        for p in self.point_cloud:
            yield p

    def update_positions(self, transform: int, shift: np.ndarray) -> None:
        self.position += shift
        self.transform(transform)
        self.translate(shift)
        self.update_backups()

    @staticmethod
    def orientations():
        for r in (
            lambda p: [p[0],  p[1],  p[2]],
            lambda p: [p[0],  p[2], -p[1]],
            lambda p: [p[0], -p[1], -p[2]],
            lambda p: [p[0], -p[2],  p[1]],
            lambda p: [-p[0],  p[1], -p[2]],
            lambda p: [-p[0], -p[2], -p[1]],
            lambda p: [-p[0], -p[1],  p[2]],
            lambda p: [-p[0],  p[2],  p[1]],
            lambda p: [p[1],  p[2],  p[0]],
            lambda p: [p[1],  p[0], -p[2]],
            lambda p: [p[1], -p[2], -p[0]],
            lambda p: [p[1], -p[0],  p[2]],
            lambda p: [-p[1],  p[2], -p[0]],
            lambda p: [-p[1], -p[0], -p[2]],
            lambda p: [-p[1], -p[2],  p[0]],
            lambda p: [-p[1],  p[0],  p[2]],
            lambda p: [p[2],  p[0],  p[1]],
            lambda p: [p[2],  p[1], -p[0]],
            lambda p: [p[2], -p[0], -p[1]],
            lambda p: [p[2], -p[1],  p[0]],
            lambda p: [-p[2], -p[1], -p[0]],
            lambda p: [-p[2], -p[0],  p[1]],
            lambda p: [-p[2],  p[1],  p[0]],
            lambda p: [-p[2],  p[0], -p[1]],
        ):
            yield r

    @staticmethod
    def _find_common_points(self: np.ndarray, other: np.ndarray, f: Callable):
        self_pts = self.point_cloud.copy()
        self_pset = set([tuple(p) for p in self_pts])

        # Compute reoriented positions
        other.transform(f)
        other_pts = other.point_cloud.copy()
        other.reset_beacon_positions()

        (found_match, b_pos_rel_to_a) = (False, None)
        for ia in range(len(self_pts)):
            diff = np.atleast_2d(other_pts - self_pts[ia])
            diff = diff[:, np.newaxis, :]
            shifted_other_pts = (other_pts - diff)
            for (i, row) in enumerate(shifted_other_pts):
                n_overlapped_beacons = len(self_pset & set(map(tuple, row)))
                if n_overlapped_beacons >= 12:
                    (found_match, b_pos_rel_to_a) = (True, -diff[i].squeeze())
                    return (found_match, b_pos_rel_to_a)
        return (found_match, b_pos_rel_to_a)

    def find_common_beacons(self, other: "Scanner"):
        for f in Scanner.orientations():
            (is_match, b_pos_rel_to_a) = Scanner._find_common_points(self, other, f)
            if is_match:
                return (is_match, b_pos_rel_to_a, f)
        (is_match, b_pos_rel_to_a, f) = (False, None, None)
        return (is_match, b_pos_rel_to_a, f)


@timing
def solve_pt1(scanners: List[Scanner]) -> int:
    print(f"\nAbout to begin scanner sweep. Beep. Beeep.")

    scanners_connected_to_first_scanner = set((0,))
    scanners_not_found = set(tuple(range(1, len(scanners))))

    # Keep knocking out the scanners that we haven't connected yet using
    # the scanners that we have connected (otherwise scanners won't get
    # the correct position)
    while len(scanners_not_found) > 0:

        # Create a copy for editing during the iteration
        scanners_not_found_copy = scanners_not_found.copy()
        scanners_connected_to_first_scanner_copy = scanners_connected_to_first_scanner.copy()

        found_a_beacon = False
        for i1 in scanners_connected_to_first_scanner:
            for i2 in scanners_not_found:
                (s1, s2) = (scanners[i1], scanners[i2])

                # Find matching beacons
                (is_match, b_pos_rel_to_a, f) = Scanner.find_common_beacons(s1, s2)

                # Couldn't find an overlap; move onto the next scanner
                if not is_match:
                    print(f".", end='')
                    continue

                # Found a match; print a tick
                print(u'\u2713')

                # Transform the second scanner to the same coordinate system
                s2.update_positions(transform=f, shift=b_pos_rel_to_a)

                # Add connected scanners
                scanners_not_found_copy ^= set((i2,))
                scanners_connected_to_first_scanner_copy |= set((i2,))

                # Break and start while loop again; we have to keep doing this
                # so that we can update 'scanners_not_found' and
                # 'scanners_connected_to_first_scanner_copy'
                found_a_beacon = True
                break
            if found_a_beacon:
                break

        # Update
        scanners_not_found = scanners_not_found_copy
        scanners_connected_to_first_scanner = scanners_connected_to_first_scanner_copy

    all_beacons = set()
    for scanner in scanners:
        all_beacons |= set(map(tuple, scanner.point_cloud))

    for (i, scanner) in enumerate(scanners):
        print(f"Scanner {i} position: {scanner.position}")
    return (len(all_beacons), scanners)


@timing
def solve_pt2(reoriented_scanners: List[Scanner]) -> int:
    def l1_norm(pos1: np.ndarray, pos2: np.ndarray) -> int:
        return np.sum(np.abs(pos1 - pos2))

    n_scanner = len(reoriented_scanners)
    max_l1_norm = 0
    for i in range(n_scanner):
        for j in range(i + 1, n_scanner):
            pos1 = reoriented_scanners[i].position
            pos2 = reoriented_scanners[j].position
            norm_val = l1_norm(pos1, pos2)
            max_l1_norm = max(norm_val, max_l1_norm)
    return max_l1_norm


@timing
def load_scanners(fpath: str) -> List[str]:
    contents = None
    with open(fpath, "r") as f:
        contents = f.read()
    contents = re.sub(r"\n\n", r"\n", contents)
    scanners_data = re.split(r"--- scanner \d\d? ---\n", contents)[1:]

    scanners = []
    for scanner_data in scanners_data:
        beacons = [l.split(",") for l in scanner_data.splitlines()]
        beacons = np.array([list(map(int, line)) for line in beacons])
        beacons = beacons.astype(int)
        scanners.append(Scanner(beacons=beacons))
    return scanners


@timing
def main() -> int:
    transmission = load_scanners(EXAMPLE_DATA_PATH)
    (answer1, _) = solve_pt1(transmission)
    print(f"Answer to Part 1: {answer1}")
    assert answer1 == 79

    have_test_data = True
    if have_test_data:
        test_scanners = load_scanners(TEST_DATA_PATH)
        (solution1, solution2) = (425, 13354)
        (answer1, reoriented_scanners) = solve_pt1(test_scanners)
        answer2 = solve_pt2(reoriented_scanners)
        print(f"Answer to Part 1: {answer1}")
        print(f"Answer to Part 2: {answer2}")
        assert answer2 == solution1
        assert answer2 == solution2


if __name__ == "__main__":
    main()
