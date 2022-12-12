from collections import Counter
from functools import reduce
import math
import operator
from typing import Callable, List, Tuple

INPUT_FILE = "./input.txt"


class Monkey:
    def __init__(
        self,
        queue: List[int],
        operation: Callable[[int], int],
        dividend: int,
        test: Callable[[int], int],
    ) -> None:
        self.queue = queue
        self.operation = operation
        self.dividend = dividend
        self.test = test

    def __repr__(self) -> str:
        return f"q:{self.queue}"


def testHelper(dividend, trueMonkey, falseMonkey) -> Tuple[int, Callable[[int], int]]:
    return dividend, lambda x: trueMonkey if x % dividend == 0 else falseMonkey


monkeyArray = lambda: [
    Monkey([57, 58], lambda old: old * 19, *testHelper(7, 2, 3)),
    Monkey([66, 52, 59, 79, 94, 73], lambda old: old + 1, *testHelper(19, 4, 6)),
    Monkey([80], lambda old: old + 6, *testHelper(5, 7, 5)),
    Monkey(
        [82, 81, 68, 66, 71, 83, 75, 97], lambda old: old + 5, *testHelper(11, 5, 2)
    ),
    Monkey([55, 52, 67, 70, 69, 94, 90], lambda old: old * old, *testHelper(17, 0, 3)),
    Monkey([69, 85, 89, 91], lambda old: old + 7, *testHelper(13, 1, 7)),
    Monkey([75, 53, 73, 52, 75], lambda old: old * 7, *testHelper(2, 0, 4)),
    Monkey([94, 60, 79], lambda old: old + 2, *testHelper(3, 1, 6)),
]


testMonkeyArray = lambda: [
    Monkey([79, 98], lambda old: old * 19, *testHelper(23, 2, 3)),
    Monkey([54, 65, 75, 74], lambda old: old + 6, *testHelper(19, 2, 0)),
    Monkey([79, 60, 97], lambda old: old * old, *testHelper(13, 1, 3)),
    Monkey([74], lambda old: old + 3, *testHelper(17, 0, 1)),
]


def monkeyRoundProcessor(monkeys: List[Monkey], totalRounds=1):

    round = 0

    monkeyTestCounter = Counter()
    while round < totalRounds:
        round += 1
        for index, monkey in enumerate(monkeys):
            for oldWorry in monkey.queue:
                newWorryLevel = monkey.operation(oldWorry) // 3
                receivingMonkey = monkey.test(newWorryLevel)
                monkeys[receivingMonkey].queue.append(newWorryLevel)

            monkeyTestCounter[index] += len(monkey.queue)
            monkey.queue = []

    topTwo = monkeyTestCounter.most_common(2)

    print(topTwo[0][1] * topTwo[1][1])


print("PT: 1")
monkeyRoundProcessor(testMonkeyArray(), 20)
monkeyRoundProcessor(monkeyArray(), 20)


def boundedMonkeyRoundProcessor(monkeys: List[Monkey], totalRounds=1):

    round = 0

    monkeyTestCounter = Counter()

    # https://en.wikipedia.org/wiki/Modular_arithmetic
    # outputs of polynomial functions will maintain equality post modular application
    # to ensure consistent monkey.test outputs across all potential calls, the dividend
    # we need to choose is the one that they all share. This can be trivially computed by
    # multiplying all the dividends together. If the dividends weren't co prime, this would not
    # be the smallest possible bound.
    boundedValue = reduce(operator.mul, [m.dividend for m in monkeys], 1)

    print(f"Starting with monkeys = {monkeys}")
    while round < totalRounds:
        round += 1

        print(f"on round {round}", end="\r")
        for index, monkey in enumerate(monkeys):
            for oldWorry in monkey.queue:
                newWorryLevel = monkey.operation(oldWorry)
                receivingMonkey = monkey.test(newWorryLevel)
                monkeys[receivingMonkey].queue.append(newWorryLevel % boundedValue)

            monkeyTestCounter[index] += len(monkey.queue)
            monkey.queue = []

    print()
    print("done")
    topTwo = monkeyTestCounter.most_common(2)

    print(topTwo[0][1] * topTwo[1][1])


print("PT: 2")
boundedMonkeyRoundProcessor(testMonkeyArray(), 10000)
boundedMonkeyRoundProcessor(monkeyArray(), 10000)
