import operator
from collections import defaultdict, deque
import pprint

INPUT_FILE = "./input.txt"


def parseGraph(rawGraph):

    rows, cols = len(rawGraph), len(rawGraph[0])

    points = [(row, col) for col in range(cols) for row in range(rows)]
    isValid = lambda x: 0 <= x[0] < rows and 0 <= x[1] < cols

    graph = defaultdict(set)
    start, end = None, None

    for point in points:

        rawPointVal = rawGraph[point[0]][point[1]]

        neighbors = [
            tuple(map(operator.add, point, mutation))
            for mutation in [[1, 0], [-1, 0], [0, 1], [0, -1]]
            if isValid(list(map(operator.add, point, mutation)))
        ]

        elevationMask = {"S": "a", "E": "z"}

        if rawPointVal == "S":
            start = point
        elif rawPointVal == "E":
            end = point

        print(point, rawPointVal, "->", end=" ")
        for neighbor in neighbors:
            rawNeighborVal = rawGraph[neighbor[0]][neighbor[1]]

            startElevation = (
                elevationMask[rawPointVal]
                if rawPointVal in elevationMask
                else rawPointVal
            )

            endElevation = (
                elevationMask[rawNeighborVal]
                if rawNeighborVal in elevationMask
                else rawNeighborVal
            )

            if ord(endElevation) - ord(startElevation) <= 1:
                print(
                    neighbor,
                    rawNeighborVal,
                    end=" ",
                )

                graph[point].add(neighbor)

        print()
    return graph, start, end


def bfs(parsedGraph, start, end):
    queue = deque()

    visited = set()

    queue.append((start, []))

    finalPath = []
    while queue:

        curr, path = queue.popleft()

        if curr == end:

            finalPath = path + [curr]
            break

        for n in parsedGraph[curr]:
            if n not in visited:
                visited.add(n)
                queue.append((n, path + [curr]))

    return finalPath


def printPath(rawGraph, finalPath):
    charMap = {
        (-1, 0): "^",
        (1, 0): "v",
        (0, 1): ">",
        (0, -1): "<",
    }

    printableGraph = [
        [v if v in ["S", "E"] else "." for v in line] for line in rawGraph
    ]
    for i in range(len(finalPath) - 1):
        diff = tuple(map(operator.sub, finalPath[i + 1], finalPath[i]))
        printableGraph[finalPath[i][0]][finalPath[i][1]] = charMap[diff]

    for line in printableGraph:
        print("".join(line))


def problemOne(rawGraph, parsedGraph, start, end):
    finalPath = bfs(parsedGraph, start, end)

    print(f"Final path length: {len(finalPath) - 1}")
    printPath(rawGraph, finalPath)


def problemTwo(rawGraph, parsedGraph, _, end):

    possibleStarts = [
        (row, col)
        for row in range(len(rawGraph))
        for col in range(len(rawGraph[0]))
        if rawGraph[row][col] == "a"
    ]

    minValidPath = []
    minValidPathLength = float("inf")

    for start in possibleStarts:
        path = bfs(parsedGraph, start, end)

        if 0 < len(path) < minValidPathLength:
            # skip empty paths i.e. there is no path
            minValidPath = path
            minValidPathLength = len(path)

    print(f"Min path length: {len(minValidPath)- 1}")
    printPath(rawGraph, minValidPath)


def main():
    with open(INPUT_FILE, "r") as f:
        rawGraph = [line.strip() for line in f.readlines()]
        parsedGraph, start, end = parseGraph(rawGraph)

        print("P1")
        problemOne(rawGraph, parsedGraph, start, end)
        print("P2")
        problemTwo(rawGraph, parsedGraph, start, end)


main()
