from collections import defaultdict, deque


INPUT_FILE = "./input.txt"


board = dict(
    [
        ((row, col), val)
        for row, line in enumerate(open(INPUT_FILE, "r"))
        for col, val in enumerate(line.strip())
    ]
)


def sim(arrows, rows, cols):
    direction = {"^": (-1, 0), "v": (1, 0), "<": (0, -1), ">": (0, 1)}

    ret = []
    for pos, a in arrows:
        ret.append(
            (
                tuple(
                    [
                        1 + (x1 + x2 - 1) % x3
                        for x1, x2, x3 in zip(pos, direction[a], [rows - 1, cols - 1])
                    ]
                ),
                a,
            )
        )

    return ret


def printBoard(arrows, rows, cols, currentPos=None):

    ret = []

    for r in range(rows + 1):

        rowString = []
        for c in range(cols + 1):
            if r == 0 or r == rows or c == 0 or c == cols:
                rowString.append("#")
            else:
                rowString.append(".")

        ret.append(rowString)

    groupedByPos = defaultdict(list)
    for pos, a in arrows:
        groupedByPos[pos].append(a)

    for pos, a in groupedByPos.items():
        ret[pos[0]][pos[1]] = a[0] if len(a) == 1 else str(len(a))

    if currentPos:
        ret[currentPos[0]][currentPos[1]] = "E"

    print("\n".join(["".join(r) for r in ret]))


def traverseBlizzard(startingPos, endingPos, arrows, rows, cols):
    queue = deque()
    queue.append((startingPos, 0, arrows))

    visited = set()

    breadthMax = 0
    while queue:

        curr, timeTaken, blizzardState = queue.popleft()

        if timeTaken > breadthMax:
            print("MAX:", timeTaken, end="\r")
            breadthMax = timeTaken

        # pruning on mod 10 works for some reason. I thought the min
        # would be (rows - 1) * (cols - 1), but this worked for some reason
        if (curr, timeTaken % (10)) in visited:
            # print("PRUNED", (curr, timeTaken % (10)), end="\r")
            continue
        else:
            visited.add((curr, timeTaken % (10)))

        if curr == endingPos:

            return timeTaken, blizzardState

        blizzardState = sim(blizzardState, rows, cols)
        blizzardSet = set([b[0] for b in blizzardState])

        for n in [(-1, 0), (1, 0), (0, 1), (0, -1), (0, 0)]:

            proposed = tuple([x + y for x, y in zip(curr, n)])

            if (
                proposed == endingPos
                or proposed == startingPos
                or (
                    0 < proposed[0] < rows
                    and 0 < proposed[1] < cols
                    and proposed not in blizzardSet
                )
            ):
                queue.append((proposed, timeTaken + 1, blizzardState))


initialArrows = [(pos, val) for pos, val in board.items() if val not in {".", "#"}]
boardRows = max([p[0] for p in board])
boardCols = max([p[1] for p in board])


timeToEnd, arrowState = traverseBlizzard(
    (0, 1), (boardRows, boardCols - 1), initialArrows, boardRows, boardCols
)

print()
print(f"P1: {timeToEnd}")

timeBackToStart, returnedState = traverseBlizzard(
    (boardRows, boardCols - 1), (0, 1), arrowState, boardRows, boardCols
)

print()
print(f"P1.5: {timeToEnd + timeBackToStart}")


timeBackToEnd, _ = traverseBlizzard(
    (0, 1), (boardRows, boardCols - 1), returnedState, boardRows, boardCols
)

print()
print(f"P2: {timeToEnd + timeBackToStart + timeBackToEnd}")
