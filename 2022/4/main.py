from functools import cache
from typing import Tuple
FILE_NAME = './input.txt'


def doesLeftContainRight(left: Tuple[int, int], right: Tuple[int, int]) -> bool:
    return left[0] <= right[0] and left[1] >= right[1]


@cache
def doesEitherIntervalSubsume(a: Tuple[int, int], b: Tuple[int, int]) -> int:
    return doesLeftContainRight(a, b) or doesLeftContainRight(b, a)


def doesLeftOverLapWithRight(a: Tuple[int, int], b: Tuple[int, int]) -> int:
    # is any point in b contained inside a. must be true if they overlap
    return a[0] <= b[0] <= a[1] or a[0] <= b[1] <= a[1]


@cache
def doIntervalsOverlap(a: Tuple[int, int], b: Tuple[int, int]) -> int:
    # intervals overlap if either contains a point within the other
    return doesLeftOverLapWithRight(a, b) or doesLeftOverLapWithRight(b, a)


def parseInterval(line: str) -> Tuple[Tuple[int, int], Tuple[int, int]]:
    return tuple(tuple(int(bound) for bound in elf.split("-")) for elf in line.split(","))


def problemTwo():
    with open(FILE_NAME, 'r') as f:

        totalSum = 0
        for line in f.readlines():
            line = line[:len(line)-1]

            elfA, elfB = parseInterval(line)

            if doIntervalsOverlap(elfA, elfB):
                totalSum += 1

        return totalSum


def problemOne():

    with open(FILE_NAME, 'r') as f:

        totalSum = 0
        for line in f.readlines():
            line = line[:len(line)-1]

            elfA, elfB = parseInterval(line)

            if doesEitherIntervalSubsume(elfA, elfB):
                totalSum += 1

        return totalSum


def main():

    def test(x): return print(x, doIntervalsOverlap(*parseInterval(x)))

    test("5-7,7-9")
    test("3-7,2-8")
    test("6-6,4-6")
    test("2-6,4-8")
    print(f"P1: {problemOne()}")
    print(f"P2: {problemTwo()}")


main()
