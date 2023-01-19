import json


def orderChecker(leftOriginal, rightOriginal):

    stack = [(leftOriginal, rightOriginal, 0)]

    inOrder = True
    logs = []

    while inOrder and stack:

        left, right, index = stack.pop()

        lType = type(left)
        rType = type(right)

        logs.append((left, "<|>", right, index))

        if lType == int and rType == int:
            if left == right:
                continue
            elif left > right:
                inOrder = False
                logs.append(["LEFT GREATER THAN RIGHT"])
            else:
                return True

        elif lType == list and rType == list:
            if len(right) <= index and index < len(left):
                logs.append([f"RIGHT EXHAUSTED"])
                inOrder = False
                continue

            elif len(left) <= index and len(right) <= index:
                # if I reach the end of both, move on
                continue

            elif len(left) <= index:
                logs.append(["REACHED THE END OF left"])
                return True

            stack.append((left, right, index + 1))
            stack.append((left[index], right[index], 0))

        elif lType == list and rType == int:
            stack.append((left, [right], 0))
        elif lType == int and rType == list:
            stack.append(([left], right, 0))

    return inOrder


def problemOne():

    with open("./input.txt", "r") as f:

        left, right = None, None

        i = 1

        runningSum = 0

        for rawLine in f:

            line = rawLine.strip()

            if line == "":
                left, right = None, None

            elif left == None:
                left = json.loads(line)

            elif right == None:
                right = json.loads(line)

            if left != None and right != None:

                valid = orderChecker(left, right)

                if valid:

                    runningSum += i
                i += 1

        return runningSum


# quick sort implementation taken from
# https://www.geeksforgeeks.org/quicksort-using-random-pivoting/
# just wanted to try it out
def partition(array, low, high, compare):
    pivotValue = array[high]

    i = low - 1

    for j in range(low, high):

        if compare(array[j], pivotValue):

            i = i + 1
            (array[i], array[j]) = (array[j], array[i])

    (array[i + 1], array[high]) = (array[high], array[i + 1])

    return i + 1


def quickSort(array, low, high, compare):

    stack = [(low, high)]
    while stack:

        l, h = stack.pop()

        if l >= h:
            continue

        pivot = partition(array, l, h, compare)

        stack.append((l, pivot - 1))
        stack.append((pivot + 1, h))


def problemTwo():

    with open("./input.txt", "r") as f:

        packets = list(
            map(
                json.loads,
                [packet.strip() for packet in f.readlines() if packet.strip() != ""],
            )
        )

        packets.append([[2]])
        packets.append([[6]])

        quickSort(packets, 0, len(packets) - 1, orderChecker)

        a = 1 + packets.index([[2]])
        b = 1 + packets.index([[6]])

        return a * b


def main():
    # iterative only!
    print(f"Problem 1: {problemOne()}")
    print(f"Problem 2: {problemTwo()}")


main()
