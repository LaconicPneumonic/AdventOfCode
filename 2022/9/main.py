from typing import List, Tuple

movementMap = {"U": (-1, 0), "D": (1, 0), "L": (0, -1), "R": (0, 1)}


def renderSnek(snek: List[Tuple[int, int]]):

    minx, maxx, miny, maxy = 0, 1, 0, 1

    for link in snek:

        minx = min(link[0], minx)
        maxx = max(link[0], maxx)
        miny = min(link[1], miny)
        maxy = max(link[1], maxy)

    ret = [["." for _ in range(maxy - miny + 1)] for _ in range(maxx - minx + 1)]

    for i in reversed(range(len(snek))):
        snekLink = snek[i]

        ret[snekLink[0] - minx][snekLink[1] - miny] = f"{i if i != 0 else 'H'}"

    print("\n".join(["".join(row) for row in ret]))


# incorrect, but left for reflection
def handleMove(
    head: Tuple[int, int], tail: Tuple[int, int], direction: str
) -> Tuple[Tuple[int, int], Tuple[int, int]]:

    # find new head
    move = movementMap[direction]
    newHead = (head[0] + move[0], head[1] + move[1])

    # compute tail
    if abs(newHead[0] - tail[0]) <= 1 and abs(newHead[1] - tail[1]) <= 1:
        return newHead, tail

    newTail = head

    if newHead == tail:
        newTail = tail

    return newHead, newTail


def propogate(newHead: Tuple[int, int], tail: Tuple[int, int]) -> Tuple[int, int]:

    # compute tail

    leftRight = abs(newHead[0] - tail[0])
    upDown = abs(newHead[1] - tail[1])
    if leftRight <= 1 and upDown <= 1:
        return tail

    return (
        (0 if leftRight == 0 else (newHead[0] - tail[0]) // leftRight) + tail[0],
        (0 if upDown == 0 else (newHead[1] - tail[1]) // upDown) + tail[1],
    )


def problemOne():
    with open("./input.txt", "r") as f:

        head, tail = (0, 0), (0, 0)

        positionSet = set()

        positionSet.add(tail)
        for line in f:

            d, amount = line.strip().split(" ")

            for _ in range(int(amount)):
                head, tail = handleMove(head, tail, d)
                positionSet.add(tail)

        print(len(positionSet))


def problemTwo():
    with open("./input.txt", "r") as f:

        snek = [(0, 0) for _ in range(10)]

        positionSet = set()
        positionSet.add(snek[-1])
        for line in f:

            d, amount = line.strip().split(" ")

            for _ in range(int(amount)):

                move = movementMap[d]
                snek[0] = (snek[0][0] + move[0], snek[0][1] + move[1])

                for i in range(len(snek) - 1):

                    front, back = snek[i : i + 2]
                    newBack = propogate(front, back)

                    if back == newBack:
                        break

                    snek[i + 1] = newBack

                positionSet.add(snek[-1])

                # print("===========")
            # renderSnek(snek)
            # print(d, amount)

        print(len(positionSet))


def main():
    problemOne()
    problemTwo()


main()
