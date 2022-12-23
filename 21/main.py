INPUT_FILE = "./input.txt"
import math
import re
import operator


class CompNode:
    def __init__(self, left, right, op=None, val=None) -> None:
        self.left = left
        self.right = right
        self.operator = op
        self.val = val


def createComputationGraph(lines):
    computationGraph = dict()
    for line in lines:
        result, operation = line.strip().split(": ")

        isNumber = re.search("\d+", operation)

        if isNumber == None:
            left = operation[:4]
            right = operation[7:]
            op = operation[5]

            if op == "+":
                op = operator.add
            elif op == "-":
                op = operator.sub

            elif op == "*":
                op = operator.mul
            else:
                op = operator.truediv

            computationGraph[result] = (left, right, op)

        else:
            val = int(isNumber.group())

            computationGraph[result] = tuple([val])
    return computationGraph


def problemOne(fileContent):
    computationGraph = createComputationGraph(fileContent)

    stack = []
    postOrder = []

    stack.append(("root", computationGraph["root"]))
    while stack:
        result, operation = stack.pop()

        postOrder.append(result)

        if len(operation) != 1:
            stack.append((operation[0], computationGraph[operation[0]]))
            stack.append((operation[1], computationGraph[operation[1]]))

    for result in reversed(postOrder):
        op = computationGraph[result]

        if len(op) == 1:
            computationGraph[result] = op[0]

        else:
            computationGraph[result] = op[2](
                computationGraph[op[0]], computationGraph[op[1]]
            )

    print("ANSWER 1", computationGraph["root"])


def calculateRootVal(computationGraph, start):
    stack = []
    postOrder = []

    stack.append((start, computationGraph[start]))
    while stack:
        result, operation = stack.pop()

        postOrder.append(result)

        if len(operation) != 1:
            stack.append((operation[0], computationGraph[operation[0]]))
            stack.append((operation[1], computationGraph[operation[1]]))

    for result in reversed(postOrder):
        op = computationGraph[result]

        if len(op) == 1:
            computationGraph[result] = op[0]

        else:
            computationGraph[result] = op[2](
                computationGraph[op[0]], computationGraph[op[1]]
            )

    return computationGraph[start]


def problemTwo(fileContent):
    computationGraph = createComputationGraph(fileContent)

    sideWithoutYou = 0
    sideWithYou = 1

    yourName = "humn"

    stack = [computationGraph["root"][0]]

    found = False

    while stack:

        curr = stack.pop()

        if curr == yourName:
            found = True
            break

        if len(computationGraph[curr]) != 1:
            stack.append(computationGraph[curr][0])
            stack.append(computationGraph[curr][1])

    if found:
        sideWithoutYou, sideWithYou = sideWithYou, sideWithoutYou

    leftVal = calculateRootVal(
        computationGraph, computationGraph["root"][sideWithoutYou]
    )

    i = 0

    L = 0.005

    previousVal = 0

    # gradient descent, but it'd be cooler if I could reverse the computation tree
    while True:
        computationGraph = createComputationGraph(fileContent)

        computationGraph[yourName] = tuple([i])

        val = calculateRootVal(computationGraph, computationGraph["root"][sideWithYou])

        if val == leftVal:
            break

        # the derivative of a convex optimization
        gradient = 2 * (leftVal - val)

        i = i - L * gradient

        if abs(i - previousVal) < L:
            break
        previousVal = i

    print("ANSWER 2", round(i))


with open(INPUT_FILE, "r") as f:

    fileContent = f.readlines()
    problemOne(fileContent)
    problemTwo(fileContent)
