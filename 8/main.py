import pprint
from typing import List
from collections import Counter

FILE_NAME = "./input.txt"


def problem2():

    with open(FILE_NAME, "r") as f:

        lines = [l.strip() for l in f.readlines()]

        rows = len(lines)
        cols = len(lines[0])

        visibilityScore = [[0 for _ in range(cols)] for _ in range(rows)]

        rowColPair = [(r, c) for c in range(1, cols - 1) for r in range(1, rows - 1)]

        maxScore = 0
        for r, c in rowColPair:

            # from the left

            left, right, up, down = 0, 0, 0, 0

            val = int(lines[r][c])
            for i in reversed(lines[r][:c]):
                left += 1
                if int(i) >= val:
                    break

            # from the right
            for i in lines[r][c + 1 :]:
                right += 1
                if int(i) >= val:
                    break

            # from the top

            column = "".join([row[c] for row in lines[:r]])
            for i in reversed(column):
                up += 1
                if int(i) >= val:
                    break

            column = "".join([row[c] for row in lines[r + 1 :]])
            for i in column:
                down += 1
                if int(i) >= val:
                    break

            # pprint.pprint(
            #     [
            #         [
            #             lines[row][col] if row == r or c == col else " "
            #             for col in range(cols)
            #         ]
            #         for row in range(rows)
            #     ]
            # )
            # print(left, right, up, down)
            maxScore = max(maxScore, left * right * up * down)

        return maxScore


def problem1():

    with open(FILE_NAME, "r") as f:

        lines = [l.strip() for l in f.readlines()]

        rows = len(lines)
        cols = len(lines[0])

        isVisible = [[False for _ in range(cols)] for _ in range(rows)]

        # top down
        maxSeenSoFar = [-1 for _ in range(cols)]
        for c in range(cols):
            for r in range(rows):

                val = int(lines[r][c])

                isVisible[r][c] |= val > maxSeenSoFar[c]
                maxSeenSoFar[c] = max(maxSeenSoFar[c], val)

        # bottom up
        maxSeenSoFar = [-1 for _ in range(cols)]
        for c in range(cols):
            for r in reversed(range(rows)):

                val = int(lines[r][c])

                isVisible[r][c] |= val > maxSeenSoFar[c]
                maxSeenSoFar[c] = max(maxSeenSoFar[c], val)

        # left to right
        maxSeenSoFar = [-1 for _ in range(rows)]
        for r in range(rows):
            for c in range(cols):

                val = int(lines[r][c])

                isVisible[r][c] |= val > maxSeenSoFar[r]
                maxSeenSoFar[r] = max(maxSeenSoFar[r], val)

        # right to left
        maxSeenSoFar = [-1 for _ in range(rows)]
        for r in range(rows):
            for c in reversed(range(cols)):

                val = int(lines[r][c])

                isVisible[r][c] |= val > maxSeenSoFar[r]
                maxSeenSoFar[r] = max(maxSeenSoFar[r], val)

        return sum([1 if i else 0 for j in isVisible for i in j])


def main():
    print(f"P1: {problem1()}")

    pprint.pprint(problem2())
    # print(f"P2: {'\n'}{'\n'.join(problem2())}")


main()
