from collections import defaultdict
import math
import re

INPUT_FILE = "./input.txt"


def constructBoardOne(lines):
    board = dict()

    ROWS = 0
    COLS = 0

    parsingBoard = True

    monkeyPath: str = "R"

    for line in lines:
        parsed: str = line.strip("\n")

        if len(parsed) == 0:
            parsingBoard = False
            continue

        if parsingBoard:
            ROWS += 1
            padding = re.search("\.|#", parsed).span()[0]

            board.update(
                [
                    ((ROWS, padding + col + 1), val)
                    for col, val in enumerate(parsed.strip())
                ]
            )

            COLS = max(COLS, len(parsed))

        else:
            monkeyPath += parsed

    neighbors = defaultdict(dict)

    for location in board:
        for direction in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            neighbor = (location[0] + direction[0], location[1] + direction[1])
            if neighbor not in board:
                start = location
                end = None

                while True:
                    if start not in board:
                        break

                    end = start
                    start = (-1 * direction[0] + start[0], -1 * direction[1] + start[1])

                # print(
                #     f"Neighbor for {location} is now {end}. {board[location]} => {board[end]}"
                # )

                neighbors[location][direction] = end + tuple([direction])

            else:
                neighbors[location][direction] = neighbor + tuple([direction])
    return board, monkeyPath, neighbors, ROWS // 4


def constructBoardTwo(lines):
    board = dict()

    ROWS = 0
    COLS = 0

    SIDE_LENGTH = None

    parsingBoard = True

    monkeyPath: str = "R"

    for line in lines:
        parsed: str = line.strip("\n")

        if len(parsed) == 0:
            parsingBoard = False
            continue

        if parsingBoard:
            ROWS += 1
            padding = re.search("\.|#", parsed).span()[0]

            if SIDE_LENGTH == None:
                SIDE_LENGTH = len(parsed.strip()) // 2

            for col, val in enumerate(parsed.strip()):

                board[(ROWS, padding + col + 1)] = val

            COLS = max(COLS, len(parsed))

        else:
            monkeyPath += parsed

    neighbors = defaultdict(dict)

    for location in sorted(board, key=lambda p: SIDE_LENGTH * 3 * p[0] + p[1]):
        for direction in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            neighbor = (
                location[0] + direction[0],
                location[1] + direction[1],
            )
            if neighbor not in board:
                row = location[0]
                col = location[1]

                newNeighbor = None

                # I didn't like this. I feel like reversing the cubic projection is a lot more difficult than
                # the going from cube to projection

                # in another world, I would've started in the cubic space, annotated the cells from their projection
                # and traversed the map in the cubic space instead of the projection space.
                if (
                    row == 1
                    and SIDE_LENGTH + 1 <= col < 2 * SIDE_LENGTH + 1
                    and direction == (-1, 0)
                ):
                    newNeighbor = (
                        3 * SIDE_LENGTH + col - SIDE_LENGTH,
                        1,
                        (0, 1),
                    )
                elif (
                    row == 1
                    and 2 * SIDE_LENGTH + 1 <= col < 3 * SIDE_LENGTH + 1
                    and direction == (-1, 0)
                ):
                    newNeighbor = (
                        4 * SIDE_LENGTH,
                        col - (2 * SIDE_LENGTH),
                        (-1, 0),
                    )
                elif (
                    row == SIDE_LENGTH
                    and 2 * SIDE_LENGTH + 1 <= col < 3 * SIDE_LENGTH + 1
                    and direction == (1, 0)
                ):
                    newNeighbor = (
                        SIDE_LENGTH + col - (2 * SIDE_LENGTH),
                        2 * SIDE_LENGTH,
                        (0, -1),
                    )

                elif (
                    row == 2 * SIDE_LENGTH + 1
                    and 1 <= col < SIDE_LENGTH + 1
                    and direction == (-1, 0)
                ):
                    newNeighbor = (SIDE_LENGTH + col, SIDE_LENGTH + 1, (0, 1))
                elif (
                    row == 3 * SIDE_LENGTH
                    and SIDE_LENGTH + 1 <= col < 2 * SIDE_LENGTH + 1
                    and direction == (1, 0)
                ):
                    newNeighbor = (
                        3 * SIDE_LENGTH + (col - SIDE_LENGTH),
                        SIDE_LENGTH,
                        (0, -1),
                    )
                elif (
                    row == 4 * SIDE_LENGTH
                    and 1 <= col < SIDE_LENGTH + 1
                    and direction == (1, 0)
                ):
                    newNeighbor = (
                        1,
                        2 * SIDE_LENGTH + (col),
                        (1, 0),
                    )
                elif (
                    col == SIDE_LENGTH + 1
                    and 1 <= row < SIDE_LENGTH + 1
                    and direction == (0, -1)
                ):
                    newNeighbor = (
                        (3 * SIDE_LENGTH) - (row) + 1,
                        1,
                        (0, 1),
                    )

                elif (
                    col == 3 * SIDE_LENGTH
                    and 1 <= row < SIDE_LENGTH + 1
                    and direction == (0, 1)
                ):
                    newNeighbor = (
                        (3 * SIDE_LENGTH) - row + 1,
                        2 * SIDE_LENGTH,
                        (0, -1),
                    )
                elif (
                    col == SIDE_LENGTH + 1
                    and SIDE_LENGTH + 1 <= row < 2 * SIDE_LENGTH + 1
                    and direction == (0, -1)
                ):

                    newNeighbor = (
                        2 * SIDE_LENGTH + 1,
                        row - SIDE_LENGTH,
                        (1, 0),
                    )

                elif (
                    col == 2 * SIDE_LENGTH
                    and SIDE_LENGTH + 1 <= row < 2 * SIDE_LENGTH + 1
                    and direction == (0, 1)
                ):
                    newNeighbor = (
                        SIDE_LENGTH,
                        2 * SIDE_LENGTH + row - SIDE_LENGTH,
                        (-1, 0),
                    )

                elif (
                    col == 1
                    and 2 * SIDE_LENGTH + 1 <= row < 3 * SIDE_LENGTH + 1
                    and direction == (0, -1)
                ):
                    newNeighbor = (
                        SIDE_LENGTH - (row - (2 * SIDE_LENGTH)) + 1,
                        SIDE_LENGTH + 1,
                        (0, 1),
                    )

                elif (
                    col == 2 * SIDE_LENGTH
                    and 2 * SIDE_LENGTH + 1 <= row < 3 * SIDE_LENGTH + 1
                    and direction == (0, 1)
                ):
                    newNeighbor = (
                        SIDE_LENGTH - (row - (2 * SIDE_LENGTH)) + 1,
                        3 * SIDE_LENGTH,
                        (0, -1),
                    )

                elif (
                    col == 1
                    and 3 * SIDE_LENGTH + 1 <= row < 4 * SIDE_LENGTH + 1
                    and direction == (0, -1)
                ):
                    newNeighbor = (
                        1,
                        SIDE_LENGTH + (row - 3 * SIDE_LENGTH),
                        (1, 0),
                    )

                elif (
                    col == SIDE_LENGTH
                    and 3 * SIDE_LENGTH + 1 <= row < 4 * SIDE_LENGTH + 1
                    and direction == (0, 1)
                ):
                    newNeighbor = (
                        3 * SIDE_LENGTH,
                        SIDE_LENGTH + (row - (3 * SIDE_LENGTH)),
                        (-1, 0),
                    )

                if newNeighbor is None:
                    print(location, direction, newNeighbor)

                neighbors[location][direction] = newNeighbor

            else:
                neighbors[location][direction] = neighbor + tuple([direction])
    return board, monkeyPath, neighbors, SIDE_LENGTH


def getPassCodeFromBoard(board, monkeyPath, neighbors, SIDE_LENGTH):
    directionInDegrees = 0
    position = min([pos for pos in board if pos[0] == 1], key=lambda pos: pos[1])

    while len(monkeyPath):
        (start, stop) = re.search("[RL]\d+", monkeyPath).span()

        token = monkeyPath[start:stop]

        turn, length = token[0], token[1:]

        if turn == "R":
            directionInDegrees += 90
        else:
            directionInDegrees -= 90

        iterativeDirection = tuple(
            [
                int(-1 * math.cos(math.radians(directionInDegrees))),
                int(math.sin(math.radians(directionInDegrees))),
            ]
        )

        for _ in range(int(length)):

            (row, col, direction) = neighbors[position][iterativeDirection]

            if board[(row, col)] == "#":
                break

            else:
                position = (row, col)

            iterativeDirection = direction
            if direction == (-1, 0):
                directionInDegrees = 0
            elif direction == (1, 0):
                directionInDegrees = 180

            elif direction == (0, 1):
                directionInDegrees = 90

            elif iterativeDirection == (0, -1):
                directionInDegrees = 270

            else:
                raise Exception("SHOULDN'T GET HERE")

        monkeyPath = monkeyPath[stop:]

    print(
        position,
        directionInDegrees,
    )

    return (
        1000 * position[0]
        + 4 * position[1]
        + ((((directionInDegrees - 90) % 360) + 360) % 360) // 90
    )


with open(INPUT_FILE, "r") as f:

    lines = f.readlines()

    board, monkeyPath, neighbors, SIDE_LENGTH = constructBoardOne(lines)

    print(f"P1 = {getPassCodeFromBoard(board, monkeyPath, neighbors, SIDE_LENGTH)}")

    board, monkeyPath, neighbors, SIDE_LENGTH = constructBoardTwo(lines)

    print(f"P2 = {getPassCodeFromBoard(board, monkeyPath, neighbors, SIDE_LENGTH)}")
