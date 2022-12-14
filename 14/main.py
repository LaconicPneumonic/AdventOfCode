from collections import defaultdict
from typing import Dict, List, Tuple

INPUT_FILE = "./input.txt"


def interpolatePoints(start, end) -> List[Tuple[int, int]]:

    d = 0 if end[0] - start[0] else 1

    ret = []
    iteration = (end[d] - start[d]) // abs(end[d] - start[d])
    for i in range(start[d], end[d], iteration):

        temp = list(start)

        temp[d] = i

        ret.append(tuple(temp))

    return ret


def parseMap():

    finalMap = defaultdict(lambda: ".")

    with open(INPUT_FILE, "r") as f:

        for line in f:
            boundary = [
                tuple(map(int, l.split(","))) for l in line.strip().split(" -> ")
            ]

            finalBoundary = []
            for i in range(len(boundary) - 1):
                finalBoundary += interpolatePoints(boundary[i], boundary[i + 1])

            finalBoundary.append(boundary[-1])

            for p in finalBoundary:
                finalMap[p] = "#"

    return finalMap


def simulate(rockMap):

    done = False
    i = 0
    MAX_ITER = 100000

    sand = (500, 0)
    sandCount = 0

    while not done and i < MAX_ITER:
        if rockMap[(sand[0], sand[1] + 1)] == ".":
            sand = (sand[0], sand[1] + 1)
        elif rockMap[(sand[0] - 1, sand[1] + 1)] == ".":
            sand = (sand[0] - 1, sand[1] + 1)
        elif rockMap[(sand[0] + 1, sand[1] + 1)] == ".":
            sand = (sand[0] + 1, sand[1] + 1)

        else:
            rockMap[sand] = "#"
            sand = (500, 0)
            sandCount += 1

        i += 1

    print(sandCount)


def simulateTwo(rockMap: Dict[Tuple[int, int], str]):

    done = False
    i = 0
    MAX_ITER = 100000000

    sand = (500, 0)
    sandCount = 0

    floor = 2 + max([y for y in map(lambda p: p[1], rockMap.keys())])

    while not done and i < MAX_ITER:
        # print(i, sand)
        if rockMap[(sand[0], sand[1] + 1)] == ".":

            if sand[1] + 1 == floor:
                if sand == (500, 0):
                    sandCount += 1
                    break
                rockMap[sand] = "#"
                sand = (500, 0)
                sandCount += 1
            else:
                sand = (sand[0], sand[1] + 1)
        elif rockMap[(sand[0] - 1, sand[1] + 1)] == ".":
            sand = (sand[0] - 1, sand[1] + 1)
        elif rockMap[(sand[0] + 1, sand[1] + 1)] == ".":
            sand = (sand[0] + 1, sand[1] + 1)

        else:
            if sand == (500, 0):
                sandCount += 1
                break
            rockMap[sand] = "#"
            sand = (500, 0)
            sandCount += 1

        i += 1

    print(sandCount)


simulate(parseMap())
simulateTwo(parseMap())
