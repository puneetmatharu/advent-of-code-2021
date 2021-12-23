from pathlib import Path
from typing import List, Union

EXAMPLES = (
    (Path.cwd() / "example-data11.dat", (6, None)),
    (Path.cwd() / "example-data12.dat", (16, None)),
    (Path.cwd() / "example-data13.dat", (12, None)),
    (Path.cwd() / "example-data14.dat", (23, None)),
    (Path.cwd() / "example-data15.dat", (31, None)),
    (Path.cwd() / "example-data21.dat", (None, 3)),
    (Path.cwd() / "example-data22.dat", (None, 54)),
    (Path.cwd() / "example-data23.dat", (None, 7)),
    (Path.cwd() / "example-data24.dat", (None, 9)),
    (Path.cwd() / "example-data25.dat", (None, 1)),
    (Path.cwd() / "example-data26.dat", (None, 0)),
    (Path.cwd() / "example-data27.dat", (None, 0)),
    (Path.cwd() / "example-data28.dat", (None, 1)),
)
TEST_DATA_PATH = Path.cwd() / "test-data.dat"


class PrettyPrinter(object):
    def __str__(self):
        lines = [self.__class__.__name__ + ":"]
        for key, val in vars(self).items():
            new_lines = ""
            if isinstance(val, (list, tuple)):
                new_lines += f"{key}: [\n"
                for entry in val:
                    new_lines += f"    {entry},\n"
                new_lines += f"]"
            else:
                new_lines += f"{key}: {val}"
            lines += new_lines.split("\n")
        return "\n    ".join(lines)


class Subpacket(PrettyPrinter):
    def __init__(self, version: int, type_id: int, data: Union[int, List["Subpacket"]]):
        self.version = version
        self.type_id = type_id
        self.data = data

    def __repr__(self):
        return str(self)

    def is_operator(self) -> bool:
        return self.type_id != 4

    def value(self) -> int:
        if not self.is_operator():
            return self.data

        assert isinstance(self.data, (list, tuple))

        operator_value = 0

        if self.type_id == 0:
            for entry in self.data:
                operator_value += entry.value()

        elif self.type_id == 1:
            operator_value = 1
            for entry in self.data:
                operator_value *= entry.value()

        elif self.type_id in [2, 3]:
            values = []
            for entry in self.data:
                values.append(entry.value())
            if self.type_id == 2:
                operator_value = min(values)
            elif self.type_id == 3:
                operator_value = max(values)

        elif self.type_id in [5, 6, 7]:
            assert len(self.data) == 2
            if self.type_id == 5:
                operator_value = int(
                    self.data[0].value() > self.data[1].value())
            elif self.type_id == 6:
                operator_value = int(
                    self.data[0].value() < self.data[1].value())
            elif self.type_id == 7:
                operator_value = int(
                    self.data[0].value() == self.data[1].value())
        else:
            raise ValueError(f"ERROR: Subpacket has type ID: {self.type_id}")

        return operator_value


class Stream:
    def __init__(self, data: str):
        self._data = data
        self._position = 0

    @staticmethod
    def _split_at(s: str, n: int):
        return (s[:n], s[n:])

    def consume(self, n_bit: int) -> str:
        assert (len(self._data) > 0) and (n_bit <= len(self._data))
        (output, self._data) = Stream._split_at(self._data, n_bit)
        self._position += n_bit
        return output

    def position(self) -> int:
        return self._position

    def __str__(self) -> str:
        return self._data


class Decoder:
    def __init__(self, data: str):
        self._orig_code = data
        self.code = Stream(data)

    def consume(self, n_bit: int) -> str:
        return self.code.consume(n_bit)

    def position(self) -> int:
        return self.code.position()

    def parse_header(self) -> List[int]:
        version = int(self.consume(n_bit=3), base=2)
        type_id = int(self.consume(n_bit=3), base=2)
        return (version, type_id)

    def parse(self) -> List[Subpacket]:
        (version, type_id) = self.parse_header()

        packets = None
        if type_id == 4:
            chunks = []
            while True:
                chunk = self.consume(n_bit=5)
                chunks.append(chunk[1:])
                if chunk[0] == "0":
                    break
            number = int("".join(chunks), base=2)
            new_subpacket = Subpacket(version, type_id, data=number)
            packets = new_subpacket
        else:
            subpackets = []
            length_type_id = int(self.consume(n_bit=1))
            if length_type_id == 0:
                total_length = int(self.consume(n_bit=15), base=2)
                start_posn = self.position()
                while self.position() - start_posn < total_length:
                    subpackets.append(self.parse())
            elif length_type_id == 1:
                n_subpacket = int(self.consume(n_bit=11), base=2)
                for _ in range(n_subpacket):
                    subpackets.append(self.parse())

            new_subpacket = Subpacket(version, type_id, data=subpackets)
            packets = new_subpacket

        return packets


def flatten(packet: Subpacket):
    assert isinstance(packet, Subpacket)
    flattened_packets = []

    if isinstance(packet.data, (int, float)):
        flattened_packets.append(packet)
    elif isinstance(packet.data, (list, tuple)):
        inner_packets = []
        for j in packet.data:
            inner_packets += flatten(j)
        packet.data = None
        flattened_packets += [packet]
        flattened_packets += inner_packets

    return flattened_packets


def solve_pt1(transmission: List[str]) -> int:
    decoder = Decoder(transmission)
    packets = decoder.parse()
    flattened_packets = flatten(packets)
    sum_value = sum(map(lambda x: x.version, flattened_packets))
    return sum_value


def solve_pt2(transmission: List[str]) -> int:
    decoder = Decoder(transmission)
    packets = decoder.parse()
    outer_packet_value = packets.value()
    return outer_packet_value


def load_transmission(fpath: str) -> List[str]:
    def hex_to_bin(x: str):
        return bin(int(x, 16))[2:].zfill(4)

    transmission = None
    with open(fpath, "r") as f:
        transmission = f.read()
    transmission = "".join(list(map(hex_to_bin, transmission)))
    return transmission


def main() -> int:
    for (fname, (solution1, solution2)) in EXAMPLES:
        transmission = load_transmission(fname)
        if solution1:
            answer1 = solve_pt1(transmission)
            print(f"Answer to Part 1: {answer1}")
            assert answer1 == solution1
        if solution2:
            answer2 = solve_pt2(transmission)
            print(f"Answer to Part 2: {answer2}")
            assert answer2 == solution2

    have_test_data = True
    if have_test_data:
        transmission = load_transmission(TEST_DATA_PATH)
        answer1 = solve_pt1(transmission)
        answer2 = solve_pt2(transmission)
        print(f"Answer to Part 1: {answer1}")
        print(f"Answer to Part 2: {answer2}")


if __name__ == "__main__":
    main()
