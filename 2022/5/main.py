from typing import Tuple, List
from enum import Enum
FILE_NAME = './input.txt'


class State(Enum):
    READING = 0
    FLUSHING = 1
    MOVING = 2


def parseMove(line: str) -> Tuple[int, int, int]:
    splitTokens = line.split(" ")

    return tuple([int(splitTokens[1]), int(splitTokens[3]) - 1, int(splitTokens[5]) - 1])


def problemTwo():
    with open(FILE_NAME, 'r') as f:

        stack = []
        parsedStacks = [[]]
        totalStacks = 1

        state = State.READING
        for line in f.readlines():

            match state:
                case State.READING:
                    if line.find("1") == -1:
                        stack.append(line)
                    else:
                        totalStacks = max([int(i)
                                          for i in line.strip() if i != " "])
                        state = State.FLUSHING

                case State.FLUSHING:
                    # line read at this point is empty
                    print(totalStacks)

                    parsedStacks: List[List[str]] = [list()
                                                     for _ in range(totalStacks)]
                    while stack:
                        level = stack.pop()
                        # parse the charachters
                        stackValues = [
                            level[4 * i + 1: 4 * (i + 1) - 2] for i in range(totalStacks)]

                        for i in range(totalStacks):
                            if stackValues[i].isalpha():
                                parsedStacks[i].append(stackValues[i])

                    state = State.MOVING
                case State.MOVING:
                    amount, sourceStack, destinationStack = parseMove(
                        line.strip())

                    toBeAdded = []
                    for _ in range(amount):
                        toBeAdded.append(parsedStacks[sourceStack].pop())

                    parsedStacks[destinationStack] += reversed(toBeAdded)
        return "".join([s[-1] for s in parsedStacks])


def problemOne():

    with open(FILE_NAME, 'r') as f:

        stack = []
        parsedStacks = [[]]
        totalStacks = 1

        state = State.READING
        for line in f.readlines():

            match state:
                case State.READING:
                    if line.find("1") == -1:
                        stack.append(line)
                    else:
                        totalStacks = max([int(i)
                                          for i in line.strip() if i != " "])
                        state = State.FLUSHING

                case State.FLUSHING:
                    # line read at this point is empty
                    print(totalStacks)

                    parsedStacks: List[List[str]] = [list()
                                                     for _ in range(totalStacks)]
                    while stack:
                        level = stack.pop()
                        # parse the charachters
                        stackValues = [
                            level[4 * i + 1: 4 * (i + 1) - 2] for i in range(totalStacks)]

                        for i in range(totalStacks):
                            if stackValues[i].isalpha():
                                parsedStacks[i].append(stackValues[i])

                    state = State.MOVING
                case State.MOVING:
                    amount, sourceStack, destinationStack = parseMove(
                        line.strip())

                    for _ in range(amount):

                        val = parsedStacks[sourceStack].pop()
                        parsedStacks[destinationStack].append(val)

        return "".join([s[-1] for s in parsedStacks])


def main():

    print(f"P1: {problemOne()}")
    print(f"P2: {problemTwo()}")


main()
