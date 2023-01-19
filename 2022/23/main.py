from collections import defaultdict
from functools import reduce


INPUT_FILE = "./input.txt"


def getBoardString(elves):

    minRow = min([e[0] for e in elves])
    minCol = min([e[1] for e in elves])

    maxRow = max([e[0] for e in elves])
    maxCol = max([e[1] for e in elves])

    ret = ""
    for row in range(minRow, maxRow + 1):

        rowString = ""

        for col in range(minCol, maxCol + 1):

            if (row, col) in elves:

                rowString += "#"
            else:
                rowString += "."

        ret += rowString + "\n"

    return ret


def printBoard(elves):
    print(getBoardString(elves))


with open(INPUT_FILE, "r") as f:

    elves = defaultdict()

    for row, line in enumerate(f):

        for col, value in enumerate(line.strip()):

            if value == "#":

                elves[(row, col)] = (row, col)

    ROWS = row
    COLS = col

    i = 0

    directionsMap = {
        (-1, 0): [(-1, -1), (-1, 1)],
        (1, 0): [(1, -1), (1, 1)],
        (0, -1): [(-1, -1), (1, -1)],
        (0, 1): [(1, 1), (-1, 1)],
        (0, 0): [
            (i, j) for i in [-1, 0, 1] for j in [-1, 0, 1] if not (i == 0 and j == 0)
        ],
    }

    directionCheckingOrder = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    while True:

        print(f"ROUND {i + 1}", end="\r")

        # print(
        #     f"CHECKING {directionCheckingOrder[i % len(directionCheckingOrder)]} first"
        # )

        move = False

        for elf in elves:

            if not any(
                (elf[0] + elfLoc[0], elf[1] + elfLoc[1]) in elves
                for elfLoc in directionsMap[(0, 0)]
            ):
                # print(f"ELF: {elf} moved to {elves[elf]}")
                continue

            for d in list(range(i, i + 4)):
                direction = directionCheckingOrder[d % len(directionCheckingOrder)]

                if not any(
                    (elf[0] + elfLoc[0], elf[1] + elfLoc[1]) in elves
                    for elfLoc in [direction] + directionsMap[direction]
                ):

                    proposed = (elf[0] + direction[0], elf[1] + direction[1])

                    # print(f"ELF: {elf} moved to {proposed}")

                    elves[elf] = proposed

                    move = True
                    break

        # check if elves are going to a colliding position
        # every elf with the same value,

        if not move:
            print()
            print(f"P2: {i + 1}")
            break
        elvesGroupedByProposal = defaultdict(list)

        for elf, proposal in elves.items():

            elvesGroupedByProposal[proposal].append(elf)

        for proposal, elfGroup in elvesGroupedByProposal.items():
            if len(elfGroup) > 1:
                # reset them to their current position
                for e in elfGroup:
                    elves[e] = e

        # move all the elves

        newElfPosition = dict()
        for elfPos in elves:
            newElfPosition[elves[elfPos]] = elves[elfPos]

        elves = newElfPosition

        # printBoard(elves)

        i += 1

        if i == 10:

            boardString = getBoardString(elves)
            print()
            print(
                "P1:",
                len([c for line in boardString.split("\n") for c in line if c != "#"]),
            )
