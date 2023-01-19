from functools import cache
inputFile = "./input.txt"


@cache
def calcPointsForMeTwo(game: str) -> int:

    theirs, mine = game.split(" ")

    dominance = {
        'A': 'C',
        'B': 'A',
        'C': 'B'
    }

    transformDictionary = {
        'A': 'X',
        'B': 'Y',
        'C': 'Z'
    }

    reversedDominance = {
        value: key for key, value in dominance.items()
    }

    shouldPlay = theirs

    if mine == 'X':
        shouldPlay = dominance[theirs]

    elif mine == 'Z':
        shouldPlay = reversedDominance[theirs]

    return calcPointsForMe(f"{theirs} {transformDictionary[shouldPlay]}")


@cache
def calcPointsForMe(game: str) -> int:
    transformDictionary = {
        'A': 'R',
        'B': 'P',
        'C': 'S',
        'X': 'R',
        'Y': 'P',
        'Z': 'S',
    }

    theirs, mine = map(lambda x: transformDictionary[x], game.split(" "))

    dominance = {
        'R': 'S',
        'S': 'P',
        'P': 'R'
    }

    points = {
        'R': 1,
        'P': 2,
        'S': 3
    }

    winPoints = 3 if theirs == mine else (
        6 if dominance[mine] == theirs else 0)

    return winPoints + points[mine]


def problemTwo():
    with open(inputFile, 'r') as f:

        total = 0
        for line in f.readlines():
            line = line[:len(line) - 1]
            total += calcPointsForMeTwo(line)

        print(f"TOTAL: {total}")


def problemOne():

    with open(inputFile, 'r') as f:

        total = 0
        for line in f.readlines():
            line = line[:len(line) - 1]
            total += calcPointsForMe(line)

        print(f"TOTAL: {total}")


def main():
    problemOne()
    problemTwo()


main()
