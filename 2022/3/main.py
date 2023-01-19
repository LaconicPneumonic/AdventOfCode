from functools import cache
import string
from typing import List
FILE_NAME = './input.txt'


@cache
def getLetterScore(letter: str) -> int:
    return (string.ascii_lowercase + string.ascii_uppercase).index(letter) + 1


def getSharedLetter(rucksack: string) -> str:
    totalLength = len(rucksack)

    firstHalf = set()

    for i in range(totalLength):
        if i < totalLength // 2:
            firstHalf.add(rucksack[i])
        elif rucksack[i] in firstHalf:
            return rucksack[i]

    raise Exception('Incorrect Input: ' + rucksack)


def problemTwo():
    with open(FILE_NAME, 'r') as f:

        totalSum = 0

        lineSet: List[str] = []
        for line in f.readlines():
            line = line[:len(line)-1]

            if len(lineSet) != 3:
                lineSet.append(line)

            if len(lineSet) == 3:
                # flush line set
                sharedChar = set(lineSet[0]).intersection(
                    lineSet[1]).intersection(lineSet[2]).pop()

                totalSum += getLetterScore(sharedChar)
                lineSet = []

        return totalSum


def problemOne():

    with open(FILE_NAME, 'r') as f:

        totalSum = 0
        for line in f.readlines():
            line = line[:len(line)-1]

            sharedLetter = getSharedLetter(line)
            totalSum += getLetterScore(sharedLetter)

        return totalSum


def main():

    print(f"P1: {problemOne()}")
    print(f"P2: {problemTwo()}")


main()
