import re
from typing import List, Set, Tuple


def overlapWithLine(sensor, beacon, yOfInterest) -> Set[Tuple[int, int]]:
    # intersection of manhattan distance circle and horizontal line
    # r = abs((x - x0)) + abs((y - y0)) and y = yOfInterest
    # e.g. x0=0, y0=0, r=10, yOfInterest=3 => 10 = abs(x) + 3 => x = -7 or 7 => 2 * 7 + 1 = 15 = overlap

    r = abs(beacon[0] - sensor[0]) + abs(beacon[1] - sensor[1])

    # find the y of interest assuming the sensor is at (0,0) in this coordinate plane
    relativeYOfInterest = abs(yOfInterest - sensor[1])

    x = r - relativeYOfInterest

    # no intersection because radius is too short
    if x < 0:
        return []

    return [tuple([i, yOfInterest]) for i in range(sensor[0] - x, sensor[0] + x + 1)]


def parseLine(line: str) -> Tuple[Tuple[int, int], Tuple[int, int]]:

    p = re.search("x=(\-?[0-9]+), y=(\-?[0-9]+).*x=(\-?[0-9]+), y=(\-?[0-9]+)", line)

    found = p.groups()

    return ((int(found[0]), int(found[1])), (int(found[2]), int(found[3])))


def problemOne():

    finalSum = set()
    sensorBeaconSet = set()

    yOfInterest = 2000000

    with open("./input.txt", "r") as f:

        for line in f:

            parsed = parseLine(line.strip())
            sensorBeaconSet.update(parsed[:2])
            print(line.strip())
            overLappingPoints = overlapWithLine(parsed[0], parsed[1], yOfInterest)
            print(len(overLappingPoints))

            finalSum.update(overLappingPoints)

    return len(sorted(list(finalSum - sensorBeaconSet), key=lambda p: p[0]))


def overlapWithLineInterval(sensor, beacon, yOfInterest) -> Tuple[int, int]:
    # intersection of manhattan distance circle and horizontal line
    # r = abs((x - x0)) + abs((y - y0)) and y = yOfInterest
    # e.g. x0=0, y0=0, r=10, yOfInterest=3 => 10 = abs(x) + 3 => x = -7 or 7 => 2 * 7 + 1 = 15 = overlap

    r = abs(beacon[0] - sensor[0]) + abs(beacon[1] - sensor[1])

    # find the y of interest assuming the sensor is at (0,0) in this coordinate plane
    relativeYOfInterest = abs(yOfInterest - sensor[1])

    x = r - relativeYOfInterest

    # no intersection because radius is too short
    if x < 0:
        return None

    # return one dimensional interval
    return (sensor[0] - x, sensor[0] + x + 1)


def findFreeSpace(intervals: List[Tuple[int, int]]) -> List[int]:
    s = sorted(intervals, key=lambda x: x[0])

    ret = [s[0]]

    for i in range(1, len(s)):

        if s[i][0] < ret[-1][1]:

            ret[-1] = (ret[-1][0], max(s[i][1], ret[-1][1]))

        else:
            return ret[-1][1]

    return None


def problemTwo():

    with open("./input.txt", "r") as f:

        lines = [parseLine(line.strip()) for line in f]

        for i in range(0, 4000000):
            intervals = []

            if i % 10000 == 0:
                print(i, end="\r")

            for parsed in lines:

                interval = overlapWithLineInterval(parsed[0], parsed[1], i)

                if interval != None:

                    intervals.append(interval)

            freeSpace = findFreeSpace(intervals)

            if freeSpace != None:

                return 4000000 * freeSpace + i


def main():

    """
    Choosing to leave my unoptimized first solution just in case anyone wants to see the progression
    """
    print(f"P1: {problemOne()}")
    print(f"P2: {problemTwo()}")


main()
