from collections import defaultdict
from typing import Dict, List, Tuple


INPUT_FILE = "./input.txt"


def rootShapeAtPoint(point, shape):
    return list(map(lambda p: (p[0] + point[0], p[1] + point[1]), shape))


def findIndexOfRepetition(lines, initialStart=0, initialLength=2):

    stack = [(initialStart, initialLength)]
    memo = dict()

    while stack:

        startOfPattern, lengthOfPattern = stack.pop()

        memo[(startOfPattern, lengthOfPattern)] = True

        patternBase = "\n".join(
            lines[startOfPattern : startOfPattern + lengthOfPattern]
        )
        patternNext = "\n".join(
            lines[
                startOfPattern
                + lengthOfPattern : startOfPattern
                + (2 * lengthOfPattern)
            ]
        )

        if lengthOfPattern > 3000 or startOfPattern > 300:
            continue

        if patternBase == patternNext:

            return startOfPattern, lengthOfPattern
        else:

            if (startOfPattern + 1, lengthOfPattern) not in memo:
                stack.append((startOfPattern + 1, lengthOfPattern))
            if (startOfPattern, lengthOfPattern + 1) not in memo:
                stack.append((startOfPattern, lengthOfPattern + 1))

    return None, None


def simulate(directions, shapeMaps, length) -> List[str]:
    gameMap: Dict[Tuple[int, int], bool] = defaultdict(lambda: False)

    for i in range(7):
        gameMap[(-1, i)] = True

    shapeRoot = (3, 2)
    windIndex = 0
    highestRock = 0
    shapes = 0

    while shapes < length:
        currentShape = shapeMaps[shapes % len(shapeMaps)]
        done = False

        while True:
            windAdjustment = (
                shapeRoot[0],
                shapeRoot[1] + (-1 if directions[windIndex] == "<" else 1),
            )
            windLocation = rootShapeAtPoint(windAdjustment, currentShape)

            for p in windLocation:
                if gameMap[p] or p[1] < 0 or p[1] >= 7:
                    # if I can't apply my wind adjustment, move back
                    windAdjustment = shapeRoot
                    break

            proposedRoot = (windAdjustment[0] - 1, windAdjustment[1])
            proposedLocation = rootShapeAtPoint(proposedRoot, currentShape)

            # find first point of intersection and root the rock to the map
            for p in proposedLocation:
                if gameMap[p]:
                    # add the new rocks to the map
                    for c in rootShapeAtPoint(windAdjustment, currentShape):
                        if c[0] > highestRock:
                            highestRock = c[0]
                        gameMap[c] = True

                    done = True
                    shapeRoot = (highestRock + 4, 2)
                    break

            windIndex = (windIndex + 1) % len(directions)
            if done:
                break
            else:
                shapeRoot = proposedRoot

        shapes += 1

    lines = []
    for row in range(shapeRoot[0]):
        lines.append("".join("#" if gameMap[(row, col)] else "." for col in range(7)))

    return lines


def main():

    directions = ""
    with open(INPUT_FILE, "r") as f:

        directions = f.readlines()[0].strip()

    # positive row means up and positive col means right
    shapeMaps = [
        # horizontal line
        [(0, 0), (0, 1), (0, 2), (0, 3)],
        # plus
        [(0, 1), (1, 1), (1, 0), (1, 2), (2, 1)],
        # bottom corner
        [(0, 0), (0, 1), (0, 2), (1, 2), (2, 2)],
        # vertical line
        [(0, 0), (1, 0), (2, 0), (3, 0)],
        # square
        [(0, 0), (0, 1), (1, 0), (1, 1)],
    ]

    lines = simulate(directions, shapeMaps, 2022)

    print(len(lines) - 3)

    miniSimLines: List[str] = simulate(directions, shapeMaps, len(directions) * 5)

    start, patternLength = findIndexOfRepetition(miniSimLines, 100, 2600)

    print(start, patternLength)

    repeatRocks = sum(
        map(
            lambda p: p.count("#"),
            miniSimLines[start : start + patternLength],
        )
    )

    initialRocks = sum(
        map(
            lambda p: p.count("#"),
            miniSimLines[:start],
        )
    )

    shapes = 0
    totalRocks = 0

    initialShapes, repeatShapes = 0, 0
    while totalRocks <= initialRocks + repeatRocks:

        totalRocks += len(shapeMaps[shapes % len(shapeMaps)])

        if totalRocks == initialRocks:
            initialShapes = shapes + 1
        if totalRocks == repeatRocks:
            repeatShapes = shapes + 1
        shapes += 1

    print(initialRocks, repeatRocks)
    print(initialShapes, repeatShapes)

    bigSimVal = 1000000000000

    moduloSimVal = ((bigSimVal - initialShapes) % repeatShapes) + initialShapes
    totalPatterns = (bigSimVal - initialShapes) // repeatShapes

    residualHeight = simulate(directions, shapeMaps, moduloSimVal)

    print(patternLength * totalPatterns + len(residualHeight) - 3)


main()
